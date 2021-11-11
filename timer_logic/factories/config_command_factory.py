
from .command_factory_base_class import CommandAbstractFactory

from command_classes.commands import ConfigCommand


class ConfigCommandFactory(CommandAbstractFactory):

    def __init__(self, command_args: tuple):
        self.command = command_dict[0]
        self.view = command_dict['command_args'].view
        self.config_key = command_dict['command_args'].config_key
        self.config_value = command_dict['command_args'].config_value

    def create_command(self):
        return ConfigCommand(self.command, self.view, self.config_key, self.config_value)
