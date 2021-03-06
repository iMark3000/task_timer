from src.timer_reports.report_constructor.report_constructor import Section
from ..layout.report_configuration import FIELD_MAPPING


class SectionPrinter:

    def __init__(self, report_width, fields):
        self.report_width = report_width
        self.header_fields = fields["headers"]
        self.header_field_names = list()
        self.header_field_obj = list()
        self.footer_fields = fields["footers"]
        self.footer_field_names = list()
        self.footer_field_obj = list()

    def set_header_field_names(self):
        # Sets field names for corresponding header field
        for field in self.header_fields:
            if field in FIELD_MAPPING.keys():
                header = FIELD_MAPPING[field][0]
                if header not in self.header_field_names:
                    self.header_field_names.append(header)

    def set_header_field_objects(self):
        # Sets appropriate object for each header field
        for field in self.header_fields:
            if field in FIELD_MAPPING.keys():
                field_obj = FIELD_MAPPING[field][1]
                field_obj = field_obj(row_field=False)
                field_obj.set_field_width(self.report_width - (len(field) + 2))
                self.header_field_obj.append(field_obj)

    def set_footer_field_names(self):
        # Sets field names for corresponding footer field
        for field in self.footer_fields:
            if field in FIELD_MAPPING.keys():
                footer = FIELD_MAPPING[field][0]
                if footer not in self.footer_field_names:
                    self.footer_field_names.append(footer)

    def set_footer_field_objects(self):
        # Sets appropriate object for each footer field
        for field in self.footer_fields:
            if field in FIELD_MAPPING.keys():
                field_obj = FIELD_MAPPING[field][1]
                field_obj = field_obj(row_field=False)
                field_obj.set_field_width(self.report_width - (len(field) + 2))
                self.footer_field_obj.append(field_obj)

    def configure(self):
        self.set_header_field_names()
        self.set_header_field_objects()
        self.set_footer_field_names()
        self.set_footer_field_objects()

    def print_section_header(self, section: Section):
        """
        Iterates through the header_fields list and checks if each header is in the Section's data dict keys.
        If True, then it retrieves the value from dict and relays it to the corresponding header_field_obj

        Primary sections are formatted as full line breaks.
        """

        for index, field in enumerate(self.header_fields):
            if field in section.data.keys():
                data = self.header_field_obj[index].print_field(section.data[field])
                if section.is_sub_section():
                    print(f'<<<< {self.header_field_names[index]}: {data} >>>>')
                else:
                    head = f' {self.header_field_names[index]}: {data.upper()} '
                    print('{0:{fill}{align}{length}}'.format(head, fill='-', align='^', length=self.report_width))

        if not section.is_sub_section():
            print('\n')

    def print_section_foot(self, section: Section):
        """
        Iterates through the footer fields and checks if it's in the Section's data dict keys.
        If True, then it retrieves the value from dict and relays it to the corresponding footer_field_obj

        Sub sections do not have footers.
        """
        print('\n')
        if not section.is_sub_section():
            print('SECTION SUMMARY')
            print('---------------')
            for index, field in enumerate(self.footer_fields):
                if field in section.data.keys():
                    data = self.footer_field_obj[index].print_field(section.data[field])
                    print(f'{self.footer_field_names[index]}: {data}')
        print('\n')
