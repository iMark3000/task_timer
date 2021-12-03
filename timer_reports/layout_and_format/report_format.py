from os import get_terminal_size
from math import floor

from ..report_nodes import RootNode
from ..report_nodes import ProjectNode
from ..report_nodes import SessionNode
from ..report_nodes import LogNode

# 'as_section' Fields are side by side their headers; any header with _DATA
# is formatting for the field's data
# Any "as_section" with 'SPACER' is used to space apart fields

FORMAT_TEMPLATE_DICT = {
    RootNode: {
        "as_section": {
            "section_header": {

                },
            "section_footer": {

            }
        }
    },
    ProjectNode: {
        "as_section": {
            "section_header": {
                "project": 'PROJECT',
            },
            "section_footer": {
                "count_of_children": 'NO. SESSIONS',
                "duration": 'DURATION',
                "average_session":  'AVE. SESSIONS',
                "report_percentage": '%%REPORT'
            }
        },
    },
    SessionNode: {
        "as_section": {
            "section_header": {
                "session": 'SESSION',
                "session_data": 'SESSION_DATA',
            },
            "section_footer": None
        },
        "as_row": {
            'max_report_width': 165,
            'columns':{
                "session": ['SESSION', '^', 15 ],
                "count_of_children": ['NO. LOGS', '^', 15],
                "duration": ['DURATION', '^', 25],
                "report_percentage": ['%%REPORT', '^', 15],
                "project_percentage": ['%%PROJECT', '^', 15],
                "note": ['NOTES', '<']
                      }
                  }},
    LogNode: {
        "as_row": {
            'max_report_width': 165,
            # [COL HEAD, ALIGN, %]
            'columns': {
                "LogID": ['LOG ID', '^', 15],
                "startTime": ['START', '^', 17],
                "endTime": ['END', '^', 17],
                "duration": ['DURATION', '^', 15],
                "session_percentage": ['%%SESSION', '^', 8],
                "project_percentage": ['%%PROJECT', '^', 8],
                "startNote": ['NOTES', '<'],  # Min will always be the difference
                "endNote": [None, '<']  # NEED SPECIAL CALCULATION FOR THIS}
            }
        },
        "as_chron": {
            "max_report_width": 118,
            "columns": {
                "project": ['PROJECT', '^', 25],
                "count_of_children": ['NO. SESSIONS', '^', 25],
                "duration": ['DURATION', '^', 25],
                "report_percentage": ['%%REPORT', '^', 25]
            }
        }
        }
    }


class Formatter:

    def __init__(self, row, *sections):
        self.sections = sections
        self.row = row
        self.terminal_width = self._get_terminal_window_size()
        self.report_width = 118
        self.report_max_width = 0
        self.formats = dict()

    @staticmethod
    def _get_terminal_window_size(self):
        col = get_terminal_size().columns
        if col < 118:
            print('Minimum width for reports is 118. You may want to expand your terminal window.')
        return col

    def _set_report_width(self):
        """Sets the report width to between 118 columns and the max column width depending on size of terminal window"""
        if 118 < self.terminal_width < self.report_max_width:
            self.report_width = self.terminal_width
        elif self.terminal_width > self.report_max_width:
            self.report_width = self.report_max_width

    def _get_section_format_templates(self):
        for section in self.sections:
            _format = FORMAT_TEMPLATE_DICT[section]['as_section']
            self.formats[section] = _format

    def _get_row_format_template(self):
        _format = FORMAT_TEMPLATE_DICT[self.row]['as_row']
        header_mappings = self._create_row_header_map(_format['columns'])
        columns = self._calculate_row_widths(_format['columns'])
        self.formats[self.row]['header_mappings'] = header_mappings
        self.formats[self.row]['column_formats'] = columns

    def _set_report_max_width(self, width):
        self.report_max_width = width

    def _calculate_section_widths(self):
        pass

    def _calculate_row_widths(self, columns: dict):
        new_columns = dict()
        note_width_count = 0
        for k, v in columns.items():
            if v[0] == 'NOTES':
                # Todo: as with header_mapping below, should try to handle notes with it's own method
                width =  note_width_count - self.report_max_width
            else:
                width = floor(self.report_width * (v[2] * 0.01))
                note_width_count += width
            new_columns[k] = {"align": v[1], "width": width}
        return new_columns

    def _create_row_header_map(self, columns: dict):
        header_mappings = dict()
        for k, v in columns.items():
            if v[0] == 'NOTES' and self.row == LogNode:
                # Special clause to handle mapping for start and end notes TODO: Move to it's own method
                if 'NOTES' in header_mappings.keys():
                    header_mappings[v[0]] = header_mappings[v[0]].append(k)
                else:
                    header_mappings[v[0]] = [k]
            header_mappings[v[0]] = k
        return header_mappings

    def _create_row_header_for_notes(self):
        pass

    def generate_formats(self):
        self._set_report_max_width(FORMAT_TEMPLATE_DICT[self.row]['max_report_width'])
        self._set_report_width()
        self._get_row_format_template()
        self._get_section_format_templates()



