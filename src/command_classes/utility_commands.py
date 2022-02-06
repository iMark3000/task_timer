from src.command_classes.commands_base_class import CommandBaseClass
from src.utils.command_enums import InputType


class UtilityCommand(CommandBaseClass):

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)


class StatusCheck(UtilityCommand):

    def __init__(self, command: InputType, **kwargs):
        self._all = False
        super().__init__(command, **kwargs)

    def is_all(self):
        return self._all


class UtilityProjectsCommands(UtilityCommand):

    def __init__(self, command: InputType, **kwargs):
        self._project_name = None
        super().__init__(command, **kwargs)

    @property
    def project_name(self):
        return self._project_name


class ProjectsCommand(UtilityProjectsCommands):

    def __init__(self, command: InputType, **kwargs):
        self._all = False
        self._filter_by = None
        super().__init__(command, **kwargs)

    def is_all(self):
        return self._all

    @property
    def filter_by(self):
        return self._filter_by


class NewCommand(UtilityProjectsCommands):

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)


class SessionUtilityCommands(UtilityCommand):

    def __init__(self, command: InputType, **kwargs):
        self._project_id = None
        super().__init__(command, **kwargs)

    @property
    def project_id(self):
        return self._project_id


class FetchProject(SessionUtilityCommands):

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)


class SwitchCommand(SessionUtilityCommands):

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)
