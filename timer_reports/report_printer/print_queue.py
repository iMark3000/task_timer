from typing import Union

from report_head_foot_printer import ReportHeadFootPrinter
from sectionprinter import SectionPrinter
from rowprinter import RowPrinter
from ..layout.report_componenets import Row
from ..layout.report_componenets import Section
from ..layout.report_componenets import ReportHeaderSummary


class ReportPrintQueue:

    """
    Takes in ReportComponent object (ReportHeaderSummary, Section, Row) and holds them in
    a queue.

    Once the queue is complete, the queue is iterated through, and each component is fed to
    it's corresponding printer objects (ReportHeadFootPrinter, SectionPrinter, RowPrinter).

    The ReportPrintQueue will keep track of printing the header and footer parts of the
    ReportHeadFootPrinter and the SectionPrinter.
    """

    def __init__(self):
        self._report_header_summary = None
        self._sub_queues = list()
        self._report_header_summary_printer = None
        self._section_printer = None
        self._row_printer = None

    def set_report_header_summary_printer(self, printer: ReportHeadFootPrinter) -> None:
        self._report_header_summary_printer = printer

    def set_section_printer(self, printer: SectionPrinter) -> None:
        self._section_printer = printer

    def set_row_printer(self, printer: RowPrinter) -> None:
        self._row_printer = printer

    def set_report_header_summary(self, component: ReportHeaderSummary) -> None:
        self._report_header_summary = component

    def add_to_queue(self, item: "ReportSubQueue") -> None:
        self._sub_queues.append(item)

    def process_queue(self):
        self._print_report_header()
        for item in self._sub_queues:
            if item.section is not None:
                self._print_section_headers(item.section)
            item.sort_rows()
            for row in item.rows:
                self._print_row(row)
            if item.section is not None:
                self._print_section_footer(item.section)
        self._print_report_summary()

    def _print_row(self, row: Row):
        self._row_printer.generate_row(row)

    def _print_row_headers(self):
        self._row_printer.column_head_printer.print_headers()

    def _print_section_headers(self, section: Section):
        self._section_printer.print_section_header(section)

    def _print_section_footer(self, section: Section):
        self._section_printer.print_section_foot(section)

    def _print_report_header(self):
        self._report_header_summary_printer.print_report_header(self._report_header_summary)

    def _print_report_summary(self):
        self._report_header_summary_printer.print_report_summary(self._report_header_summary)


class ReportSubQueue:

    def __init__(self):
        self._section = None
        self._rows = list()

    @property
    def section(self) -> Section:
        return self._section

    @section.setter
    def section(self, section: Section) -> None:
        self._section = section

    def add_row(self, row: Row) -> None:
        self._rows.append(row)

    def sort_rows(self) -> None:
        self._rows.sort(key=lambda x: x.node.start_time)

    @property
    def rows(self) -> list:
        return self._rows
