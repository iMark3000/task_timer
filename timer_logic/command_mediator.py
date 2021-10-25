from timer_session.timer_session import create_session
from timer_logic.command_factories import command_factory_router
from timer_logic.commands import LogCommand, QueryCommand, StatusMiscCommand
from timer_logic.command_handlers import LogCommandHandler, QueryCommandHandler, StatusMiscHandler
from utils.exceptions import HandlerNotFound


def run_mediator(command_dict: dict):
    command_obj = command_factory_router(command_dict)
    if isinstance(command_obj, LogCommand):
        session = create_session()
        LogCommandHandler(command_obj, session)
    elif isinstance(command_obj, QueryCommand):
        QueryCommandHandler(command_obj)
    elif isinstance(command_obj, StatusMiscCommand):
        session = create_session()
        StatusMiscHandler(command_obj, session)
    else:
        raise HandlerNotFound("Mediator was unable to find a handler for given command.")
