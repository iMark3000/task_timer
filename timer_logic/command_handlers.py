from abc import ABC
import datetime

from typing import Union

from timer_database.dbManager import DbUpdate, DbQuery
from .commands import LogCommand, QueryCommand, UtilityCommand
from timer_session.timer_session import Session, write_session_data_to_json, reset_json_data
from utils.exceptions import CommandSequenceError, TimeSequenceError
from utils.command_enums import InputType


class Handler(ABC):

    def __init__(self, command: Union[LogCommand, QueryCommand, UtilityCommand]):
        self.command = command


class LogCommandHandler(Handler):

    def __init__(self, command: LogCommand, session: Session):
        self.session = session
        super().__init__(command)

    def _validate_command(self):
        try:
            self.command.validate_sequence(self.session.get_last_command_enum())
        except CommandSequenceError as e:
            print(e)
        try:
            self._validate_command_time()
        except TimeSequenceError as e:
            print(e)

    def _validate_command_time(self):
        if self.session.get_last_command_time():
            if self.command.get_command_time() < self.session.get_last_command_time():
                raise TimeSequenceError('Error: New time is before old time')

    def start_command(self):
        # Creating new session SPECIFIC TO START
        project = self.session.get_project_id()
        session_data = project, self.command.get_command_time(), None
        session_id = DbUpdate().create_session(session_data)
        self.session.update_session_id(session_id)
        self.session.update_session_start_time(self.command.get_command_time())
        # UPDATE SESSION and WRITE TO JSON
        self.update_session()

    def pause_command(self):
        # gather data and creating log for DB
        self.log_time_to_db()
        # updating session and JSON
        self.update_session()

    def resume_command(self):
        self.update_session()

    def stop_command(self):
        #  ToDo: Stop needs to be handled differently coming after PAUSE
        # gather data and creating log for DB
        self.log_time_to_db()
        # close session
        self.close_session()
        # reset json
        reset_json_data()

    def update_session(self):
        self.session.update_last_command(self.command.get_command_name())
        self.session.update_last_command_time(self.command.get_command_time())
        write_session_data_to_json(self.session)

    def log_time_to_db(self):
        session_id = self.session.get_session_id()
        start_log_time = self.session.get_last_command_time()
        end_log_time = self.command.get_command_time()
        log = session_id, start_log_time, end_log_time
        DbUpdate.create_time_log(log)

    def close_session(self):
        session_id = self.session.get_session_id()
        data = datetime.date.today(), session_id
        DbUpdate.close_session(data)


class QueryCommandHandler(Handler):

    def __init__(self, command: QueryCommand):
        super().__init__(command)


class UtilityCommandHandler(Handler):

    def __init__(self, command: UtilityCommand, session: Session):
        self.session = session
        super().__init__(command)
        self.handle()

    def handle(self):
        if self.command.get_command_type() == InputType.FETCH:
            self._fetch_project()
        elif self.command.get_command_type() == InputType.STATUS:
            self._status_check()
        elif self.command.get_command_type() == InputType.NEW:
            self._new_project()

    def _fetch_project(self):
        project_id = self.command.get_project_id()  # This works even though PyCharm disagrees
        results = DbQuery.fetch_project(project_id)
        project_name = results[1]
        self.session.update_project_id(project_id)
        self.session.update_project_name(project_name)

    def _new_project(self):
        tup = (self.command.get_command_name(), 1)
        project = DbUpdate().create_project(tup)
        print(f'{self.command.get_command_name()} [project] created!!!')

    def _status_check(self):
        if self.session.get_project_name() and self.session.get_last_command_str():
            # Todo: This will need to be reworked later
            print(f'Current project: {self.session.get_project_name()}')
            print(f'Session started on {self.session.get_session_start_time()}')
            print(f'Last command {self.session.get_last_command_str()} on {self.session.get_last_command_time()}')
        elif self.session.get_project_name():
            print(f'Project Queued Up: {self.session.get_project_name()}')
            print(f'No session in progress')
        else:
            print('No project queued and no session in progress.')


