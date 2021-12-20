
from ..layout.report_configuration import FIELD_MAPPING
from ..layout.report_componenets import Row
from .report_fields import Field
from .report_fields import NoteField
from typing import List


class RowPrinter:

    def __init__(self, report_width, fields):
        self.row_fields = fields["row_fields"]
        self.report_width = report_width
        self.column_widths = 0
        self.column_headers = list()
        self.row_field_objects = list()
        self.column_head_printer = ColumnHeaderPrinter()

    def set_headers(self):
        # Looks up column heading from FIELD_MAPPING
        for field in self.row_fields:
            if field in FIELD_MAPPING.keys():
                header = FIELD_MAPPING[field][0]
                if header not in self.column_headers:
                    self.column_headers.append(header)

    def set_field_objects(self):
        # Create a Field Object to correspond with the column's data
        for field in self.row_fields:
            if field in FIELD_MAPPING.keys():
                field_obj = FIELD_MAPPING[field][1]
                if field == 'end_log_note':
                    self.row_field_objects.append(field_obj(end_note=True))
                else:
                    self.row_field_objects.append(field_obj())

    def set_non_note_field_widths(self):
        # Iterate through Field Objects and set their widths
        calculated_column_widths = self.report_width * .75  # Todo: This is an  arbitrary number for testing
        for field in self.row_field_objects:
            if not isinstance(field, NoteField):
                field.set_field_width(calculated_column_widths)
                self.column_widths += field.field_width

    def set_note_field_widths(self):
        # Special function to set the width of NoteField objects
        width = self.report_width - self.column_widths
        for field in self.row_field_objects:
            if isinstance(field, NoteField):
                field.set_field_width(width)

    def set_column_head_printer(self):
        self.column_head_printer.configure_header_printer(self.column_headers, self.row_field_objects)

    def configure_row(self):
        # Driver function to run all of the funcs needed to prep for printing
        self.set_headers()
        self.set_field_objects()
        self.set_non_note_field_widths()
        self.set_note_field_widths()
        self.set_column_head_printer()

    def generate_row(self, row: Row):
        # Takes in Row object, accesses it's data, and compiles a print line
        data = row.data
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


class ColumnHeaderPrinter:

    def __init__(self):
        self.column_headers = list()
        self.column_header_widths = dict()
        self.header_line = None
        self.header_breaker_line = None

    def _set_headers(self, headers: list):
        self.column_headers = headers

    def _set_header_widths(self, field_obj: List[Field]):
        for index, header in enumerate(self.column_headers):
            self.column_header_widths[header] = field_obj[index].field_width

    def _create_header_line(self):
        for header in self.column_headers:
            if header != 'NOTE':
                head = '{0:{fill}{align}{length}}'.format(header, fill='', align='^',
                                                          length=self.column_header_widths[header] - 1) + '|'
            else:
                head = '{0:{fill}{align}{length}}'.format(header, fill='', align='<',
                                                          length=self.column_header_widths[header])
            if self.header_line is None:
                self.header_line = head
            else:
                self.header_line += head

    def _create_header_breaker_line(self):
        width = 0
        field_widths = [v for v in self.column_header_widths.values()]
        for w in field_widths:
            width += w

        self.header_breaker_line = '{0:{fill}{align}{length}}'.format('', fill='-', align='<', length=width)

    def configure_header_printer(self, column_headers, field_objects):
        self._set_headers(column_headers)
        self._set_header_widths(field_objects)
        self._create_header_line()
        self._create_header_breaker_line()

    def print_headers(self):
        print(self.header_line)
        print(self.header_breaker_line)
