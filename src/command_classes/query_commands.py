from src.command_classes.commands import Command
from src.utils.command_enums import InputType


class QueryCommand(Command):

    def __init__(self, command: InputType, **kwargs):
        self._query_projects = None
        self._query_level = None
        self._query_time_period = None
        self._start_date = None
        self._end_date = None
        super().__init__(command, **kwargs)

    @property
    def query_projects(self):
        return self._query_projects

    @property
    def query_level(self):
        return self._query_level

    @property
    def query_time_period(self):
        return self._query_time_period

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date