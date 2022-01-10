
from timer_reports.report_constructor.report_constructor import ReportPrep
from timer_reports.report_constructor.report_constructor import ReportTreeCreator
from timer_reports.report_constructor.report_constructor import ReportConstructor
from timer_reports.report_constructor.report_constructor import total_duration_helper

from timer_reports.report_printer.printer_manager import ReportPrinter

from timer_reports.layout.layout_manager import LayoutManager


def create_report(data):
    """
    data from Query Command needs to supply these arguments to make teh report work

    reporting_on: tuple(str) of project_ids that were queried
    reporting_period: tuples(str) of the dates that were queried
    reporting_level: An int that will dictate the level at which the report will display
        1 - Log Level
        2 - Session Level
        3 - Project Level (not working yet)
    report_query: a list of dictionaries; each dict is a row from teh log table combined with
        the project_id, project_name, and session_id
    """

    report_data = ReportPrep(data["reporting_period"], data["reporting_on"], data["report_query"])
    report_data.prep_report()
    report_tree_creator = ReportTreeCreator(**report_data.export_data_for_tree())
    report_tree_creator.build_tree()
    report_tree = report_tree_creator.get_tree()
    total_duration_helper(report_tree)

    layout_manager = LayoutManager(data["reporting_level"])
    layout_manager.set_up_layout()

    report_constructor = ReportConstructor(report_tree, layout_manager)
    report_constructor.construct()
    report_components = report_constructor.get_report_components()

    report_printer = ReportPrinter(layout_manager)
    report_printer.set_up_component_printers()
    for component in report_components:
        component.compile_data()
        report_printer.print_component(component)
    report_printer.end_report_printing_process()
