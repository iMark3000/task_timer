from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import datetime

from utils.command_enums import InputType
from utils.const import LOG_COMMANDS
from utils.const import QUERY_COMMANDS
from utils.const import UTILITY_COMMANDS
from utils.const import VALID_TIME_CHARACTERS
from utils.const import VALID_NAME_CHARACTERS
from utils.time_string_converter import TimeDateStrToDateTimeObj

from utils.exceptions import RequiredArgMissing
from utils.exceptions import InvalidArgument
from utils.exceptions import TooManyCommandArgs
from utils.exceptions import TimeError

LogArgs = namedtuple("LogArgs", "time name log_note session_note")
QueryArgs = namedtuple("QueryArgs", "args")
UtilityArgs = namedtuple("StatusMiscArgs", "project_id project_name")


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
        self.log_note = None
        super().__init__(command, command_args)

    def _identify_time(self):
        for index, arg in enumerate(self.command_args):
            if self._check_timer_chars(arg):
                return index
            elif index + 1 == len(self.command_args):
                return None

    @staticmethod
    def _check_timer_chars(arg):
        char_index = 0
        for c in arg:
            if c not in VALID_TIME_CHARACTERS:
                return False
            else:
                char_index += 1
                if char_index == len(arg):
                    return True

    def _identify_date(self):
        for index, arg in enumerate(self.command_args):
            if "/" in arg:
                return index
            elif index + 1 == len(self.command_args):
                return None

    def _convert_to_date_time_obj(self):
        if self.time and self.date:
            datetime_obj = TimeDateStrToDateTimeObj(self.time, self.date).get_datetime_obj()
        elif self.time:
            datetime_obj = TimeDateStrToDateTimeObj(self.time).get_datetime_obj()
        else:
            datetime_obj = datetime.now()

        return datetime_obj

    def _identify_log_note_sub_list(self):
        for index, arg in enumerate(self.command_args):
            if 'ln=' in arg:
                return index
            elif index + 1 == len(self.command_args):
                return None

    def _parse_log_note(self):
        start = self._identify_log_note_sub_list()
        if start is not None:
            note = list()
            note.append(self.command_args[start].split('=')[1])
            note.extend(self.command_args[start + 1:])
            note = ' '.join(note)
            return note
        else:
            return None

    def parse(self):
        date = self._identify_date()
        if date is not None:
            self.date = self.command_args.pop(date)
        else:
            self.date = date

        time_arg = self._identify_time()
        if time_arg is not None:
            self.time = self.command_args.pop(time_arg)

        self.log_note = self._parse_log_note()
        try:
            time = self._convert_to_date_time_obj()
            tup = LogArgs(name=None, time=time, log_note=self.log_note, session_note=None)
            return {'command': self.command, 'command_args': tup}
        except TimeError as e:
            print(e)


class StartCommandArgParser(LogCommandArgParser):

    def __init__(self, command: InputType, command_args: list):
        self.time = None
        self.date = None
        self.project_name = None
        self.log_note = None
        self.session_note = None
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
                index += 1

    def _identify_session_note_start(self):
        for index, arg in enumerate(self.command_args):
            if 'sn=' in arg:
                return index
            elif index + 1 == len(self.command_args):
                return None

    def _identify_session_note_end(self):
        for index, arg in enumerate(self.command_args):
            if 'ln=' in arg:
                return index
            elif index + 1 == len(self.command_args):
                return None

    def _parse_session_note(self):
        start = self._identify_session_note_start()
        end = self._identify_session_note_end()
        if start is not None:
            note = list()
            note.append(self.command_args[start].split('=')[1])
            if end is not None:
                note.extend(self.command_args[start + 1: end])
            else:
                note.extend(self.command_args[start + 1:])
            note = ' '.join(note)
            return note
        else:
            return None

    def parse(self):
        date = self._identify_date()
        if date is not None:
            self.date = self.command_args.pop(date)
        else:
            self.date = date

        time_arg = self._identify_time()
        if time_arg is not None:
            self.time = self.command_args.pop(time_arg)

        self.session_note = self._parse_session_note()
        self.log_note = self._parse_log_note()
        try:
            time = self._convert_to_date_time_obj()
            tup = LogArgs(name=self.project_name, time=time,
                          log_note=self.log_note, session_note=self.session_note)
            return {'command': self.command, 'command_args': tup}
        except TimeError as e:
            print(e)


class QueryCommandArgParser(CommandArgParser):
    # Todo: Setup Queries
    pass


class UtilityCommandArgParser(CommandArgParser):
    utility_command_dict = {
        'FETCH': ['Project ID', 'self._fetch_args'],
        'NEW': ['Project Name', 'self._new_args'],
    }

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def _validate_number_of_args(self):
        if len(self.command_args) == 0:
            raise RequiredArgMissing(f'{self.command.name} command requires one argument: '
                                     f'{self.utility_command_dict[self.command.name][0]}')
        elif len(self.command_args) >= 2:
            raise TooManyCommandArgs(f'{self.command.name} command takes only one argument: '
                                     f'{self.utility_command_dict[self.command.name][0]}')
        elif len(self.command_args) == 1:
            if self.command == InputType.FETCH:
                return self._fetch_args()
            elif self.command == InputType.NEW:
                return self._new_args()

    @staticmethod
    def _validate_name_char_count(name: str) -> bool:
        """Project Name needs 3 alpha characters to be valid"""
        index = 0
        char_count = 0
        for c in name:
            try:
                index += 1
                if c.lower() in VALID_NAME_CHARACTERS:
                    char_count += 1
                    if char_count == 3:
                        return True
                    elif index == len(name):
                        return False
            except AttributeError as e:
                # Ignoring non Alpha Characters in Name
                index += 1

    def _fetch_args(self):
        try:
            project_id = int(self.command_args[0])
            tup = UtilityArgs(project_id=project_id, project_name=None)
            return {'command': self.command, 'command_args': tup}
        except ValueError:
            raise InvalidArgument('Project ID for FETCH command is not an integer')

    def _status_args(self):
        if len(self.command_args) == 0:
            tup = UtilityArgs(project_id=None, project_name=None)
            return {'command': self.command, 'command_args': tup}
        else:
            raise TooManyCommandArgs('STATUS Command takes no arguments.')

    def _new_args(self):
        project_name = self.command_args[0]
        if self._validate_name_char_count(project_name):
            tup = UtilityArgs(project_id=None, project_name=project_name)
            return {'command': self.command, 'command_args': tup}
        else:
            raise InvalidArgument('Project Names need a minimum of three alphabetic characters.')

    def parse(self) -> dict:
        if self.command != InputType.STATUS:
            return self._validate_number_of_args()
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
    elif command in UTILITY_COMMANDS:
        return UtilityCommandArgParser(command, command_args).parse()
