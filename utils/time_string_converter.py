import re
import datetime

from .exceptions import HoursValueError, MinutesValueError, \
    TooManyNumsTimeFormatError, NonNumberTimeFormatError


class TimeStringToDateTimeObj:

    def __init__(self, t: str):
        self.time_str = t.lower()
        self.pm = False
        self.year = None
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.datetime_obj = None
        self._construct_datetime_obj()

    @staticmethod
    def _check_for_pm(s):
        return 'p' in s

    @staticmethod
    def _check_for_colon(s):
        return ':' in s

    def _string_parser(self):
        time = self.time_str
        if self._check_for_pm(time):
            time = time.split('p')[0]
            self.pm = True
            print('pm = true')
        if self._check_for_colon(time):
            self.hour, self.minute = time.split(':')
        else:
            if len(time) == 3:
                self.hour, self.minute = time[0], time[1:]
            else:
                self.hour, self.minute = time[:2], time[2:]

    def _convert_time_str_to_int(self):
        try:
            self.hour = int(self.hour)
            self.minute = int(self.minute)
        except ValueError as err:
            raise NonNumberTimeFormatError("Non-numbers entered for time.")

        if self.pm:  # Todo: Figure hour why the multiple conditions were not working
            if self.hour < 12:
                self.hour += 12

    def _get_todays_date(self) -> None:
        today = datetime.date.today()
        self.year = today.year
        self.month = today.month
        self.day = today.day

    def _construct_datetime_obj(self) -> None:
        self._string_parser()
        self._convert_time_str_to_int()
        self._get_todays_date()

        try:
            self.datetime_obj = datetime.datetime(self.year, self.month, self.day,
                                              hour=self.hour, minute=self.minute)
        except ValueError as err:
            if 59 < self.minute <= 99:
                raise MinutesValueError("There can not be more than 59 minutes in an hour.") from err
            if self.minute > 99:
                raise TooManyNumsTimeFormatError("Too many numbers entered to be an actual time.") from err
            elif self.hour >= 24:
                raise HoursValueError("I wish there were more than 24 hours in a day, but there are not.") from err

    def get_datetime_obj(self) -> datetime:
        return self.datetime_obj
