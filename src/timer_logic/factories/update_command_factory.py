
from .command_factory_base_class import CommandAbstractFactory

from ...command_classes.update_commands import ReactivateCommand
from ...command_classes.update_commands import RenameCommand

from src.utils.command_enums import InputType


class UpdateCommandFactory(CommandAbstractFactory):

    def __init__(self, command: InputType, command_args: dict):
        self.command = command
        self.command_args = command_args

    def create_command(self):
        if self.command == InputType.REACTIVATE:
            return ReactivateCommand(self.command, **self.command_args)
        elif self.command == InputType.RENAME:
            return RenameCommand(self.command, **self.command_args)
