
from .command_factory_base_class import CommandAbstractFactory

from command_classes.commands import DeactivateCommand
from command_classes.commands import ReactivateCommand
from command_classes.commands import RenameCommand
from command_classes.commands import EditCommand
from command_classes.commands import MergeCommand


class UpdateCommandFactory(CommandAbstractFactory):

    def __init__(self, command_dict: dict):
        self.command = command_dict['command']

    def create_command(self):
        pass
