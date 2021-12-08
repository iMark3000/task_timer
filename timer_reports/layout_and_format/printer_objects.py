from abc import ABC, abstractmethod


class PrinterObject(ABC):

    def __init__(self, node, formats):
        self.node = node
        self.formats = formats
        pass

    @abstractmethod
    def print_lines(self):
        pass


class ReportHeader(PrinterObject):

    def __init__(self, node, formats):
        super().__init__(node, formats)

    def print_lines(self):
        pass


class ReportFooter(PrinterObject):

    def __init__(self, node, formats):
        super().__init__(node, formats)

    def print_lines(self):
        pass


class SectionHeader(PrinterObject):

    def __init__(self, node, formats):
        super().__init__(node, formats)

    def print_lines(self):
        pass


class SectionFooter(PrinterObject):

    def __init__(self, node, formats):
        super().__init__(node, formats)

    def print_lines(self):
        pass


class RowHeaders(PrinterObject):

    def __init__(self, node, formats):
        super().__init__(node, formats)

    def print_lines(self):
        pass


class Row(PrinterObject):

    def __init__(self, node, formats):
        super().__init__(node, formats)

    def print_lines(self):
        pass
