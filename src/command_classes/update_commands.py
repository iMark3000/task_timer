from src.command_classes.commands_base_class import CommandBaseClass
from src.utils.command_enums import InputType


class UpdateCommand(CommandBaseClass):

    def __init__(self, command: InputType, **kwargs):
        self._project_id = None
        super().__init__(command, **kwargs)

    @property
    def project_id(self):
        return self._project_id


class DeactivateCommand(UpdateCommand):
    """Deactivates project by project ID"""

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)


class ReactivateCommand(UpdateCommand):
    """Reactivates project by project ID"""

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)


class RenameCommand(UpdateCommand):
    """Takes in a project id and 'name' argument to rename a project"""

    def __init__(self, command: InputType, **kwargs):
        super().__init__(command, **kwargs)


class EditCommand(UpdateCommand):
    pass


class MergeCommand(UpdateCommand):
    """Merges two or more projects into one. Optional argument 'name'

    Input list of two or more project ids separated by spaces. If the optional 'name' argument is not provided, then
    the first project listed will absorb all of the sessions and logs of the other projects listed. Those projects
    will then be deactivated.

    If the 'name' argument is included, then a new project is created and all the sessions and logs of the listed
    projects will be moved to that new project. All listed projects will be deactivated.

    """
    pass
