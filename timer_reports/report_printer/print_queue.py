from report_head_foot_printer import ReportHeadFootPrinter
from sectionprinter import SectionPrinter
from rowprinter import RowPrinter


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
        self.report_header_node = None
        self.current_section = None
        self.component_queue = list()
        self._report_header_summary_printer = None
        self._section_printer = None
        self._row_printer = None

    def set_report_header_summary_printer(self, printer: ReportHeadFootPrinter) -> None:
        self._report_header_summary_printer = printer

    def set_section_printer(self, printer: SectionPrinter) -> None:
        self._section_printer = printer

    def set_row_printer(self, printer: RowPrinter) -> None:
        self._row_printer = printer
