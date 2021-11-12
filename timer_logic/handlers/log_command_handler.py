from sqlite3 import IntegrityError
import datetime

from typing import Union

from .command_handler_base_class import Handler
from timer_database.dbManager import DbUpdate
from command_classes.commands import *
from timer_session.timer_session import Session
from timer_session.timer_session import write_session_data_to_json
from timer_session.timer_session import reset_json_data
from utils.exceptions import CommandSequenceError, TimeSequenceError
from utils.command_enums import InputType


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
            if self.command.time < self.session.last_command_time:
                raise TimeSequenceError('Error: New time is before old time')

    def _start_command(self):
        try:
            # Creating new session SPECIFIC TO START
            project = self.session.project_id
            date = self.command.time.strftime('%Y-%m-%d')  # ToDo - not a datetime object, refactor
            note = self.command.session_note
            session_data = project, date, None, note
            session_id = DbUpdate().create_session(session_data)
            self.session.session_id = session_id
            self.session.session_start_time = self.command.time
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
        if self.command.log_note:
            self.session.log_note = self.command.log_note
        self.session.last_command = self.command.command
        self.session.last_command_time = self.command.time
        write_session_data_to_json(self.session)

    def _log_time_to_db(self):
        session_id = self.session.session_id
        start_log_time = self.session.last_command_time
        end_log_time = self.command.time
        start_note = self.session.log_note
        end_note = self.command.log_note
        log = session_id, start_log_time, end_log_time, start_note, end_note
        DbUpdate().create_time_log(log)

    def _close_session(self):
        session_id = self.session.session_id
        data = datetime.today(), session_id
        DbUpdate().close_session(data)

    def handle(self):
        try:
            self._validate_command()
            if self.command.command == InputType.START:
                self._start_command()
            elif self.command.command == InputType.PAUSE:
                self._pause_command()
            elif self.command.command == InputType.RESUME:
                self._resume_command()
            elif self.command.command == InputType.STOP:
                self._stop_command()
            else:
                pass
            self._display_command_summary()
        except (TimeSequenceError, CommandSequenceError) as e:
            print(e)

    def _display_command_summary(self):
        print(f'{self.command.get_command_name().capitalize()} {self.session.project_name} session at '
              f'{self.session.last_command_time}')
        if self.command.command == InputType.STOP:
            print('Queue has been cleared. Use FETCH to queue another project.')
