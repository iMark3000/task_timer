from collections import namedtuple

from .arg_parse_base_class import CommandArgParser
from src.utils.command_enums import InputType


class ConfigCommandArgParser(CommandArgParser):

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def _setup_arg_dict(self):
        self.arg_dict['view'] = False
        self.arg_dict['config_key'] = None
        self.arg_dict['config_value'] = None

    def parse(self) -> tuple:
        for c in self.command_args:
            if c.lower() == 'view':
                self.arg_dict['view'] = True
            elif c.lower() == 'fetch' or c.lower() == 'switch' or c.lower() == 'test':
                self.arg_dict['config_toggle'] = c.lower()
        return super().get_command_tuple()
