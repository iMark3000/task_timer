from collections import namedtuple

from .arg_parse_base_class import CommandArgParser
from utils.command_enums import InputType
from utils.exceptions import InvalidArgument

QUERY_PARAMS = {
    'd': 'query_time_period',
    'p': 'query_projects',
    '+l': 2,
    '+s': 1,
    '+p': 0,
    }


class QueryCommandArgParser(CommandArgParser):

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def _identify_query_params(self):
        for index, arg in enumerate(self.command_args):
            if arg.lower() == '+chron':
                _ = self.command_args.pop(index)
                self._set_chron()
                return True
            elif "=" in arg:
                self._set_variable_param(self.command_args.pop(index))
                return True
            elif "+" in arg:
                self._set_query_level(self.command_args.pop(index))
                return True
        return False

    def _set_chron(self):
        self.arg_dict['chron'] = True

    def _set_variable_param(self, arg):
        param, param_value = arg.split('=')
        if param_value == '':
            param_value = '0'
        try:
            param_name = QUERY_PARAMS[param.lower()]
            self.arg_dict[param_name] = param_value
        except KeyError:
            raise InvalidArgument(f'{param} is not a valid Query parameter')

    def _set_query_level(self, arg):
        if 'query_level' in self.arg_dict.keys():
            if self.arg_dict['query_level'] < QUERY_PARAMS[arg]:
                self.arg_dict['query_level'] = QUERY_PARAMS[arg]
        else:
            self.arg_dict['query_level'] = QUERY_PARAMS[arg]

    def _no_params(self):
        self.arg_dict['query_time_period'] = '0'
        self.arg_dict['query_projects'] = '0'
        self.arg_dict['query_level'] = 2

    def parse(self):
        if len(self.command_args) != 0:
            param_search = True
            while param_search:
                param_search = self._identify_query_params()
        else:
            self._no_params()
        return super().get_command_tuple()
