

class Field:

    def __init__(self):
        self.WIDTH_PERCENT = None
        self.MIN_WIDTH = None
        self._field_width = None

    @property
    def field_width(self):
        return self._field_width

    def set_field_width(self, width):
        if self.WIDTH_PERCENT * width <= self.MIN_WIDTH:
            self._field_width = self.MIN_WIDTH
        else:
            self._field_width = self.WIDTH_PERCENT * width

    def print_field(self, value):
        return '{0:{fill}{align}{length}}'.format(value, fill='', align='^', length=self._field_width)


class ProjectField:

    MIN_WIDTH = 15
    WIDTH_PERCENT = .20

    def __init__(self):
        self.WIDTH_PERCENT = None
        self.MIN_WIDTH = None
        self._field_width = None

    @property
    def field_width(self):
        return self._field_width

    def set_field_width(self, width):
        if self.WIDTH_PERCENT * width <= self.MIN_WIDTH:
            self._field_width = self.MIN_WIDTH
        else:
            self._field_width = self.WIDTH_PERCENT * width

    def print_field(self, value):
        return '{0:{fill}{align}{length}}'.format(value, fill='', align='^', length=self._field_width)


class TimeField:
    MIN_WIDTH = 25
    WIDTH_PERCENT = .33

    def __init__(self):
        self.WIDTH_PERCENT = None
        self.MIN_WIDTH = None
        self._field_width = None

    @property
    def field_width(self):
        return self._field_width

    def set_field_width(self, width):
        if self.WIDTH_PERCENT * width <= self.MIN_WIDTH:
            self._field_width = self.MIN_WIDTH
        else:
            self._field_width = self.WIDTH_PERCENT * width

    def print_field(self, value):
        return '{0:{fill}{align}{length}}'.format(value, fill='', align='^', length=self._field_width)


class IDField:
    MIN_WIDTH = 10
    WIDTH_PERCENT = .15

    def __init__(self):
        self.WIDTH_PERCENT = None
        self.MIN_WIDTH = None
        self._field_width = None

    @property
    def field_width(self):
        return self._field_width

    def set_field_width(self, width):
        if self.WIDTH_PERCENT * width <= self.MIN_WIDTH:
            self._field_width = self.MIN_WIDTH
        else:
            self._field_width = self.WIDTH_PERCENT * width

    def print_field(self, value):
        return '{0:{fill}{align}{length}}'.format(value, fill='', align='^', length=self._field_width)


class DurationField:
    pass


class CountField:
    pass


class AverageField:
    pass


class PercentField:
    pass


class NoteField:

    def __init__(self, end_note=False):
        self._field_width = 0
        self.end_note = end_note

    @property
    def field_width(self):
        return self._field_width

    def set_field_width(self, width):
        self._field_width = width

    def print_field(self, value, padding=None):
        if self.end_note:
            first_str = '{0:{fill}{align}{length}}'.format('\\s', fill='', align='<', length=padding)
            second_str = '{0:{fill}{align}{length}}'.format(value, fill='', align='<', length=self._field_width)
            return '\n' + first_str + second_str
        else:
            return '{0:{fill}{align}{length}}'.format(value, fill='', align='<', length=self._field_width)
