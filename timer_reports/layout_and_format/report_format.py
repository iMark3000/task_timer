from os import get_terminal_size
from math import floor

from utils.exceptions import ReportTemplateNotFound


class ReportFormatTemplate:

    def __init__(self, level):
        self.level = level

    @staticmethod
    def _log_level_template():
        non_note_col_max_width = 135
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
            "log_id": {"align": '^', "width": .086},
            "start_time": {"align": "^", "width": .17},
            "end_time": {"align": '^', "width": .17},
            "duration": {"align": '^', "width": .15},
            "session_percentage": {"align": '^', "width": .11},
            "project_percentage": {"align": '^', "width": .11},
            "start_log_note": {"align": '<'},
            "end_log_note": {"align": '<'}
        }
        return {'non_note_col_max_width': non_note_col_max_width,
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
            "session": {"align": '^', "width": 0.135},
            "log_count": {"align": '^', "width": 0.135},
            "duration": {"align": '^', "width": 0.147},
            "project_percentage": {"align": '^', "width": 0.127},
            "session_note": {"align": '<'}
        }
        return {'non_note_col_max_width': non_note_col_max_width,
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
            "project_name": {"align": '^', "width": 0.076},
            "session": {"align": '^', "width": 0.135},
            "log_id": {"align": '^', "width": .101},
            "start_time": {"align": "^", "width": .152},
            "end_time": {"align": '^', "width": .161},
            "duration": {"align": '^', "width": .152},
            "project_percentage": {"align": '^', "width": .118},
            "start_log_note": {"align": '<'},
            "end_log_note": {"align": '<'}
        }
        return {"non_note_col_max_width": non_note_col_max_width,
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
        self.non_note_col_width = None
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
    def _calculate_non_note_column_width(self, width):
        sum_col_width = 0
        for row in self.row_format.items():
            if 'width' in row.keys():
                row["width"] = floor(row["width"] * width)
                sum_col_width += row["width"]
        self.non_note_col_width = sum_col_width

    def _check_col_width_against_max(self):
        if self.non_note_col_width > self.non_note_col_max_width:
            self._calculate_non_note_column_width(self.non_note_col_max_width)

    def _calculate_note_column_width(self):
        note_fields = ["start_log_note", "end_log_note", "session_note"]
        note_width = self.report_width - self.non_note_col_width
        for row, value in self.row_format.items():
            for v in value.keys():
                if v in note_fields:
                    value[v].update({"width": note_width})

    def _calculate_end_note_column_formatting(self):
        if 'end_log_note' in self.row_format.keys():
            self.row_format["end_log_note"].update({"buffer": self.non_note_col_width})

    # For Report Header and Footer
    def _calculate_report_header_footer_width(self):
        width = self.report_width - 2
        for k, v in self.report_header_footer["report_header_fields"].items():
            k["width"] = width
        for k, v in self.report_header_footer["report_footer_fields"].items():
            k["width"] = width

    # Just project_name needs the width
    def _calculate_section_header_width(self):
        if self.section_header_footer:
            if 'project_name' in self.section_header_footer['header_fields']:
                self.section_header_footer['header_fields']['project_name'].update({"width": self.report_width})

    def generate_format_dict(self):
        terminal_width = self._get_terminal_width()
        self._set_report_width(terminal_width)
        # Maybe not the best way to do this
        self._calculate_non_note_column_width(self.report_width)
        self._check_col_width_against_max()
        self._calculate_note_column_width()
        self._calculate_end_note_column_formatting()
        self._calculate_report_header_footer_width()
        self._calculate_section_header_width()
