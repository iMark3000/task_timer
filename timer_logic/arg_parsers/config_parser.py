from collections import namedtuple

from .arg_parse_base_class import CommandArgParser
from utils.command_enums import InputType


ConfigArgs = namedtuple("ConfigArgs", "view config_key config_value")


class ConfigCommandArgParser(CommandArgParser):

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def parse(self) -> dict:
        if self.command_args[0].upper() == 'VIEW':
            tup = ConfigArgs(view=True, config_key=None, config_value=None)
        else:
            key, value, *misc = self.command_args
            tup = ConfigArgs(view=False, config_key=key, config_value=value)

        return {'command': self.command, 'command_args': tup}
