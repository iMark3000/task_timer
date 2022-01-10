import datetime

from .exceptions import HoursValueError
from .exceptions import MinutesValueError
from .exceptions import TooManyNumsTimeFormatError
from .exceptions import NonNumberTimeFormatError


class TimeDateStrToDateTimeObj:

    def __init__(self, t: str, date=None):
        self.time_str = t.lower()
        self.date = date
        self.pm = False
        self.date_cont = DateContainer()
        self.datetime_obj = None
        self._construct_datetime_obj()

    @staticmethod
    def _check_for_pm(s):
        return 'p' in s

    @staticmethod
    def _check_for_colon(s):
        return ':' in s

    def _time_string_parser(self):
        time = self.time_str
        if self._check_for_pm(time):
            time = time.split('p')[0]
            self.pm = True
        if self._check_for_colon(time):
            self.date_cont.hour, self.date_cont.minute = time.split(':')
        else:
            if len(time) == 3:
                self.date_cont.hour, self.date_cont.minute = time[0], time[1:]
            else:
                self.date_cont.hour, self.date_cont.minute = time[:2], time[2:]

    def _convert_time_to_int(self):
        self.date_cont.convert_to_int()
        if self.pm:
            if self.date_cont.hour < 12:
                self.date_cont.hour += 12

    def _date_string_parser(self):
        num_date_fields = len(self.date.split('/'))
        if num_date_fields == 3:
            self.date_cont.month, self.date_cont.day, self.date_cont.year = self.date.split('/')
        elif num_date_fields == 2:
            self.date_cont.month, self.date_cont.day = self.date.split('/')
            self.date_cont.year = datetime.date.today().year

    def _get_todays_date(self) -> None:
        today = datetime.date.today()
        self.date_cont.year = today.year
        self.date_cont.month = today.month
        self.date_cont.day = today.day

    def _construct_datetime_obj(self) -> None:
        self._time_string_parser()
        if self.date is None:
            self._get_todays_date()
        else:
            self._date_string_parser()

        self._convert_time_to_int()

        try:
            self.datetime_obj = datetime.datetime(self.date_cont.year,
                                                  self.date_cont.month,
                                                  self.date_cont.day,
                                                  hour=self.date_cont.hour,
                                                  minute=self.date_cont.minute)
        except ValueError as err:
            if 59 < self.date_cont.minute <= 99:
                raise MinutesValueError("There can not be more than 59 minutes in an hour.") from err
            if self.date_cont.minute > 99:
                raise TooManyNumsTimeFormatError("Too many numbers entered to be an actual time.") from err
            elif self.date_cont.hour >= 24:
                raise HoursValueError("I wish there were more than 24 hours in a day, but there are not.") from err

    def get_datetime_obj(self) -> datetime:
        return self.datetime_obj


class DateContainer:

    def __init__(self):
        self._year = None
        self._month = None
        self._day = None
        self._hour = None
        self._minute = None

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value):
        self._month = value

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        self._day = value

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, value):
        self._hour = value

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, value):
        self._minute = value

    def __str__(self):
        return f'M: {self.month} D: {self.day} Y: {self.year}'

    def convert_to_int(self):
        print(self)
        for att in vars(self):
            value = self.__getattribute__(att)
            if isinstance(value, str):
                try:
                    value = int(value)
                    self.__setattr__(att, value)
                except ValueError as e:
                    print(e)
                    raise NonNumberTimeFormatError('Argument Identified as time: Non integers mixed with "/"')