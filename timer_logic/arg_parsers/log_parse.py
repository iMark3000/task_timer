from collections import namedtuple
from datetime import datetime

from .parse_base_class import CommandArgParser

from utils.command_enums import InputType
from utils.const import VALID_TIME_CHARACTERS
from utils.const import VALID_NAME_CHARACTERS
from utils.time_string_converter import TimeDateStrToDateTimeObj

from utils.exceptions import TimeError

LogArgs = namedtuple("LogArgs", "time name log_note session_note")


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

