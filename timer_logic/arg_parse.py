from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import datetime

from utils.command_enums import InputType
from utils.const import LOG_COMMANDS
from utils.const import QUERY_COMMANDS
from utils.const import STATUS_MISC
from utils.const import VALID_TIME_CHARACTERS
from utils.const import VALID_NAME_CHARACTERS
from utils.time_string_converter import TimeStringToDateTimeObj

from utils.exceptions import RequiredArgMissing
from utils.exceptions import InvalidArgument
from utils.exceptions import TooManyCommandArgs
from utils.exceptions import TimeError



LogArgs = namedtuple("LogArgs", "time name")
QueryArgs = namedtuple("QueryArgs", "args")
StatusMiscArgs = namedtuple("StatusMiscArgs", "project_id")


class CommandArgParser(ABC):

    def __init__(self, command: InputType, command_args: list):
        self.command = command
        self.command_args = command_args

        @abstractmethod
        def parse():
            pass


class LogCommandArgParser(CommandArgParser):

    def __init__(self, command: InputType, command_args: list):
        self.time = None
        self.date = None
        super().__init__(command, command_args)

    def _identify_time(self):
        for arg in self.command_args:
            index = 0
            for c in arg:
                if c not in VALID_TIME_CHARACTERS:
                    break
                else:
                    index += 1
                    if index == len(arg):
                        self.time = arg

    def _identify_date(self):
        for arg in self.command_args:
            if "/" in arg:
                self.date = arg

    def _convert_to_date_time_obj(self):
        if self.time and self.date:
            datetime_obj = TimeStringToDateTimeObj(self.time, self.date).get_datetime_obj()
        elif self.time:
            datetime_obj = TimeStringToDateTimeObj(self.time).get_datetime_obj()
        else:
            datetime_obj = datetime.now()

        return datetime_obj

    def parse(self):
        self._identify_date()
        self._identify_time()
        try:
            time = self._convert_to_date_time_obj()
            tup = LogArgs(name=None, time=time)
            return {'command': self.command, 'command_args': tup}
        except TimeError as e:
            print(e)


class StartCommandArgParser(LogCommandArgParser):

    def __init__(self, command: InputType, command_args: list):
        self.time = None
        self.date = None
        self.project_name = None
        super().__init__(command, command_args)

    def _identify_name(self):
        for arg in self.command_args:
            if self._check_name_chars(arg):
                break

    def _check_name_chars(self, name):
        index = 0
        char_count = 0
        for c in name:
            try:
                index += 1
                if c.lower() in VALID_NAME_CHARACTERS:
                    char_count += 1
                    if char_count == 3:
                        self.project_name = name
                        return True
                    elif index == len(name):
                        return False
            except AttributeError as e:
                # Ignoring non Alpha Characters in Name
                char_count += 1

    def parse(self):
        self._identify_date()
        self._identify_time()
        self._identify_name()
        try:
            time = self._convert_to_date_time_obj()
            tup = LogArgs(name=self.project_name, time=time)
            return {'command': self.command, 'command_args': tup}
        except TimeError as e:
            print(e)


class QueryCommandArgParser(CommandArgParser):
    # Todo: Setup Queries
    pass


class StatusMiscArgParser(CommandArgParser):

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def _fetch_args(self):
        if len(self.command_args) == 0:
            raise RequiredArgMissing('FETCH command needs a project ID argument')
        elif len(self.command_args) >= 2:
            raise TooManyCommandArgs('FETCH command takes one arg: Project ID')
        elif len(self.command_args) == 1:
            try:
                project_id = int(self.command_args[0])
                tup = StatusMiscArgs(project_id=project_id)
                return {'command': self.command, 'command_args': tup}
            except ValueError:
                raise InvalidArgument('Project ID for FETCH command is not an integer')

    def _status_args(self):
        if len(self.command_args) == 0:
            tup = StatusMiscArgs(project_id=None)
            return {'command': self.command, 'command_args': tup}
        else:
            raise TooManyCommandArgs('STATUS Command takes no arguments.')

    def parse(self) -> dict:
        if self.command == InputType.FETCH:
            return self._fetch_args()
        elif self.command == InputType.STATUS:
            return self._status_args()


def arg_router(command: InputType, command_args: list) -> dict:
    if command == InputType.START:
        return StartCommandArgParser(command, command_args).parse()
    elif command in LOG_COMMANDS:
        return LogCommandArgParser(command, command_args).parse()
    elif command in QUERY_COMMANDS:
        # ToDo: Add Query Commands
        pass
    elif command in STATUS_MISC:
        return StatusMiscArgParser(command, command_args).parse()
