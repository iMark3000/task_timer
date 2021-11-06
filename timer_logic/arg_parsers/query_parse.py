from collections import namedtuple
from datetime import datetime

from .parse_base_class import CommandArgParser
from utils.command_enums import InputType

QueryArgs = namedtuple("QueryArgs", "args")


class QueryCommandArgParser(CommandArgParser):
    # Todo: Setup Queries
    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def parse(self):
        print('Not Se up Yet')
