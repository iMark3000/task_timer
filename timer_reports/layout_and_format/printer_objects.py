from abc import ABC, abstractmethod


class PrinterObject(ABC):

    def __init__(self, node, fields, formats):
        self.node = node
        self.fields = fields
        self.formats = formats

    @abstractmethod
    def print_lines(self):

        first_line = '|' + '{0:{fill}{align}{length}}'.format('', fill='*', align='^', length=width) + '|'
        print(first_line)

        for key, value in fields.items():
            if 'count' in key:
                print('|' + '{0:{fill}{align}{length}}'.format('', fill='', align='<', length=width) + '|')
            field = f'{key}: {value}'
            field_formatted = '{0:{fill}{align}{length}}'.format(field, fill='', align='<', length=width)
            line = '|' + field_formatted + '|'
            print(line)

        print('|' + '{0:{fill}{align}{length}}'.format('', fill='*', align='^', length=width) + '|')


class ReportHeader(PrinterObject):

    def __init__(self, node, fields, formats):
        super().__init__(node, fields, formats)

    def print_lines(self):
        pass


class ReportFooter(PrinterObject):

    def __init__(self, node, fields, formats):
        super().__init__(node, fields, formats)

    def print_lines(self):
        pass


class SectionHeader(PrinterObject):

    def __init__(self, node, fields, formats):
        super().__init__(node, fields, formats)

    def print_lines(self):
        pass


class SectionFooter(PrinterObject):

    def __init__(self, node, fields, formats):
        super().__init__(node, fields, formats)

    def print_lines(self):
        pass


class RowHeaders(PrinterObject):

    def __init__(self, node, fields, formats):
        super().__init__(node, fields, formats)

    def print_lines(self):
        pass


class Row(PrinterObject):

    def __init__(self, node, fields, formats):
        super().__init__(node, fields, formats)

    def print_lines(self):
        pass
