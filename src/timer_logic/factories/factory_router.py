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
from utils.command_enums import InputType


def command_factory_router(command_args: tuple):
    command: InputType = command_args[0]
    command_args: dict = command_args[1]
    if command in LOG_COMMANDS:
        return LogCommandFactory(command, command_args).create_command()
    elif command in QUERY_COMMANDS:
        return QueryCommandFactory(command, command_args).create_command()
    elif command in UTILITY_COMMANDS:
        return UtilityCommandFactory(command, command_args).create_command()
    elif command in UPDATE_COMMANDS:
        return UpdateCommandFactory(command, command_args).create_command()
    elif command in CONFIG_COMMANDS:
        return ConfigCommandFactory(command, command_args).create_command()
