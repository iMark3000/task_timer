from abc import ABC, abstractmethod


class KeywordBaseClass(ABC):

    def __init__(self):
        self._db_field = None
        self._db_table = None
        self._value = None

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def process_value(self):
        pass

class ProjectID:
    pass

class SessionID:
    pass

class LogID:
    pass

class AppendNote:
    pass

class OverWriteNote:
    pass

class DeleteNote:
    pass

class StartTimeDate:
    pass

class EndTimeDate:
    pass
