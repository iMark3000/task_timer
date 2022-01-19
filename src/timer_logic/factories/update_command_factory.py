
from .command_factory_base_class import CommandAbstractFactory


class UpdateCommandFactory(CommandAbstractFactory):

    def __init__(self, command_dict: dict):
        self.command = command_dict['command']

    def create_command(self):
        pass
