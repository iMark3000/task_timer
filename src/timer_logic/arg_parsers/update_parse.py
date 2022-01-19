
from .arg_parse_base_class import CommandArgParser
from utils.command_enums import InputType


class UpdateCommandArgParser(CommandArgParser):
    # Todo: Setup Update

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def parse(self):
        print('Not Se up Yet')
