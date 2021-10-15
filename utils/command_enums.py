from enum import Enum, auto


class InputType(Enum):
    START = auto()
    PAUSE = auto()
    RESUME = auto()
    STOP = auto()
    STATUS = auto()
    NEW = auto()
    PROJECTS = auto()
    MERGE = auto()
    LOG = auto()
    REPORT = auto()
    NO_SESSION = auto()
