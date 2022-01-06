from report_constructor.report_constructor import ReportPrep
from report_constructor.report_constructor import ReportTreeCreator
from report_constructor.report_constructor import ReportConstructor

from layout.layout_manager import LayoutManager


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
    report_tree = ReportTreeCreator(**report_data.export_data_for_tree()).get_tree()
    layout_manager = LayoutManager(data["reporting_level"])

    report_constructor = ReportConstructor(report_tree, layout_manager)
