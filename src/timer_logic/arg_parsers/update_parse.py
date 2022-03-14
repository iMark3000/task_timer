from .arg_parse_base_class import CommandArgParser
from src.utils.command_enums import InputType
from src.utils.exceptions import InvalidArgument


class UpdateCommandArgParser(CommandArgParser):
    # Todo: Setup Update

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def _reactivate(self):
        if len(self.command_args) != 1:
            raise InvalidArgument('Reactivate Command only takes one argument.')
        try:
            self.arg_dict['project_id'] = int(self.command_args[0])
            return super().get_command_tuple()
        except ValueError:
            raise InvalidArgument('Project ID for Reactivate must be an integer')

    def parse(self):
        if self.command == InputType.REACTIVATE:
            self._reactivate()
