from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from math import floor


class Field(ABC):

    def __init__(self):
        # self.WIDTH_PERCENT = width_per
        # self.MIN_WIDTH = min_width
        self._field_width = None

    @property
    def field_width(self) -> int:
        return self._field_width

    def _truncate(self, value: Any) -> str:
        value_str = f'{value}'
        if len(value_str) > self._field_width - 2:
            value_str = value_str[:self._field_width - 5]
            value_str += '...'
        return value_str

    @abstractmethod
    def set_field_width(self, width: int) -> None:
        pass

    @abstractmethod
    def print_field(self, value: Any) -> str:
        pass


class ValueField(Field):

    def __init__(self, width_per, min_width, row_field=True):
        self.WIDTH_PERCENT = width_per
        self.MIN_WIDTH = min_width
        self._row_field = row_field
        super().__init__()

    def set_field_width(self, width: int) -> None:
        if self._row_field:
            if floor(self.WIDTH_PERCENT * width) <= self.MIN_WIDTH:
                self._field_width = self.MIN_WIDTH
            else:
                self._field_width = floor(self.WIDTH_PERCENT * width)
        else:
            # TODO: Is this necessary?
            # Override for non-Row use
            self._field_width = width

    def _as_row(self, value: Any) -> str:
        value = self._truncate(value)
        return '{0:{fill}{align}{length}}'.format(value, fill='', align='^', length=self._field_width)

    def print_field(self, value: Any) -> str:
        if self._row_field:
            return self._as_row(value)
        else:
            return f'{value}'


class ProjectField(ValueField):

    def __init__(self, row_field=True):
        self.WIDTH_PERCENT = .085
        self.MIN_WIDTH = 9
        self._row_field = row_field
        super().__init__(self.WIDTH_PERCENT, self.MIN_WIDTH, row_field=row_field)


class TimeField(ValueField):

    def __init__(self, row_field=True):
        self.WIDTH_PERCENT = .238
        self.MIN_WIDTH = 25
        self._row_field = row_field
        super().__init__(self.WIDTH_PERCENT, self.MIN_WIDTH, row_field=row_field)

    @staticmethod
    def _format_date_time(dt: datetime) -> str:
        return dt.strftime("%m/%d/%Y - %X")

    def print_field(self, value: datetime) -> str:
        value = self._format_date_time(value)
        if self._row_field:
            return self._as_row(value)
        else:
            return f'{value}'


class IDField(ValueField):

    def __init__(self, row_field=True):
        self.WIDTH_PERCENT = .142
        self.MIN_WIDTH = 15
        self._row_field = row_field
        super().__init__(self.WIDTH_PERCENT, self.MIN_WIDTH, row_field=row_field)


class DurationField(ValueField):

    def __init__(self, row_field=True):
        self.WIDTH_PERCENT = .171
        self.MIN_WIDTH = 18
        self._row_field = row_field
        super().__init__(self.WIDTH_PERCENT, self.MIN_WIDTH, row_field=row_field)


class CountField(ValueField):

    def __init__(self, row_field=True):
        self.WIDTH_PERCENT = .104
        self.MIN_WIDTH = 11
        self._row_field = row_field
        super().__init__(self.WIDTH_PERCENT, self.MIN_WIDTH, row_field=row_field)


class AverageField(ValueField):

    def __init__(self, row_field=True):
        self.WIDTH_PERCENT = .123
        self.MIN_WIDTH = 13
        self._row_field = row_field
        super().__init__(self.WIDTH_PERCENT, self.MIN_WIDTH, row_field=row_field)

    @staticmethod
    def _format_float(n: float) -> str:
        return f'{n:.2f}'

    def print_field(self, value: float) -> str:
        value = self._format_float(value)
        if self._row_field:
            return self._as_row(value)
        else:
            return f'{value}'


class PercentField(ValueField):

    def __init__(self, row_field=True):
        self.WIDTH_PERCENT = .133
        self.MIN_WIDTH = 14
        self._row_field = row_field
        super().__init__(self.WIDTH_PERCENT, self.MIN_WIDTH, row_field=row_field)

    @staticmethod
    def _format_percent(p: float) -> str:
        return f'{p:.2}' + ' %'

    def print_field(self, value: float) -> str:
        value = self._format_percent(value)
        if self._row_field:
            return self._as_row(value)
        else:
            return f'{value}'


class NoteField(Field):

    def __init__(self, end_note=False):
        self.end_note = end_note
        super().__init__()

    @property
    def field_width(self) -> int:
        return self._field_width

    def set_field_width(self, width: int) -> None:
        self._field_width = width

    def print_field(self, value: str, padding=None) -> str:
        if self.end_note:
            first_str = '{0:{fill}{align}{length}}'.format('', fill='', align='<', length=padding)
            second_str = '{0:{fill}{align}{length}}'.format(value, fill='', align='<', length=self._field_width)
            return '\n' + first_str + second_str
        else:
            return '{0:{fill}{align}{length}}'.format(value, fill='', align='<', length=self._field_width)
