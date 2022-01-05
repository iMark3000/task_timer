from report_constructor.report_constructor import ReportPrep
from report_constructor.report_constructor import ReportTreeCreator
from report_constructor.report_constructor import ReportConstructor

from layout.layout_manager import LayoutManager


def create_report(data):
    #Todo: data param is coming from Queue Command
    report_data = ReportPrep()
    report_tree = ReportTreeCreator(tree_data).get_tree(report_data.export_data_for_tree())
    layout_manager = LayoutManager() #