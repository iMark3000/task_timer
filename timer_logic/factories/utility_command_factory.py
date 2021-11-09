
from .command_factory_base_class import CommandAbstractFactory

from command_classes.commands import UtilityCommand
from command_classes.commands import NewCommand
from command_classes.commands import FetchProject
from command_classes.commands import StatusCheck
from command_classes.commands import SwitchCommand
from command_classes.commands import ProjectsCommand

from utils.command_enums import InputType


class UtilityCommandFactory(CommandAbstractFactory):
    # Todo: Tuple was changed, need to update these instance vars
    def __init__(self, command_dict: dict):
        self.command = command_dict['command']
        self.project_id = command_dict['command_args'].project_id
        self.project_name = command_dict['command_args'].project_name

    def create_command(self) -> UtilityCommand:
        if self.command == InputType.FETCH:
            return FetchProject(self.command, project_id=self.project_id)
        elif self.command == InputType.NEW:
            return NewCommand(self.command, project_name=self.project_name)
        elif self.command == InputType.STATUS:
            return StatusCheck(self.command)
