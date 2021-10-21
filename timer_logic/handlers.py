from abc import ABC, abstractmethod

from .commands import Command
from timer_session import timer_session
from utils.exceptions import CommandSequenceError
from utils.command_enums import InputType


class Handler(ABC):

    def __init__(self, command: Command):
        self.command = command


class LogCommandHandler(Handler):

    def __init__(self, command: Command, session: timer_session):
        self.session = session
        super().__init__(command)

    @abstractmethod
    def _validate_sequence(self):
        pass

    @abstractmethod
    def _validate_time(self):
        pass

    @abstractmethod
    def process_command(self):
        pass


class StartCommandHandler(LogCommandHandler):

    def _validate_sequence(self):
        if self.session.get_last_action() != InputType.NO_SESSION:
            raise CommandSequenceError(f"Stop current session first before starting new Session")

    def _validate_time(self):



class QueryCommandHandler(Handler):
    pass
