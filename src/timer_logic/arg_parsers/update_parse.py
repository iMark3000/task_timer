from .arg_parse_base_class import CommandArgParser
from src.utils.command_enums import InputType
from src.utils.exceptions import InvalidArgument
from src.utils.exceptions import RequiredArgMissing


class UpdateCommandArgParser(CommandArgParser):
    # Todo: Setup Update

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def _reactivate_and_deactivate(self):
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
            raise InvalidArgument('RENAME command takes two args: project id (with a "p=" flag'
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

        if 'project_id' not in self.arg_dict:
            raise RequiredArgMissing('Rename command needs project id with a "p=" flag; ex. p=1')

    def _edit(self):
        pass

    def _merge(self):
        pass
        """
        Parses the following:
            merge_to: int if existing project, str for name of new project
            new_project: bool, default to False; True is "name=" argument is used
            absorbed: list[int] project IDs that will be absorbed into the "merge_to" project
        """
        self.arg_dict['new_project'] = False
        for index, arg in enumerate(self.command_args):
            if 'name=' in arg:
                self.arg_dict['merge_to'] = self.command_args.pop(index).split('=')[1]
                self.arg_dict['new_project'] = True
                break

        if not self.arg_dict['new_project']:
            if len(self.command_args) > 1:
                try:
                    self.arg_dict['merge_to'] = int(self.command_args.pop(0))
                    self.arg_dict['absorbed'] = [int(x) for x in self.command_args]
                except ValueError:
                    raise InvalidArgument('MERGE command needs project ids as integers. '
                                          'If looking to merge to a new project, use "name=" argument')
            else:
                raise RequiredArgMissing('Merge needs at least two project ids')
        else:
            if len(self.command_args) == 1:
                raise RequiredArgMissing('Merge needs at least two project ids. '
                                         'If using one project id with the "name=" argument, '
                                         'then you may want to use the RENAME command')
            else:
                try:
                    self.arg_dict['absorbed'] = [int(x) for x in self.command_args]
                except ValueError:
                    raise InvalidArgument('Non-integers detected. MERGE command needs project ids as integers.')

    def parse(self):
        if self.command == InputType.REACTIVATE:
            self._reactivate_and_deactivate()
        elif self.command == InputType.DEACTIVATE:
            self._reactivate_and_deactivate()
        elif self.command == InputType.RENAME:
            self._rename()
        elif self.command == InputType.MERGE:
            self._merge()
        return super().get_command_tuple()
