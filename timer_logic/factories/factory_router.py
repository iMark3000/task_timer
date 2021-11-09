from .log_command_factory import LogCommandFactory
from .query_command_factory import QueryCommandFactory
from .update_command_factory import UpdateCommandFactory
from .utility_command_factory import UtilityCommandFactory
from .config_command_factory import ConfigCommandFactory

from utils.const import LOG_COMMANDS
from utils.const import UTILITY_COMMANDS
from utils.const import QUERY_COMMANDS
from utils.const import UPDATE_COMMANDS
from utils.const import CONFIG_COMMANDS


def command_factory_router(command_dict: dict):
    command = command_dict['command']
    if command in LOG_COMMANDS:
        return LogCommandFactory(command_dict).create_command()
    elif command in QUERY_COMMANDS:
        return QueryCommandFactory(command_dict).create_command()
    elif command in UTILITY_COMMANDS:
        return UtilityCommandFactory(command_dict).create_command()
    elif command in UPDATE_COMMANDS:
        return UpdateCommandFactory(command_dict).create_command()
    elif command in CONFIG_COMMANDS:
        return ConfigCommandFactory(command_dict).create_command()
