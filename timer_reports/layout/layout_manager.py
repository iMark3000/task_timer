from os import get_terminal_size

from report_configuration import ROW_FIELD_LAYOUTS
from report_configuration import SECTION_FIELD_LAYOUTS
from report_configuration import REPORT_HEADER_FOOTER_FIELD_LAYOUTS


class LayoutManager:

    def __init__(self, report_config: int):
        self._report_config = report_config
        self._report_width = 0
        self._report_header_footer_fields = None
        self._report_section_fields = None
        self._report_row_fields = None

    def set_up_layout(self) -> None:
        self._report_header_footer_fields = REPORT_HEADER_FOOTER_FIELD_LAYOUTS[self._report_config]
        self._report_section_fields = SECTION_FIELD_LAYOUTS[self._report_config]
        self._report_row_fields = ROW_FIELD_LAYOUTS[self._report_config]["row_fields"]
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


