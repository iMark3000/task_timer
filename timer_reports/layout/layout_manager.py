from os import get_terminal_size
from typing import Union

from report_configuration import ROW_FIELD_LAYOUTS
from report_configuration import SECTION_FIELD_LAYOUTS
from report_configuration import REPORT_HEADER_FOOTER_FIELD_LAYOUTS
from report_configuration import REPORT_STRUCTURE
from timer_reports.report_constructor.report_tree.report_nodes import ProjectNode
from timer_reports.report_constructor.report_tree.report_nodes import SessionNode
from timer_reports.report_constructor.report_tree.report_nodes import LogNode


class LayoutManager:

    def __init__(self, report_config: int):
        self._report_config = report_config
        self._report_width = 0
        self._report_header_footer_fields = None
        self._report_section_fields = None
        self._report_row_fields = None
        self._report_row = None
        self._report_sections = None

    def set_up_layout(self) -> None:
        self._report_header_footer_fields = REPORT_HEADER_FOOTER_FIELD_LAYOUTS[self._report_config]
        self._report_section_fields = SECTION_FIELD_LAYOUTS[self._report_config]
        self._report_row_fields = ROW_FIELD_LAYOUTS[self._report_config]["row_fields"]
        self._report_row = REPORT_STRUCTURE["row_node"]
        self._report_sections = REPORT_STRUCTURE["session_nodes"]
        self._report_width = self._get_width()

    @staticmethod
    def _get_width() -> int:
        return get_terminal_size().columns

    @property
    def report_width(self) -> int:
        return self._report_width

    @property
    def report_header_footer_fields(self) -> dict:
        return self._report_header_footer_fields

    @property
    def report_section_fields(self) -> dict:
        return self._report_section_fields

    @property
    def report_row_fields(self) -> list:
        return self._report_row_fields

    @property
    def report_row(self) -> Union[LogNode, SessionNode, ProjectNode]:
        return self._report_row

    @property
    def report_sections(self) -> list:
        return self._report_sections



