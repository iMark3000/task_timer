
class Section:

    def __init__(self, node, formatter, footer=True):
        self.node = node
        self.formatter = formatter
        self.footer = footer

    def generate_heading(self):
        return Header()

    def generate_summary(self):
        return Summary()


class RowHeadings:

    def __init__(self, headings, formatter):
        self.headings = headings
        self.formatter = formatter

    def print_row_headings(self):
        pass


class Row:
    # Need to calculate different percentages and count of children
    def __init__(self, node, formatter):
        self.node = node
        self.formatter = formatter

    def print_row(self):
        pass


class Summary:

    def __init__(self):
        pass

    def print_summary(self):
        pass


class Header:

    def __init__(self):
        pass

    def print_header(self):
        pass