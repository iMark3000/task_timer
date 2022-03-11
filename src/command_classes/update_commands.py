from src.command_classes.commands_base_class import CommandBaseClass


class UpdateCommand(CommandBaseClass):
    pass


class DeactivateCommand(UpdateCommand):
    """Deactivates project by project ID"""
    pass


class ReactivateCommand(UpdateCommand):
    """Reactivates project by project ID"""
    pass


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


class RenameCommand(UpdateCommand):
    """Takes in a project id and 'name' argument to rename a project"""
    pass
