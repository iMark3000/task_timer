from ..report import Section
from report_configuration import FIELD_MAPPING
from .report_fields import ValueField


class SectionPrinter:

    def __init__(self, report_width, header_fields, footer_fields):
        self.report_width = report_width
        self.header_fields = header_fields
        self.header_field_names = None
        self.header_field_obj = list()
        self.footer_fields = footer_fields
        self.footer_field_names = None
        self.footer_field_obj = list()

    def set_header_field_names(self):
        for field in self.header_fields:
            if field in FIELD_MAPPING.keys():
                header = FIELD_MAPPING[field][0]
                if header not in self.header_field_names:
                    self.header_field_names.append(header)

    def set_header_field_objects(self):
        for field in self.header_fields:
            if field in FIELD_MAPPING.keys():
                field_obj = FIELD_MAPPING[field][1]
                field_obj = field_obj(row_field=False)
                field_obj.set_field_width(self.report_width - (len(field) + 2))
                self.header_field_obj.append(field_obj)

    def set_footer_field_names(self):
        for field in self.footer_fields:
            if field in FIELD_MAPPING.keys():
                footer = FIELD_MAPPING[field][0]
                if footer not in self.footer_field_names:
                    self.footer_field_names.append(footer)

    def set_footer_field_objects(self):
        for field in self.footer_fields:
            if field in FIELD_MAPPING.keys():
                field_obj = FIELD_MAPPING[field][1]
                field_obj = field_obj(row_field=False)
                field_obj.set_field_width(self.report_width - (len(field) + 2))
                self.footer_field_obj.append(field_obj)

    def print_section_header(self, section: Section):
        for index, field in enumerate(self.header_fields):
            if field in section.section_data.keys():
                data = section.section_data[field]
                if section.is_sub_section():
                    print(f'>>>>{self.header_field_names[index]}: {data}')
                else:
                    head = f' {self.header_field_names[index]}: {data.upper()} '
                    print('{0:{fill}{align}{length}}'.format(head, fill='-', align='^', length=self.report_width))

    def print_section_foot(self, section: Section):
        if not section.is_sub_section():
            print('SECTION SUMMARY')
            print('---------------')
            for key, value in section.section_data.items():
                if key in self.footer_fields:
                    field = self._format_field(key)
                    print(f'{field}: {value}')
