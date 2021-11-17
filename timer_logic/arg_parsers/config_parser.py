from collections import namedtuple

from .arg_parse_base_class import CommandArgParser
from utils.command_enums import InputType


class ConfigCommandArgParser(CommandArgParser):

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def _setup_arg_dict(self):
        self.arg_dict['view'] = False
        self.arg_dict['config_key'] = None
        self.arg_dict['config_value'] = None

    def parse(self) -> tuple:
        if not self.command_args:
            self.arg_dict['view'] = True
        elif self.command_args[0].upper() == 'VIEW':
            self.arg_dict['view'] = True
        else:
            self.arg_dict['key'], self.arg_dict['value'], *_ = self.command_args

        return super().get_command_tuple()
