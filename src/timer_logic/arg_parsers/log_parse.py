from datetime import datetime

from .arg_parse_base_class import CommandArgParser

from src.utils.command_enums import InputType
from src.utils.const import VALID_TIME_CHARACTERS
from src.utils.const import VALID_NAME_CHARACTERS
from src.utils.time_string_converter import TimeDateStrToDateTimeObj

from src.utils.exceptions import TimeError


class LogCommandArgParser(CommandArgParser):

    def __init__(self, command: InputType, command_args: list):
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
        """Iterates through arguments from CLI looking for an arg containing '/' """
        for index, arg in enumerate(self.command_args):
            if '/' in arg:
                return index
            elif index + 1 == len(self.command_args):
                return None

    @staticmethod
    def _convert_to_date_time_obj(date, time):
        if time and date:
            datetime_obj = TimeDateStrToDateTimeObj(time, date).get_datetime_obj()
        elif time:
            datetime_obj = TimeDateStrToDateTimeObj(time).get_datetime_obj()
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

    def _handle_date_time(self):
        """Call functions to identify dates and times and passes them to func to create datetime object"""
        date = self._identify_date()
        if date is not None:
            date = self.command_args.pop(date)

        time = self._identify_time()
        if time is not None:
            time = self.command_args.pop(time)
        try:
            return self._convert_to_date_time_obj(date, time)
        except TimeError as e:
            print(e)

    def parse(self) -> tuple:
        self.arg_dict['time'] = self._handle_date_time()
        log_note = self._parse_log_note()
        if log_note is not None:
            self.arg_dict['log_note'] = log_note
        return super().get_command_tuple()


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

    def parse(self) -> tuple:
        self.arg_dict['time'] = self._compute_date_time()

        session_note = self._parse_session_note()
        if session_note is not None:
            self.arg_dict['session_note'] = session_note
        log_note = self._parse_log_note()
        if log_note is not None:
            self.arg_dict['log_note'] = log_note
        return super().get_command_tuple()

