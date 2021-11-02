from sqlite3 import IntegrityError
import datetime

from typing import Union

from timer_database.dbManager import DbUpdate, DbQuery
from command_classes.commands import *
from timer_session.timer_session import Session
from timer_session.timer_session import write_session_data_to_json
from timer_session.timer_session import reset_json_data
from timer_session.timer_session import fetch_helper_func
from utils.exceptions import CommandSequenceError, TimeSequenceError
from utils.command_enums import InputType


class Handler(ABC):

    @abstractmethod
    def handle(self):
        pass


class LogCommandHandler(Handler):

    def __init__(self, command: Union[LogCommand, StartCommand], session: Session):
        self.session = session
        self.command = command

    def _validate_command(self):
        try:
            self.command.validate_sequence(self.session.last_command)
        except CommandSequenceError as e:
            print(e)
        try:
            self._validate_command_time()
        except TimeSequenceError as e:
            print(e)

    def _validate_command_time(self):
        # Todo: Time cannot be in future
        if self.session.last_command_time:
            if self.command.get_command_time() < self.session.last_command_time:
                raise TimeSequenceError('Error: New time is before old time')

    def _start_command(self):
        try:
            # Creating new session SPECIFIC TO START
            project = self.session.project_id
            date = self.command.get_command_time().strftime('%Y-%m-%d')  # ToDo - not a datetime object, refactor
            note = self.command.get_session_note()
            session_data = project, date, None, note
            session_id = DbUpdate().create_session(session_data)
            self.session.session_id = session_id
            self.session.session_start_time = self.command.get_command_time()
            # UPDATE SESSION and WRITE TO JSON
            self._update_session()
        except IntegrityError as e:
            print(e)

    def _pause_command(self):
        # gather data and creating log for DB
        self._log_time_to_db()
        # updating session and JSON
        self._update_session()

    def _resume_command(self):
        self._update_session()

    def _stop_command(self):
        # gather data and creating log for DB
        if self.session.last_command != InputType.PAUSE:
            self._log_time_to_db()
        # close session
        self._close_session()
        # reset json
        reset_json_data()

    def _update_session(self):
        if self.command.get_log_note():
            self.session.log_note = self.command.get_log_note()
        self.session.last_command = self.command.get_command_type()
        self.session.last_command_time = self.command.get_command_time()
        write_session_data_to_json(self.session)

    def _log_time_to_db(self):
        session_id = self.session.session_id
        start_log_time = self.session.last_command_time
        end_log_time = self.command.get_command_time()
        start_note = self.session.log_note
        end_note = self.command.get_log_note()
        log = session_id, start_log_time, end_log_time, start_note, end_note
        DbUpdate().create_time_log(log)

    def _close_session(self):
        session_id = self.session.session_id
        data = datetime.today(), session_id
        DbUpdate().close_session(data)

    def handle(self):
        try:
            self._validate_command()
            if self.command.get_command_type() == InputType.START:
                self._start_command()
            elif self.command.get_command_type() == InputType.PAUSE:
                self._pause_command()
            elif self.command.get_command_type() == InputType.RESUME:
                self._resume_command()
            elif self.command.get_command_type() == InputType.STOP:
                self._stop_command()
            else:
                pass
            self._display_command_summary()
        except (TimeSequenceError, CommandSequenceError) as e:
            print(e)

    def _display_command_summary(self):
        print(f'{self.command.get_command_name().capitalize()} {self.session.project_name} session at '
              f'{self.session.last_command_time}')
        if self.command.get_command_type() == InputType.STOP:
            print('Queue has been cleared. Use FETCH to queue another project.')


class QueryCommandHandler(Handler):

    def __init__(self, command: QueryCommand):
        super().__init__(command)

    def handle(self):
        pass


class UtilityCommandHandler(Handler):

    def __init__(self, command: Union[FetchProject, StatusCheck, NewCommand], session: Session):
        self.session = session
        self.command = command

    def handle(self):
        if self.command.get_command_type() == InputType.FETCH:
            self._fetch_project()
        elif self.command.get_command_type() == InputType.STATUS:
            self._status_check()
        elif self.command.get_command_type() == InputType.NEW:
            self._new_project()

    def _fetch_project(self):
        project_id = (self.command.get_project_id(),)  # This works even though PyCharm disagrees
        results = DbQuery().fetch_project(project_id)
        project_name = results[1]
        fetch_helper_func(self.session, project_name, self.command.get_project_id())
        write_session_data_to_json(self.session)
        print(f'Fetched {self.session.project_name} -- Now in queue')

    def _new_project(self):
        tup = (self.command.get_project_name(), 1)
        project = DbUpdate().create_project(tup)
        print(f'{self.command.get_project_name()} [ID: {project}] created!!!')

    def _status_check(self):
        # Todo: This will need to be reworked later
        if self.session.project_name and self.session.last_command != InputType.NO_SESSION:
            print(f'Current project: {self.session.project_name}')
            print(f'Session started on {self.session.session_start_time}')
            print(f'Last command {self.session.last_command.name.upper()} on {self.session.last_command_time}')
        elif self.session.project_name:
            print(f'Project Queued Up: {self.session.project_name}')
            print(f'No session in progress')
        else:
            print('No project queued and no session in progress.')
