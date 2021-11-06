from collections import namedtuple

from .arg_parse_base_class import CommandArgParser

from utils.command_enums import InputType
from utils.const import VALID_NAME_CHARACTERS
from utils.exceptions import RequiredArgMissing
from utils.exceptions import InvalidArgument
from utils.exceptions import TooManyCommandArgs

UtilityArgs = namedtuple("StatusMiscArgs", "project_id project_name")


class UtilityCommandArgParser(CommandArgParser):
    utility_command_dict = {
        'FETCH': ['Project ID', 'self._fetch_args'],
        'NEW': ['Project Name', 'self._new_args'],
    }

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def _validate_number_of_args(self):
        if len(self.command_args) == 0:
            raise RequiredArgMissing(f'{self.command.name} command requires one argument: '
                                     f'{self.utility_command_dict[self.command.name][0]}')
        elif len(self.command_args) >= 2:
            raise TooManyCommandArgs(f'{self.command.name} command takes only one argument: '
                                     f'{self.utility_command_dict[self.command.name][0]}')
        elif len(self.command_args) == 1:
            if self.command == InputType.FETCH:
                return self._fetch_args()
            elif self.command == InputType.NEW:
                return self._new_args()

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
            project_id = int(self.command_args[0])
            tup = UtilityArgs(project_id=project_id, project_name=None)
            return {'command': self.command, 'command_args': tup}
        except ValueError:
            raise InvalidArgument('Project ID for FETCH command is not an integer')

    def _status_args(self):
        if len(self.command_args) == 0:
            tup = UtilityArgs(project_id=None, project_name=None)
            return {'command': self.command, 'command_args': tup}
        else:
            raise TooManyCommandArgs('STATUS Command takes no arguments.')

    def _new_args(self):
        project_name = self.command_args[0]
        if self._validate_name_char_count(project_name):
            tup = UtilityArgs(project_id=None, project_name=project_name)
            return {'command': self.command, 'command_args': tup}
        else:
            raise InvalidArgument('Project Names need a minimum of three alphabetic characters.')

    def parse(self) -> dict:
        if self.command != InputType.STATUS:
            return self._validate_number_of_args()
        elif self.command == InputType.STATUS:
            return self._status_args()
