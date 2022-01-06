from typing import Union

from report_head_foot_component_printer import ReportHeadFootPrinter
from section_component_printer import SectionPrinter
from row_component_printer import RowPrinter

from timer_reports.report_constructor.report_componenets import Row
from timer_reports.report_constructor.report_componenets import Section
from timer_reports.report_constructor.report_componenets import ReportHeaderSummary

from timer_reports.layout.layout_manager import LayoutManager


class ReportPrinter:

    def __init__(self, report_layout: LayoutManager):
        self.layout = report_layout
        self._report_header_summary_printer: Union[ReportHeadFootPrinter, None] = None
        self._section_printer: Union[SectionPrinter, None] = None
        self._row_printer: Union[ReportPrinter, None] = None
        self._current_primary_section: Union[Section, None] = None
        self._report_footer: Union[ReportHeaderSummary, None] = None
        self._row_printing_flag: bool = False
        self._row_Queue: RowQueue = RowQueue()

    def set_up_component_printers(self) -> None:
        self._report_header_summary_printer = ReportHeadFootPrinter(self.layout.report_header_footer_fields,
                                                                    self.layout.report_width)
        self._row_printer = RowPrinter(self.layout.report_row_fields, self.layout.report_width)
        if self.layout.report_sections:
            self._section_printer = SectionPrinter(self.layout.report_section_fields, self.layout.report_width)

    def print_component(self, component: Union[Row, Section, ReportHeaderSummary]) -> None:
        if isinstance(component, ReportHeaderSummary):
            if self._row_printing_flag:
                pass
            self._handle_header_footer_print(component)
        elif isinstance(component, Section):
            if self._row_printing_flag:
                pass
            self._handle_section_print(component)
        elif isinstance(component, Row):
            if not self._row_printing_flag:
                self._row_printing_flag = True
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

    def _handle_header_footer_print(self, head_foot: ReportHeaderSummary):
        self._report_header_summary_printer.print_report_header(head_foot)

    def _handle_row_print(self, row: Row):
        pass

    def print_report_footer(self):
        self._report_header_summary_printer.print_report_summary(self._report_footer)




class RowQueue:

    def __init__(self):
        self._queue = list()
        self._is_empty = True

    def add(self, element):
        self._queue.append(element)
        if self._is_empty:
            self._is_empty = False

    def get_elements(self):
        return self._queue