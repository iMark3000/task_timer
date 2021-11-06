from timer_session.timer_session import create_session
from timer_logic.factories.factory_router import command_factory_router
from command_classes.commands import LogCommand
from command_classes.commands import QueryCommand
from command_classes.commands import UtilityCommand
from command_classes.commands import UpdateCommand
from timer_logic.handlers.command_handlers import LogCommandHandler
from timer_logic.handlers.command_handlers import QueryCommandHandler
from timer_logic.handlers.command_handlers import UtilityCommandHandler
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
        else:
            raise HandlerNotFound("Mediator was unable to find a handler for given command.")
    except (TimeSequenceError, CommandSequenceError) as e:
        print(e)
