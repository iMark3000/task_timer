from row_fields import NoteField
from row_fields import TimeField
from row_fields import SesionField
from row_fields import ProjectField
from row_fields import DurationField
from row_fields import CountField
from row_fields import IDField


FIELD_MAPPING = {
    'end_log_note': ['NOTE', NoteField],
    'end_time': ['END TIME', TimeField],
    'session_note': ['NOTE', NoteField],
    'session_id': ['SESSION', IDField], # get rid of session
    'start_log_note': ['NOTE', NoteField],
    'start_time': ['START TIME', TimeField],
    'project_name': ['PROJECT NAME', ProjectField],
    'duration': ['DURATION', DurationField],
    'log_id': ['LOG ID', IDField],
    'project_id': ['PROJECT ID', IDField]
}


class Row:

    def __init__(self, fields, report_width):
        self.row_fields = fields
        self.report_width = report_width
        self.column_widths = 0
        self.column_headers = list()
        self.row_field_objects = list()

    def set_headers(self):
        for field in self.row_fields:
            if field in FIELD_MAPPING.keys():
                header = FIELD_MAPPING[field][0]
                if header not in self.column_headers:
                    self.column_headers.append(header)

    def set_field_objects(self):
        for field in self.row_fields:
            if field in FIELD_MAPPING.keys():
                field_obj = FIELD_MAPPING[field][1]
                if field == 'end_log_note':
                    self.row_field_objects.append(field_obj(end_note=True))
                else:
                    self.row_field_objects.append(field_obj())

    def set_non_note_field_widths(self):
        calculated_column_widths = self.report_width * .50
        for field in self.row_field_objects:
            if not isinstance(field, NoteField):
                field.set_field_width(calculated_column_widths)
                self.column_widths += field.field_width

    def set_note_field_widths(self):
        width = self.report_width - self.column_widths
        for field in self.row_field_objects:
            if isinstance(field, NoteField):
                field.set_field_width(width)

    def configure_row(self):
        self.set_headers()
        self.set_field_objects()
        self.set_non_note_field_widths()
        self.set_note_field_widths()

    def print_column_headers(self):
        line = ''
        for index, header in enumerate(self.column_headers):
            formatted_value = self.row_field_objects[index].print_field(header)
            line += formatted_value[:-1] + '|'
        print(line)
        print('{0:{fill}{align}{length}}'.format('', fill='-', align='<', length=self.report_width))

    def generate_row(self, data):
        line = ''
        for index, field in enumerate(self.row_fields):
            value = data[field]
            if value is not None and field == 'start_log_note':
                formatted_value = self.row_field_objects[index].print_field(value, padding=self.column_widths)
                line += formatted_value
            elif value is not None:
                formatted_value = self.row_field_objects[index].print_field(value)
                line += formatted_value
            elif value is None and field == 'start_log_note' or field == 'session_note':
                formatted_value = self.row_field_objects[index].print_field('None')
                line += formatted_value
            else:
                pass

        print(line)

