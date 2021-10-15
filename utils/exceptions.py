
class CommandSequenceError(Exception):
    pass


class InvalidArgument(Exception):
    pass


class TimeError(Exception):
    pass


class HoursValueError(TimeError):
    pass


class MinutesValueError(TimeError):
    pass


class TooManyNumsTimeFormatError(TimeError):
    pass


class NonNumberTimeFormatError(TimeError):
    pass
