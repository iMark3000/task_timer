from report_format import ReportFormatTemplate
from report_format import ReportFormatCreator
from printer_objects import ReportHeader
from printer_objects import ReportFooter
from printer_objects import SectionHeader
from printer_objects import SectionFooter
from printer_objects import RowHeaders
from printer_objects import Row


class PrinterObjectFactory:

    """
    This class combines report_nodes with their needed formatting to create a PrintObject.
    PrinterObjects are then passed to the PrintQueue.
    """

    def __init__(self, report_level):
        self.report_level = report_level
        # Report Headers
        self.report_heading_fields = None
        self.report_heading_formats = None
        self.report_footer_fields = None
        self.report_footer_formats = None
        # Report Sections
        self.section_heading_fields = None
        self.section_heading_formats = None
        self.section_footer_fields = None
        self.section_footer_formats = None
        # Report Rows
        self.row_fields = None
        self.row_formats = None

    def get_formats(self) -> dict:
        format_template = ReportFormatTemplate(self.report_level).fetch_template()
        return ReportFormatCreator(format_template).get_formats()

    def set_report_formats(self, formats):
        self.report_heading_fields = list(formats["header_fields"].keys())
        self.report_heading_formats = formats["header_fields"]
        self.report_footer_fields = list(formats["header_fields"].keys())
        self.report_footer_formats = formats["footer_fields"]

    def set_section_formats(self, formats):
        self.section_heading_fields = list(formats["header_fields"].keys())
        self.section_heading_formats = formats["header_fields"]
        self.section_footer_fields = list(formats["header_fields"].keys())
        self.section_footer_formats = formats["footer_fields"]

    def set_row_formats(self, formats):
        self.row_fields = list(formats["row_formats"].keys)
        self.row_formats = formats["row_formats"]

    def set_up_formats(self):
        formatting = self.get_formats()
        self.set_report_formats(formatting["report"])
        if formatting['section'] is not None:
            self.set_section_formats(formatting['section'])
        self.set_row_formats(formatting['row'])

    def create_report_header(self, node):
        return ReportHeader(node, self.report_heading_fields, self.report_heading_formats)

    def create_report_footer(self, node):
        return ReportFooter(node, self.report_footer_fields, self.report_footer_formats)

    def create_section_header(self, node):
        return SectionHeader(node, self.section_heading_fields, self.section_heading_formats)

    def create_section_footer(self, node):
        return SectionFooter(node, self.section_footer_fields, self.section_footer_formats)

    def create_row_header(self, node):
        return RowHeaders(node, self.row_fields, self.row_formats)

    def create_row(self, node):
        return Row(node, self.row_fields, self.row_formats)
