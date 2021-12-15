
class Section:

    def __init__(self, report_width, **kwargs):
        self.report_width = report_width
        self.head_field = None
        self.sub_head_field = None
        self.footer_fields = None
        for key, value in kwargs.items():
            if key in self.__dict__.keys():
                self.__dict__[key] = value

    def print_main_head(self, data):
        field = self._format_field(self.head_field)
        head = f' {field} : {data.upper()} '
        print('{0:{fill}{align}{length}}'.format(head, fill='-', align='^', length=self.report_width))

    def print_sub_head(self, data):
        if self.sub_head_field is not None:
            field = self._format_field(self.sub_head_field)
            print(f'>>>>{field}: {data}')

    @staticmethod
    def _format_field(field):
        return " ".join([word for word in field.split('_')]).upper()

    def print_section_foot(self, data):
        print('SECTION SUMMARY')
        print('---------------')
        for key, value in data.items():
            if key in self.footer_fields:
                field = self._format_field(key)
                print(f'{field}: {value}')
