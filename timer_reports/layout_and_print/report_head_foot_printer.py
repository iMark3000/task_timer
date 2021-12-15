from ..report import ReportHeaderFooter
from report_configuration import FIELD_MAPPING


class ReportHeadFootPrinter:

    def __init__(self, report_width, header_fields, footer_fields):
        self.report_width = report_width - 2
        self.header_fields = header_fields
        self.header_field_names = None
        self.header_field_obj = list()
        self.footer_fields = footer_fields
        self.footer_field_names = None
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

    def first_last_line(self, title_line=False, summary=False):
        title = ''
        if title_line:
            if summary:
                title = ' REPORT SUMMARY '
            else:
                title = ' TIMER QUERY '

        return '| ' + '{0:{fill}{align}{length}}'.format(title, fill='*', align='^', length=self.report_width) + '|'

    def print_section_header(self, report_head: ReportHeaderFooter):
        """
        """
        self.first_last_line(title_line=True)
        for index, field in enumerate(self.header_fields):
            if field in report_head.section_data.keys():  # TODO: !!!
                data = self.header_field_obj[index].print_field(report_head.section_data[field])  # TODO: !!!
                self._print_line(self.header_field_names[index], data)
        self.first_last_line()

    def print_report_summary(self, report_foot: ReportHeaderFooter):
        """
        """
        self.first_last_line(title_line=True, summary=True)
        for index, field in enumerate(self.footer_fields):
            if field in report_foot.section_data.keys():  # TODO: !!!
                data = self.footer_field_obj[index].print_field(report_foot.section_data[field])  # TODO: !!!
                self._print_line(self.footer_field_names[index], data)
        self.first_last_line()

    def _print_line(self, field, data):
        if 'count' in field:
            print('|' + '{0:{fill}{align}{length}}'.format('', fill='', align='<', length=self.report_width) + '|')
        line = f'{field}: {data}'
        print('|' + '{0:{fill}{align}{length}}'.format(line, fill='', align='<', length=self.report_width) + '|')
