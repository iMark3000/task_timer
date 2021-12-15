
from ..layout_and_format.printer_objects import Section
from ..layout_and_format.printer_objects import RowHeadings
from ..layout_and_format.printer_objects import Row
from ..layout_and_format.printer_objects import Summary
from timer_reports.report_tree.report_nodes import RootNode


class ReportTreePrint:

    def __init__(self, row, tree, *sections):
        self.report_header = RootNode
        self.section_types = sections
        self.row_type = row
        self.tree = tree
        self.layout_manager = ReportLayoutManager()

    def tree_traversal(self, node):
        if isinstance(node, RootNode):
            main_section = Section(node, F)
            main_section.generate_heading().print_header()
            self.layout_manager.add_full_report_summary(main_section.generate_summary())
            for child in node.children:
                self.tree_traversal(child)
        if type(node) in self.section_types:
            section = Section(node, ASS)
            section.generate_heading().print_header()
            self.layout_manager.add_summary(section.generate_summary())
            for child in node.children:
                self.tree_traversal(child)
        elif isinstance(node, self.row_type):
            # How will you generate row headings?
            row = Row(node, F)
            row.print_row()


class ReportLayoutManager:

    def __init__(self):
        self.full_report_summary = None
        self.section_summary = None
        self.row_headers = None

    def add_full_report_summary(self, summary: Summary):
        self.full_report_summary = summary

    def add_summary(self, summary: Summary):
        if self.section_summary is None:
            self.row_headers.print_row_headings()
            self.section_summary = summary
        else:
            self.section_summary.print_summary()
            self.row_headers.print_row_headings()
            self.section_summary = summary

    def add_row_headers(self, headers: RowHeadings):
        self.row_headers = headers

    def end_of_tree(self):
        self.section_summary.print_summary()
        self.full_report_summary.print_summary()


