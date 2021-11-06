
from .log_parse import LogCommandArgParser
from .log_parse import StartCommandArgParser
from .query_parse import QueryCommandArgParser
from .utility_parse import UtilityCommandArgParser
from .update_parse import UpdateCommandArgParser

from utils.command_enums import InputType
from utils.const import LOG_COMMANDS
from utils.const import QUERY_COMMANDS
from utils.const import UTILITY_COMMANDS
from utils.const import UPDATE_COMMANDS


def arg_router(command: InputType, command_args: list) -> dict:
    if command == InputType.START:
        return StartCommandArgParser(command, command_args).parse()
    elif command in LOG_COMMANDS:
        return LogCommandArgParser(command, command_args).parse()
    elif command in QUERY_COMMANDS:
        return QueryCommandArgParser(command, command_args).parse()
    elif command in UTILITY_COMMANDS:
        return UtilityCommandArgParser(command, command_args).parse()
    elif command in UPDATE_COMMANDS:
        return UpdateCommandArgParser(command, command_args).parse()
