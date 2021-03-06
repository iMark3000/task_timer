
from .arg_parse_base_class import CommandArgParser

from src.utils.command_enums import InputType
from src.utils.const import VALID_NAME_CHARACTERS
from src.utils.exceptions import InvalidArgument
from src.utils.exceptions import TooManyCommandArgs


class UtilityCommandArgParser(CommandArgParser):

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    @staticmethod
    def _validate_name_char_count(name: str) -> bool:
        """Project Name needs 3 alpha characters to be valid"""
        index = 0
        char_count = 0
        for c in name:
            try:
                index += 1
                if c.lower() in VALID_NAME_CHARACTERS:
                    char_count += 1
                    if char_count == 3:
                        return True
                    elif index == len(name):
                        return False
            except AttributeError as e:
                # Ignoring non Alpha Characters in Name
                index += 1

    def _fetch_args(self):
        try:
            self.arg_dict['project_id'] = int(self.command_args[0])
            return super().get_command_tuple()
        except ValueError:
            raise InvalidArgument('Project ID for FETCH command must be an integer')

    def _status_args(self):
        if len(self.command_args) == 0:
            return super().get_command_tuple()
        else:
            raise TooManyCommandArgs('STATUS Command takes no arguments.')

    def _new_args(self):
        project_name = self.command_args[0]
        if self._validate_name_char_count(project_name):
            self.arg_dict['project_name'] = project_name
            return super().get_command_tuple()
        else:
            raise InvalidArgument('Project Names need a minimum of three alphabetic characters.')

    def _project_args(self):
        if self.command_args:
            if self.command_args[0].upper() == 'ALL':
                self.arg_dict['all'] = True
            elif self.command_args[0].upper() == 'DEACTIVATED':
                self.arg_dict['filter_by'] = 0
        return super().get_command_tuple()

    def _switch_args(self):
        if self.command_args:
            try:
                self.arg_dict['project_id'] = int(self.command_args[0])
                return super().get_command_tuple()
            except ValueError:
                print('SWITCH needs an integer for Project ID.')
        else:
            raise InvalidArgument('SWITCH requires one argument: Project ID')

    def _remove_args(self):
        if self.command_args:
            try:
                self.arg_dict['project_id'] = int(self.command_args[0])
                return super().get_command_tuple()
            except ValueError:
                print('REMOVE needs an integer for Project ID.')
        else:
            raise InvalidArgument('REMOVE requires one argument: Project ID')

    def parse(self) -> tuple:
        if self.command == InputType.STATUS:
            return self._status_args()
        elif self.command == InputType.FETCH:
            return self._fetch_args()
        elif self.command == InputType.NEW:
            return self._new_args()
        elif self.command == InputType.PROJECTS:
            return self._project_args()
        elif self.command == InputType.SWITCH:
            return self._switch_args()
        elif self.command == InputType.REMOVE:
            return self._remove_args()
