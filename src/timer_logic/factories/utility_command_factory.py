from .command_factory_base_class import CommandAbstractFactory

from ...command_classes.utility_commands import UtilityCommand
from ...command_classes.utility_commands import StatusCheck
from ...command_classes.utility_commands import ProjectsCommand
from ...command_classes.utility_commands import NewCommand
from ...command_classes.utility_commands import FetchProject
from ...command_classes.utility_commands import SwitchCommand
from ...command_classes.utility_commands import RemoveCommand

from src.utils.command_enums import InputType


class UtilityCommandFactory(CommandAbstractFactory):
    # Todo: Tuple was changed, need to update these instance vars
    def __init__(self, command: InputType, command_args: dict):
        self.command = command
        self.command_args = command_args

    def create_command(self) -> UtilityCommand:
        if self.command == InputType.STATUS:
            return StatusCheck(self.command, **self.command_args)
        elif self.command == InputType.PROJECTS:
            return ProjectsCommand(self.command, **self.command_args)
        elif self.command == InputType.NEW:
            return NewCommand(self.command, **self.command_args)
        elif self.command == InputType.FETCH:
            return FetchProject(self.command, **self.command_args)
        elif self.command == InputType.SWITCH:
            return SwitchCommand(self.command, **self.command_args)
        elif self.command == InputType.REMOVE:
            return RemoveCommand(self.command, **self.command_args)
