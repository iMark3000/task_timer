from os import get_terminal_size
from math import floor

from utils.exceptions import ReportTemplateNotFound


class ReportFormatTemplate:

    def __init__(self, level):
        self.level = level

    @staticmethod
    def _log_level_template():
        non_note_col_width_percent = .79
        non_note_col_max_width = 135
        report_header_fields = {
            'reporting_on': {"align": '<', 'end_char': '|'},
            'reporting_period': {"align": '<', 'end_char': '|'},
        }
        report_footer_fields = {
            'total_duration:': {"align": '<', 'end_char': '|'},
            'project_count:': {"align": '<', 'end_char': '|'},
            'average_project_time:': {"align": '<', 'end_char': '|'},
            'session_count:': {"align": '<', 'end_char': '|'},
            'average_session_time:': {"align": '<', 'end_char': '|'},
            "log_count: ": {"align": '<', 'end_char': '|'},
            "average_log_time:": {"align": '<', 'end_char': '|'}
        }
        section_header_fields = {
            "project_name: ": {"fill": '-', "align": '^'},
            "session": {"fill": '', "align": '<'}
        }
        section_footer_fields = {
            'project_duration': {"align": '<'},
            'session_count:': {"align": '<'},
            'average_session_time:': {"align": '<'},
        }
        row_formats = {
            "log_id": {"align": '^', "width_%": .095, "width": 0},
            "start_time": {"align": "^", "width_%": .22, "width": 0},
            "end_time": {"align": '^', "width_%": .21, "width": 0},
            "duration": {"align": '^', "width_%": .19, "width": 0},
            "session_percentage": {"align": '^', "width_%": .13, "width": 0},
            "project_percentage": {"align": '^', "width_%": .13, "width": 0},
            "start_log_note": {"align": '<'},
            "end_log_note": {"align": '<'}
        }
        return {'non_note_col_max_width': non_note_col_max_width,
                "non_note_col_width_percent": non_note_col_width_percent,
                "report_formats": {
                    "header_fields": report_header_fields,
                    "footer_fields": report_footer_fields},
                "section_formats": {
                    "header_fields": section_header_fields,
                    "footer_fields": section_footer_fields
                },
                'row_formats': row_formats}

    @staticmethod
    def _session_level_template():
        non_note_col_width_percent = .51
        non_note_col_max_width = 84
        report_header_fields = {
            'reporting_on ': {"align": '<', 'end_char': '|'},
            'reporting_period': {"align": '<', 'end_char': '|'},
        }
        report_footer_fields = {
            'total_duration:': {"align": '<', 'end_char': '|'},
            'project_count:': {"align": '<', 'end_char': '|'},
            'average_project_time:': {"align": '<', 'end_char': '|'},
            'session_count:': {"align": '<', 'end_char': '|'},
            'average_session_time:': {"align": '<', 'end_char': '|'},
        }
        section_header_fields = {
            "project_name: ": {"fill": '-', "align": '^'},
        }
        section_footer_fields = {
            'project_duration': {"align": '<'},
            'session_count:': {"align": '<'},
            'average_session_time:': {"align": '<'},
        }
        row_formats = {
            "session": {"align": '^', "width_%": 0.25, "width": 0},
            "log_count": {"align": '^', "width_%": 0.25, "width": 0},
            "duration": {"align": '^', "width_%": 0.3, "width": 0},
            "project_percentage": {"align": '^', "width_%": 0.26, "width": 0},
            "session_note": {"align": '<'}
        }
        return {'non_note_col_max_width': non_note_col_max_width,
                "non_note_col_width_percent": non_note_col_width_percent,
                "report_formats": {
                    "header_fields": report_header_fields,
                    "footer_fields": report_footer_fields},
                "section_formats": {
                    "header_fields": section_header_fields,
                    "footer_fields": section_footer_fields
                },
                'row_formats': row_formats}

    @staticmethod
    def _project_level_template():
        non_note_col_width_percent = .88
        non_note_col_max_width = 131
        report_header_fields = {
            'reporting_on ': {"align": '<', 'end_char': '|'},
            'reporting_period': {"align": '<', 'end_char': '|'},
        }
        report_footer_fields = {
            'total_duration:': {"align": '<', 'end_char': '|'},
            'project_count:': {"align": '<', 'end_char': '|'},
            'average_project_time:': {"align": '<', 'end_char': '|'},
            "log_count: ": {"align": '<', 'end_char': '|'},
            "average_log_time:": {"align": '<', 'end_char': '|'}
        }
        row_formats = {
            "project_name": {"align": '^', "width_%": 0.087, "width": 0},
            "session": {"align": '^', "width_%": 0.145, "width": 0},
            "log_id": {"align": '^', "width_%": .106, "width": 0},
            "start_time": {"align": "^", "width_%": .174, "width": 0},
            "end_time": {"align": '^', "width_%": .174, "width": 0},
            "duration": {"align": '^', "width_%": .184, "width": 0},
            "report_percentage": {"align": '^', "width_%": .135, "width": 0},
            "start_log_note": {"align": '<'},
            "end_log_note": {"align": '<'}
        }
        return {"non_note_col_max_width": non_note_col_max_width,
                "non_note_col_width_percent": non_note_col_width_percent,
                "report_formats": {
                    "header_fields": report_header_fields,
                    "footer_fields": report_footer_fields},
                "section_formats": None,
                "row_formats": row_formats}

    def fetch_template(self):
        if self.level == 0:
            return self._project_level_template()
        elif self.level == 1:
            return self._session_level_template()
        elif self.level == 2:
            return self._log_level_template()
        elif 0 > self.level >= 3:
            raise ReportTemplateNotFound("Unable to find Template.")


