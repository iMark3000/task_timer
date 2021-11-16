from datetime import datetime
from typing import Union


class DateTimeConverter:

    """
    JSON does not store Python datetime objects. Time is stored in JSON as %x_%X

    %x is the date
    %X is the time
    _ is the delimiter

    This class will convert a datetime object to this string format using strpftime() method
    and will convert strings in this format back to a datetime object.
    """

    def __init__(self, dt: Union[str, datetime]):
        if isinstance(dt, str):
            self.date_string = dt
            self.date_obj = self._convert_str_to_datetime_obj(dt)
        elif isinstance(dt, datetime):
            self.date_obj = dt
            self.date_string = self._convert_datetime_to_str(dt)

    def _convert_str_to_datetime_obj(self, dt) -> datetime:
        d, t = dt.split("_")
        day = self._parse_date_string(d)
        tm = self._parse_time_string(t)
        return datetime(day[2], day[0], day[1], hour=tm[0], minute=tm[1], second=tm[2])

    @staticmethod
    def _parse_date_string(d: str) -> list:
        d = d.split("/")
        return [int(x) for x in d]

    @staticmethod
    def _parse_time_string(t: str) -> list:
        t = t.split(":")
        return [int(x) for x in t]

    @staticmethod
    def _convert_datetime_to_str(dt: datetime) -> str:
        return dt.strftime("%m/%d/%Y_%X")

    def get_datetime_obj(self) -> datetime:
        return self.date_obj

    def get_datetime_str(self) -> str:
        return self.date_string
