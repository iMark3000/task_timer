from .log_command_factory import LogCommandFactory
from .query_command_factory import QueryCommandFactory
from .update_command_factory import UpdateCommandFactory
from .utility_command_factory import UtilityCommandFactory

from utils.const import LOG_COMMANDS
from utils.const import UTILITY_COMMANDS
from utils.const import QUERY_COMMANDS
from utils.const import UPDATE_COMMANDS


def command_factory_router(command_dict: dict):
    command = command_dict['command']
    if command in LOG_COMMANDS:
        command_obj = LogCommandFactory(command_dict).create_command()
        return command_obj
    elif command in QUERY_COMMANDS:
        command_obj = QueryCommandFactory(command_dict).create_command()
        return command_obj
    elif command in UTILITY_COMMANDS:
        command_obj = UtilityCommandFactory(command_dict).create_command()
        return command_obj
    elif command in UPDATE_COMMANDS:
        command_obj = UpdateCommandFactory(command_dict).create_command()
        return command_obj
