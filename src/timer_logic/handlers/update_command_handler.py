from .command_handler_base_class import Handler

from ...command_classes.update_commands import UpdateCommand
from ...command_classes.update_commands import DeactivateCommand
from ...command_classes.update_commands import ReactivateCommand
from ...command_classes.update_commands import RenameCommand
from ...command_classes.update_commands import MergeCommand
from src.timer_session.sessions_manager import SessionManager
from src.timer_database.dbManager import DbUpdate


class UpdateCommandHandler(Handler):

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.db_manager = DbUpdate()

    def handle(self, command: UpdateCommand):
        if isinstance(command, ReactivateCommand):
            self._reactivate_command(command)
        elif isinstance(command, DeactivateCommand):
            self._deactivate_command(command)

    def _reactivate_command(self, command: ReactivateCommand):
        self.db_manager.reactivate_project((command.project_id,))

    def _deactivate_command(self, command: DeactivateCommand):
        self.db_manager.deactivate_project((command.project_id,))
        self.session_manager.close_session(command.project_id)
        self.db_manager.close_session((command.project_id,))
