from typing import Union

from timer_reports.report_printer.report_head_foot_component_printer import ReportHeadFootPrinter
from timer_reports.report_printer.section_component_printer import SectionPrinter
from timer_reports.report_printer.row_component_printer import RowPrinter

from timer_reports.report_constructor.report_componenets import Row
from timer_reports.report_constructor.report_componenets import Section
from timer_reports.report_constructor.report_componenets import ReportHeaderSummary

from timer_reports.layout.layout_manager import LayoutManager


class ReportPrinter:

    def __init__(self, report_layout: LayoutManager):
        self.layout = report_layout
        self._report_header_summary_printer: Union[ReportHeadFootPrinter, None] = None
        self._section_printer: Union[SectionPrinter, None] = None
        self._row_printer: Union[RowPrinter, None] = None
        self._current_primary_section: Union[Section, None] = None
        self._report_header_footer_component: Union[ReportHeaderSummary, None] = None
        self._row_Queue: RowQueue = RowQueue()

    def set_up_component_printers(self) -> None:
        self._report_header_summary_printer = ReportHeadFootPrinter(self.layout.report_width,
                                                                    self.layout.report_header_footer_fields)
        self._report_header_summary_printer.configure()
        self._row_printer = RowPrinter(self.layout.report_width, self.layout.report_row_fields)
        self._row_printer.configure_row()
        if self.layout.report_sections:
            self._section_printer = SectionPrinter(self.layout.report_width, self.layout.report_section_fields)
            self._section_printer.configure()

    def print_component(self, component: Union[Row, Section, ReportHeaderSummary]) -> None:
        if isinstance(component, ReportHeaderSummary):
            if not self._row_Queue.empty:
                self._print_row_queue()
            self._report_header_footer_component = component
            self._handle_header_footer_print(self._report_header_footer_component)
        elif isinstance(component, Section):
            if not self._row_Queue.empty:
                self._print_row_queue()
            self._handle_section_print(component)
        elif isinstance(component, Row):
            self._handle_row_print(component)

    def _handle_section_print(self, section: Section):
        if section.is_sub_section():
            self._section_printer.print_section_header(section)
        else:
            if self._current_primary_section is None:
                self._current_primary_section = section
                self._section_printer.print_section_header(section)
            else:
                self._section_printer.print_section_foot(self._current_primary_section)
                self._current_primary_section = section
                self._section_printer.print_section_header(section)

    def _handle_header_footer_print(self, head_foot: ReportHeaderSummary) -> None:
        self._report_header_summary_printer.print_report_header(head_foot)

    def _handle_row_print(self, row: Row) -> None:
        self._row_Queue.add(row)

    def _print_row_queue(self):
        self._row_printer.column_head_printer.print_headers()
        for row in self._row_Queue.get_elements():
            self._row_printer.generate_row(row)
        self._row_Queue = RowQueue()
        print('\n')

    def end_report_printing_process(self) -> None:
        self._print_row_queue()
        self._section_printer.print_section_foot(self._current_primary_section)
        self._report_header_summary_printer.print_report_summary(self._report_header_footer_component)


class RowQueue:

    def __init__(self):
        self._queue = list()
        self._empty = True

    def add(self, element: Row) -> None:
        self._queue.append(element)
        if self._empty:
            self._empty = False

    def get_elements(self) -> list:
        return self._queue

    @property
    def empty(self) -> bool:
        return self._empty
