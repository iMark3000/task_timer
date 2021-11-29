from collections import namedtuple

from .arg_parse_base_class import CommandArgParser
from utils.command_enums import InputType

REPORT_TYPES = ['spr', 'tpr', 'ctp']

REPORT_LEVEL = ['+l', '+s', '+p']


class QueryCommandArgParser(CommandArgParser):
    # Todo: Setup Queries
    def __init__(self, command: InputType, command_args: list):
        super().__init__(command, command_args)

    def _identify_report_type(self):
        for index, arg in self.command_args:
            if REPORT_TYPES in arg:
                self._parse_report_type(self.command_args.pop(index))
                break

    def _parse_report_type(self, report):
        if '=' in report:
            report_type, report_param = report.split('=')
            self.arg_dict['report_type'] = report_type
            if report_param == '':
                self.arg_dict['report_param'] = report_param
        else:
            self.arg_dict['report_type'] = report

    def _id_parse_report_level(self):
        for index, arg in self.command_args:
            if REPORT_LEVEL in arg:
                self.arg_dict['report_level'] = arg
                break

    def parse(self):
        self._identify_report_type()
        self._id_parse_report_level()
        return super().get_command_tuple()