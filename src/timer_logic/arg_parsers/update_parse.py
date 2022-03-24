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

    def _deactivate(self):
        pass

    def _rename(self):
        if len(self.command_args) != 2:
            raise InvalidArgument('RENAME command takes two args: project id (prefixed with "p=" '
                                  'and a new name in double qoutes')
        for arg in self.command_args:
            if 'p=' in arg:
                try:
                    pid = int(arg.split('=')[-1])
                    self.arg_dict['project_id'] = pid
                except ValueError:
                    raise InvalidArgument('Project id needs to be an integer')
            else:
                self.arg_dict['new_name'] = arg

    def _edit(self):
        pass

    def _merge(self):
        pass

    def parse(self):
        if self.command == InputType.REACTIVATE:
            self._reactivate()
        elif self.command == InputType.RENAME:
            self._rename()
        return super().get_command_tuple()
