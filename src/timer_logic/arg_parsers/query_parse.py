import datetime

from .arg_parse_base_class import CommandArgParser
from src.utils.command_enums import InputType
from src.utils.exceptions import InvalidArgument

QUERY_PARAMS = {
    'd': 'query_time_period',
    'p': 'query_projects',
    's': 'start_date',
    'e': 'end_date',
    '+l': 1,    # Log Level Report
    '+s': 2,    # Session Level Report
    '+p': 3,    # Project Level
    }

NON_INT_TIME_PERIOD_INPUT = ['W', 'M', 'Y', 'CY', 'AT']


class QueryCommandArgParser(CommandArgParser):

    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def _identify_query_args(self):
        """Starting point from parse() function;
        Routes arguments to appropriate function for parsing"""
        for index, arg in enumerate(self.command_args):
            if "=" in arg:
                self._set_time_project_params(self.command_args.pop(index))
                return True
            elif "+" in arg:
                self._set_report_level_param(self.command_args.pop(index))
                return True
        return False

    def _set_time_project_params(self, arg):
        """Sets query_time_period and query_projects params if argument is provided"""
        param, param_value = arg.split('=')
        if param_value == '':
            param_value = '0'
        try:
            param_name = QUERY_PARAMS[param.lower()]
            self.arg_dict[param_name] = param_value
        except KeyError:
            print(f'\n FYI: {param} is not a valid Query argument')
            pass

    def _set_report_level_param(self, arg):
        """Maps the '+' argument to the appropriate report level param; Also handles multiple '+' arguments - will
        defer to the lowest level provided"""
        if 'query_level' in self.arg_dict.keys():
            # Handling multiple '+' arguments
            if self.arg_dict['query_level'] > QUERY_PARAMS[arg]:
                self.arg_dict['query_level'] = QUERY_PARAMS[arg]
        else:
            self.arg_dict['query_level'] = QUERY_PARAMS[arg]

    def _eval_start_end_args(self):
        """Handles start and end dates if provided"""
        if 'start_date' in self.arg_dict.keys():
            self.arg_dict["start_date"] = date_string_parser(self.arg_dict["start_date"])
        if 'end_date' in self.arg_dict.keys():
            self.arg_dict["end_date"] = date_string_parser(self.arg_dict["end_date"])

    def _eval_day_arg(self):
        """Evaluates 'd=' argument; Defaults to 'W' if argument not provided"""
        if 'query_time_period' in self.arg_dict.keys():
            if self.arg_dict['query_time_period'].upper() not in NON_INT_TIME_PERIOD_INPUT:
                try:
                    self.arg_dict['query_time_period'] = int(self.arg_dict['query_time_period'])
                except ValueError:
                    raise InvalidArgument('Time must be an int or str values of "W", "M" "Y", "CY" or "AT"')
        else:
            # Default if arg not provided
            self.arg_dict['query_time_period'] = 'W'

    def _eval_project_id_arg(self):
        """Evaluates the 'p=' argument; Multiple ids need to comma separated"""
        if 'query_projects' in self.arg_dict.keys():
            project_ids = self.arg_dict['query_projects'].split(',')
            for i, e in enumerate(project_ids):
                try:
                    project_ids[i] = int(e)
                except ValueError:
                    raise InvalidArgument('Project ID must be an int')
            self.arg_dict['query_projects'] = tuple(project_ids)
        else:
            # Default if arg not provided
            self.arg_dict['query_projects'] = (0,)

    def _no_args_provided(self):
        """This func provides default arguments If no arguments are provided"""
        self.arg_dict['query_time_period'] = 'W'
        self.arg_dict['query_projects'] = (0,)
        self.arg_dict['query_level'] = 1

    def parse(self):
        if len(self.command_args) != 0:
            param_search = True
            while param_search:
                param_search = self._identify_query_args()

            self._eval_start_end_args()
            self._eval_day_arg()
            self._eval_project_id_arg()
        else:
            self._no_args_provided()

        return super().get_command_tuple()


def date_string_parser(date):
    count_date_fields = len(date.split('/'))
    if count_date_fields == 3:
        month, day, year = date.split('/')
        return datetime.date(year=int(year), month=int(month), day=int(day))
    elif count_date_fields == 2:
        month, day = date.split('/')
        year = datetime.date.today().year
        return datetime.date(year=year, month=int(month), day=int(day))