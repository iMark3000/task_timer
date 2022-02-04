from typing import Union
from .command_factory_base_class import CommandAbstractFactory

from ...command_classes.config_commands import ConfigCommand
from src.utils.command_enums import InputType


class ConfigCommandFactory(CommandAbstractFactory):

    def __init__(self, command: InputType, command_args: Union[dict, None]):
        self.command = command
        self.command_args = command_args

    def create_command(self):
        return ConfigCommand(self.command, **self.command_args)
