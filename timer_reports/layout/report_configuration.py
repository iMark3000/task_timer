from timer_reports.report_printer.report_fields import NoteField
from timer_reports.report_printer.report_fields import TimeField
from timer_reports.report_printer.report_fields import ProjectField
from timer_reports.report_printer.report_fields import DurationField
from timer_reports.report_printer.report_fields import IntField
from timer_reports.report_printer.report_fields import HeaderTextField
from timer_reports.report_printer.report_fields import PercentField


FIELD_MAPPING = {
    'average_LogNode': ['LOG AVE', DurationField],
    'average_ProjectNode': ['PROJECT AVE', DurationField],
    'average_SessionNode': ['SESSION AVE', DurationField],
    'count_LogNode': ['NO. LOGS', IntField],
    'count_ProjectNode': ['NO. PROJECTS', IntField],
    'count_SessionNode': ['NO. SESSIONS', IntField],
    'duration': ['DURATION', DurationField],
    'end_log_note': ['NOTE', NoteField],
    'end_time': ['END TIME', TimeField],
    'log_id': ['LOG ID', IntField],
    'project_id': ['PROJECT ID', IntField],
    'project_name': ['PROJECT NAME', ProjectField],
    'session_id': ['SESSION', IntField],
    'session_note': ['NOTE', NoteField],
    'start_log_note': ['NOTE', NoteField],
    'start_time': ['START TIME', TimeField],
    'percent_ProjectNode': ['%PROJECT', PercentField],
    'percent_RootNode': ['%REPORT', PercentField],
    'percent_SessionNode': ['%SESSION', PercentField],
    'reporting_on':  ['REPORTING ON', HeaderTextField],
    'reporting_period':  ['REPORTING PERIOD', HeaderTextField]
}

ROW_FIELD_LAYOUTS = {
    1: {"row_fields": ['log_id',
                       'start_time',
                       'end_time',
                       'duration',
                       'percent_SessionNode',
                       'percent_ProjectNode',
                       'start_log_note',
                       'end_log_note']},
    2: {"row_fields": ['session_id',
                       'count_LogNode',
                       'duration',
                       'percent_ProjectNode',
                       'session_note']},
    3: {"row_fields": ['project_name',
                       'session_id',
                       'log_id',
                       'start_time',
                       'end_time',
                       'duration',
                       'percent_RootNode',
                       'session_note']}
}

SECTION_FIELD_LAYOUTS = {
    1: {"headers": ['project_name', 'session_id'],
        "footers": ['count_SessionNode',
                    'duration',
                    'average_SessionNode',
                    'percent_RootNode']},
    2: {"headers": ['project_name', 'session_id'],
        "footers": ['count_SessionNode',
                    'duration',
                    'average_SessionNode',
                    ]},
    3: None
}

REPORT_HEADER_FOOTER_FIELD_LAYOUTS = {
    1: {"headers": ['reporting_on', 'reporting_period'],
        "footers": ['duration', 'count_ProjectNode', 'average_ProjectNode',
                    'count_SessionNode', 'average_SessionNode', 'count_LogNode',
                    'average_LogNode']},
    2: {"headers": ['reporting_on', 'reporting_period'],
        "footers": ['duration', 'count_ProjectNode', 'average_ProjectNode',
                    'count_SessionNode', 'average_SessionNode']},
    3: {"headers": ['reporting_on', 'reporting_period'],
        "footers": ['duration', 'count_ProjectNode', 'average_ProjectNode',
                    'count_SessionNode', 'average_SessionNode', 'count_LogNode',
                    'average_LogNode']}
}
