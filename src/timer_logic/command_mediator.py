from src.timer_session.sessions_manager import start_manager
from src.timer_logic.factories.factory_router import command_factory_router

from ..command_classes.log_commands import LogCommand
from ..command_classes.query_commands import QueryCommand
from ..command_classes.utility_commands import UtilityCommand
from ..command_classes.update_commands import UpdateCommand
from ..command_classes.config_commands import ConfigCommand

from .handlers.update_command_handler import UpdateCommandHandler
from .handlers.log_command_handler import LogCommandHandler
from .handlers.query_command_handler import QueryCommandHandler
from .handlers.utility_command_handler import UtilityCommandHandler
from .handlers.config_command_handler import ConfigCommandHandler

from src.utils.exceptions import HandlerNotFound
from src.utils.exceptions import TimeSequenceError
from src.utils.exceptions import CommandSequenceError


def run_mediator(command_args: tuple):
    command_obj = command_factory_router(command_args)
    try:
        if isinstance(command_obj, LogCommand):
            session_manager = start_manager()
            LogCommandHandler(session_manager).handle(command_obj)
        elif isinstance(command_obj, QueryCommand):
            QueryCommandHandler().handle(command_obj)
        elif isinstance(command_obj, UtilityCommand):
            session_manager = start_manager()
            UtilityCommandHandler(session_manager).handle(command_obj)
        elif isinstance(command_obj, UpdateCommand):
            # TODO: SET THIS UP
            UpdateCommandHandler(command_obj).handle()
        elif isinstance(command_obj, ConfigCommand):
            ConfigCommandHandler().handle(command_obj)
        else:
            raise HandlerNotFound("Mediator was unable to find a handler for given command.")
    except (TimeSequenceError, CommandSequenceError) as e:
        print(e)
