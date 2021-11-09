from timer_session.timer_session import create_session
from timer_logic.factories.factory_router import command_factory_router

from command_classes.commands import LogCommand
from command_classes.commands import QueryCommand
from command_classes.commands import UtilityCommand
from command_classes.commands import UpdateCommand
from command_classes.commands import ConfigCommand

from .handlers.update_command_handler import UpdateCommandHandler
from .handlers.log_command_handler import LogCommandHandler
from .handlers.query_command_handler import QueryCommandHandler
from .handlers.utility_command_handler import UtilityCommandHandler
from .handlers.config_command_handler import ConfigCommandHandler

from utils.exceptions import HandlerNotFound
from utils.exceptions import TimeSequenceError
from utils.exceptions import CommandSequenceError


def run_mediator(command_dict: dict):
    command_obj = command_factory_router(command_dict)
    try:
        if isinstance(command_obj, LogCommand):
            session = create_session()
            LogCommandHandler(command_obj, session).handle()
        elif isinstance(command_obj, QueryCommand):
            QueryCommandHandler(command_obj).handle()
        elif isinstance(command_obj, UtilityCommand):
            session = create_session()
            UtilityCommandHandler(command_obj, session).handle()
        elif isinstance(command_obj, UpdateCommand):
            # Todo: need a session?
            UpdateCommandHandler(command_obj).handle()
        elif isinstance(command_obj, ConfigCommand):
            ConfigCommandHandler(command_obj).handle()
        else:
            raise HandlerNotFound("Mediator was unable to find a handler for given command.")
    except (TimeSequenceError, CommandSequenceError) as e:
        print(e)
