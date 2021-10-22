from timer_session.timer_session import create_session
from command_factories import command_factory_router
from commands import LogCommand, QueryCommand
from handlers import LogCommandHandler, QueryCommandHandler
from utils.exceptions import HandlerNotFound


def run_mediator(command_dict: dict):
    session = create_session()
    command_obj = command_factory_router(command_dict)
    if isinstance(command_obj, LogCommand):
        LogCommandHandler(command_obj, session)
    elif isinstance(command_obj, QueryCommand):
        QueryCommandHandler(command_obj)
    else:
        raise HandlerNotFound("Mediator was unable to find a handler for given command.")

