import time
from sqlite3 import IntegrityError
import datetime
from sys import exit
from typing import Union

from .command_handler_base_class import Handler

from ...command_classes.log_commands import LogCommand
from ...command_classes.log_commands import StartCommand
from ...command_classes.log_commands import PauseCommand
from ...command_classes.log_commands import ResumeCommand
from ...command_classes.log_commands import StopCommand

from src.timer_database.dbManager import DbUpdate
from src.timer_session.sessions_manager import SessionManager
from src.utils.exceptions import CommandSequenceError, TimeSequenceError
from src.utils.command_enums import InputType


class LogCommandHandler(Handler):

    def __init__(self, session_manager: SessionManager):
        self.session = session_manager.get_current_session()
        self.session_manager = session_manager

    def _start_command(self, command: StartCommand):
        try:
            # Creating new session SPECIFIC TO START
            project = self.session.project_id
            date = command.time.strftime('%Y-%m-%d')
            note = command.session_note
            session_data = project, date, None, note
            session_id = DbUpdate().create_session(session_data)
            self.session.session_id = session_id
            self.session.session_start_time = command.time
            # UPDATE SESSION and WRITE TO JSON
            self._update_session(command)
        except IntegrityError as e:
            print(e)

    def _pause_command(self, command: PauseCommand):
        # gather data and creating log for DB
        self._log_time_to_db(command)
        # updating session and JSON
        self._update_session(command)

    def _resume_command(self, command: ResumeCommand):
        self._update_session(command)

    def _stop_command(self, command: StopCommand):
        # Logging data to db if START or RESUME are previous commands
        if self.session.last_command != InputType.PAUSE or InputType.NO_SESSION:
            self._log_time_to_db(command)

        # Closing session of all previous command types except NO_SESSION
        if self.session.last_command != InputType.NO_SESSION:
            self._close_session()

        # Getting new current session
        new_current_pid = self.session_manager.stop_select_new_current_session()
        if new_current_pid is not None:
            self.session_manager.switch_current_session(new_current_pid)

        # Removing Session
        self.session_manager.remove_session(self.session.project_id)
        self.session_manager.export_sessions_to_json()

    def _update_session(self, command: LogCommand):
        if command.log_note:
            self.session.last_command_log_note = command.log_note
        self.session.last_command = command.command
        self.session.last_command_time = command.time
        self.session_manager.export_sessions_to_json()

    def _log_time_to_db(self, command: LogCommand):
        session_id = self.session.session_id
        start_log_time = self.session.last_command_time
        end_log_time = command.time
        start_note = self.session.last_command_log_note
        end_note = command.log_note
        log = session_id, start_log_time, end_log_time, start_note, end_note
        DbUpdate().create_time_log(log)

    def _close_session(self):
        session_id = self.session.session_id
        data = datetime.datetime.today(), session_id
        DbUpdate().close_session(data)

    def handle(self, command: LogCommand):
        try:
            command.validate_sequence(self.session.last_command)
            command.validate_time(self.session.last_command_time)
        except (TimeSequenceError, CommandSequenceError) as e:
            print(e)
        else:
            if isinstance(command, StartCommand):
                self._start_command(command)
            elif isinstance(command, PauseCommand):
                self._pause_command(command)
            elif isinstance(command, ResumeCommand):
                self._resume_command(command)
            elif isinstance(command, StopCommand):
                self._stop_command(command)
            self._display_command_summary(command)

    def _display_command_summary(self, command: LogCommand):
        print(f'{command.get_command_name().capitalize()} {self.session.project_name} session at '
              f'{command.time.strftime("%H:%M:%S")}')
        if command.command == InputType.STOP:
            print('Queue has been cleared. Use FETCH to queue another project.')
