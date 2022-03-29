import datetime

from .command_handler_base_class import Handler

from ...command_classes.update_commands import UpdateCommand
from ...command_classes.update_commands import DeactivateCommand
from ...command_classes.update_commands import ReactivateCommand
from ...command_classes.update_commands import RenameCommand
from ...command_classes.update_commands import MergeCommand
from src.timer_session.sessions_manager import SessionManager
from src.timer_database.dbManager import DbUpdate

from src.utils.command_enums import InputType


class UpdateCommandHandler(Handler):

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.db_manager = DbUpdate()

    def handle(self, command: UpdateCommand):
        if isinstance(command, ReactivateCommand):
            self._reactivate_command(command)
        elif isinstance(command, DeactivateCommand):
            self._deactivate_command(command)
        elif isinstance(command, RenameCommand):
            self._rename_command(command)

    def _rename_command(self, command: RenameCommand):
        session = self.session_manager.get_session(command.project_id)
        if session is not None:
            session.project_name = command.new_name
            self.session_manager.export_sessions_to_json()

        old_name = self.db_manager.rename_project((command.new_name, command.project_id))
        print(f'Renamed project {command.project_id} -> {old_name} is now {command.new_name}')

    def _reactivate_command(self, command: ReactivateCommand):
        record = self.db_manager.reactivate_project((command.project_id,))
        if record is not None:
            print(f'{record[1]} [{record[0]}] has been reactivated.')
        else:
            print(f'Project ID #{command.project_id} was not found in the database.')

    def _deactivate_command(self, command: DeactivateCommand):
        session = self.session_manager.get_session(command.project_id)
        if session is not None:
            if session.last_command == InputType.START or session.last_command == InputType.RESUME:
                data = (session.session_id, session.last_command_time, datetime.datetime.now(), session.last_command_log_note, None)
                self.db_manager.create_time_log(data)
                stop_date = datetime.datetime.date()
            else:
                stop_date = session.get_session_start_date()
            self.db_manager.close_session((stop_date, session.session_id))
            self.session_manager.close_session(command.project_id)
        record = self.db_manager.deactivate_project((command.project_id,))
        if record is not None:
            print(f'{record[1]} [{record[0]}] has been deactivated.')
        else:
            print(f'Project ID #{command.project_id} was not found in the database.')
