from report_fields import NoteField
from report_fields import TimeField
from report_fields import ProjectField
from report_fields import DurationField
from report_fields import CountField
from report_fields import IDField
from report_fields import AverageField
from report_fields import PercentField


FIELD_MAPPING = {
    'average_LogNode': ['LOG AVE', AverageField],
    'average_ProjectNode': ['PROJECT AVE', AverageField],
    'average_SessionNode': ['SESSION AVE', AverageField],
    'count_LogNode': ['NO. LOGS', CountField],
    'count_ProjectNode': ['NO. PROJECTS', CountField],
    'count_SessionNode': ['NO. SESSIONS', CountField],
    'duration': ['DURATION', DurationField],
    'end_log_note': ['NOTE', NoteField],
    'end_time': ['END TIME', TimeField],
    'log_id': ['LOG ID', IDField],
    'project_id': ['PROJECT ID', IDField],
    'project_name': ['PROJECT NAME', ProjectField],
    'session_id': ['SESSION', IDField],
    'session_note': ['NOTE', NoteField],
    'start_log_note': ['NOTE', NoteField],
    'start_time': ['START TIME', TimeField],
    'percent_ProjectNode': ['%PROJECT', PercentField],
    'percent_RootNode': ['%REPORT', PercentField],
    'percent_SessionNode': ['%SESSION', PercentField],
}

ROW_FIELD_LAYOUTS = {
    1: ['log_id',
        'start_time',
        'end_time',
        'duration',
        'percent_SessionNode',
        'percent_ProjectNode',
        'start_log_note',
        'end_log_note'],
    2: ['session_id',
        'count_LogNode',
        'duration',
        'percent_ProjectNode',
        'session_note'],
    3: ['project_name',
        'session_id',
        'log_id',
        'start_time',
        'end_time',
        'duration',
        'percent_RootNode',
        'session_note']
}

SECTION_FOOTER_FIELD_LAYOUTS = {
    1: ['count_SessionNode',
        'duration',
        'average_SessionNode'
        'percent_RootNode'],
    2: ['count_SessionNode',
        'duration',
        'average_SessionNode',
],
    3: None
}

REPORT_FOOTER_FIELD_LAYOUTS = {
    1: ['duration', 'count_ProjectNode', 'average_ProjectNode',
        'count_SessionNode', 'average_SessionNode', 'count_LogNode',
        'average_LogNode'],
    2: ['duration', 'count_ProjectNode', 'average_ProjectNode',
        'count_SessionNode', 'average_SessionNode'],
    3: ['duration', 'count_ProjectNode', 'average_ProjectNode',
        'count_SessionNode', 'average_SessionNode', 'count_LogNode',
        'average_LogNode']
}
