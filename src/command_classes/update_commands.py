from src.command_classes.commands import Command


class UpdateCommand(Command):
    pass


class DeactivateCommand(UpdateCommand):
    pass


class ReactivateCommand(UpdateCommand):
    pass


class EditCommand(UpdateCommand):
    pass


class MergeCommand(UpdateCommand):
    pass


class RenameCommand(UpdateCommand):
    pass