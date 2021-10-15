import datetime
from collections import namedtuple
from typing import Union

TimeEntry = namedtuple("TimeEntry", "start stop")  # Todo: Remove? Is this going to get used?


class TimeLogStack:

    """ Imports times from json file, turns them in to datetime objects

    These datetime objects are stored to use for displaying current session; are part of calculating reports;
    and are used for updating the database.
     """

    INITIAL_CAP = 10

    def __init__(self, tms=None) -> None:
        self._capacity = TimeLogStack.INITIAL_CAP  # Stack capacity
        self._data = [None] * self._capacity  # Stack data
        self._size = 0  # Stack Size
        self._top = 0  # Top Element
        if tms:
            self._load_times(tms)

    def _load_times(self, tms: list) -> None:
        """ Called by __init__ if time_log exists in json.
        Creates named tuple of times"""
        for t in tms:
            self._size_check()
            if len(t) == 2:
                start = DateTimeCreator(t[0])
                end = DateTimeCreator(t[1])
                entry = [start.get_dt_obj(), end.get_dt_obj()]
            else:
                start = DateTimeCreator(t[0])
                entry = [start.get_dt_obj()]

            self._data[self._top] = entry
            self._size += 1
            self._top += 1  # TODO: Sort these variables out

    def add_time(self, tm) -> None:
        if isinstance(tm, str):
            tm = DateTimeCreator(tm)
            self._add_time_to_log(tm.get_dt_obj())
        else:
            self._add_time_to_log(tm)

    def _add_time_to_log(self, log: datetime) -> None:
        self._size_check()
        if len(self._data[self._top - 1]) == 1:
            self._data[self._top - 1].append(log)
        else:
            self._data[self._top] = [log]
            self._size += 1
            self._top += 1

    def get_session_start_time(self) -> datetime:
        return self._data[0][0]

    def get_last_action_time(self) -> datetime:
        entry = self._data[self._top - 1]
        if len(entry) == 1:
            return entry[0]
        else:
            return entry[1]

    def get_stack_data(self) -> Union[list, None]:
        return [self._data[x] for x in range(self._size)]

    def __len__(self):
        return self._size

    def _size_check(self) -> None:
        if self._size == len(self._data):
            self._resize(self._capacity * 2)

    def _resize(self, cap):
        old = self._data
        self._data = [None] * cap
        for i in range(self._size):  # Need to test this loop
            self._data[i] = old[i]


class DateTimeCreator:

    def __init__(self, dt: str):
        self.dt = dt
        self.obj = self._create_datetime_obj()

    def _create_datetime_obj(self) -> datetime:
        d, t = self.dt.split("_")
        day = self._parse_date_string(d)
        tm = self._parse_time_string(t)
        return datetime.datetime(day[2], day[0], day[1], hour=tm[0], minute=tm[1], second=tm[2])

    @staticmethod
    def _parse_date_string(d: str) -> list:
        d = d.split("/")
        return [int(x) for x in d]

    @staticmethod
    def _parse_time_string(t: str) -> list:
        t = t.split(":")
        return [int(x) for x in t]

    def get_dt_obj(self) -> datetime:
        return self.obj
