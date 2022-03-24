
# Sequence Errors for Commands
class SequenceError(Exception):
    pass


class CommandSequenceError(SequenceError):
    pass


class TimeSequenceError(SequenceError):
    pass


# Time Parse Errors
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


# Errors for command arg handling
class CommandArgError(Exception):
    pass


class NoProjectNameProvided(CommandArgError):
    pass


class UnexpectedNameArgument(CommandArgError):
    pass


class RequiredArgMissing(CommandArgError):
    pass


class InvalidArgument(CommandArgError):
    pass


class TooManyCommandArgs(CommandArgError):
    pass


# Error for Handler
class HandlerNotFound(Exception):
    pass


# MISC
class ConfigurationNotFound(Exception):
    pass


class UnknownPath(Exception):
    pass


class InvalidConfigArgument(Exception):
    pass


class ReportTemplateNotFound(Exception):
    pass