class ReportFormatCreator:

    def __init__(self, template: dict):
        self.report_width = 118
        self.non_note_col_max_width = template["non_note_col_max_width"]
        self._non_note_col_width_percent = template["non_note_col_width_percent"]
        self.non_note_col_width = None
        self.non_note_col_width_sum = 0
        self.row_format = template["row_formats"]
        self.report_header_footer = template["report_formats"]
        self.section_header_footer = template["section_formats"]

    @staticmethod
    def _get_terminal_width():
        col = get_terminal_size().columns
        if col < 118:
            print('Minimum width for reports is 118. You may want to expand your terminal window.')
        return col

    def _set_report_width(self, width):
        if 118 < width:
            self.report_width = width

    # For Rows
    def _set_non_note_column_width(self):
        self.non_note_col_width = floor(self.report_width * self._non_note_col_width_percent)
        if self.non_note_col_width > self.non_note_col_max_width:
            self.non_note_col_width = self.non_note_col_max_width

    def _calculate_widths_for_non_note_columns(self):
        for row, attr in self.row_format.items():
            for k, v in attr.items():
                if k == 'width_%':
                    width = floor(attr["width_%"] * self.non_note_col_width)
                    attr["width"] = floor(attr["width_%"] * self.non_note_col_width)
                    self.non_note_col_width_sum += width

    def _calculate_note_column_width(self):
        note_fields = ["start_log_note", "end_log_note", "session_note"]
        note_width = self.report_width - self.non_note_col_width_sum
        for row, attr in self.row_format.items():
            if row in note_fields:
                self.row_format[row].update({"width": note_width})

    def _calculate_end_note_column_padding(self):
        if 'end_log_note' in self.row_format.keys():
            self.row_format["end_log_note"].update({"padding": self.non_note_col_width_sum})

    # For Report Header and Footer
    def _calculate_report_header_footer_width(self):
        width = self.report_width - 2
        for field, attr in self.report_header_footer["header_fields"].items():
            self.report_header_footer["header_fields"][field].update({"width": width})
        for field, attr in self.report_header_footer["footer_fields"].items():
            self.report_header_footer["footer_fields"][field].update({"width": width})

    # Just project_name needs the width
    def _calculate_section_header_width(self):
        if self.section_header_footer:
            if 'project_name' in self.section_header_footer['header_fields']:
                self.section_header_footer['header_fields']['project_name'].update({"width": self.report_width})

    def generate_format_dict(self):
        terminal_width = self._get_terminal_width()
        self._set_report_width(terminal_width)
        self._set_non_note_column_width()
        self._calculate_widths_for_non_note_columns()
        self._calculate_note_column_width()
        self._calculate_end_note_column_padding()
        self._calculate_report_header_footer_width()
        self._calculate_section_header_width()

    def get_formats(self):
        return {"report": self.report_header_footer, "section": self.section_header_footer,
                "row": self.row_format}
