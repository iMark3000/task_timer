import pytest
from pytest_mock import mocker

from timer_reports.layout_and_format.report_format import ReportFormatTemplate
from timer_reports.layout_and_format.report_format import ReportFormatCreator


def test_log_level(mocker):
    mocker.patch('timer_reports.layout_and_format.report_format.ReportFormatCreator._get_terminal_width',
                 return_value=118)
    template = ReportFormatTemplate(2).fetch_template()
    report_format = ReportFormatCreator(template)
    report_format.generate_format_dict()
    formats = report_format.get_formats()
    assert report_format.report_width == 118
    assert report_format.non_note_col_max_width == 135
    assert report_format.non_note_col_width == 93
    assert report_format._non_note_col_width_percent == .79
    assert formats["section"] is not None
    assert formats["row"]["log_id"]["width"] == 8
    assert formats["row"]["start_time"]["width"] == 20
    assert formats["row"]["end_time"]["width"] == 19
    assert formats["row"]["duration"]["width"] == 17
    assert formats["row"]["session_percentage"]["width"] == 12
    assert formats["row"]["project_percentage"]["width"] == 12
    assert formats["row"]["start_log_note"]["width"] == 30
    assert formats["row"]["end_log_note"]["width"] == 30
    assert formats["row"]["end_log_note"]["padding"] == 88


def test_log_level_max_non_note_col_width(mocker):
    mocker.patch('timer_reports.layout_and_format.report_format.ReportFormatCreator._get_terminal_width',
                 return_value=200)
    template = ReportFormatTemplate(2).fetch_template()
    report_format = ReportFormatCreator(template)
    report_format.generate_format_dict()
    formats = report_format.get_formats()
    assert report_format.report_width == 200
    assert report_format.non_note_col_max_width == 135
    assert report_format.non_note_col_width == 135
    assert report_format.non_note_col_width_sum == 128
    assert report_format._non_note_col_width_percent == .79
    assert formats["section"] is not None
    assert formats["row"]["log_id"]["width"] == 12
    assert formats["row"]["start_time"]["width"] == 29
    assert formats["row"]["end_time"]["width"] == 28
    assert formats["row"]["duration"]["width"] == 25
    assert formats["row"]["session_percentage"]["width"] == 17
    assert formats["row"]["project_percentage"]["width"] == 17
    assert formats["row"]["start_log_note"]["width"] == 72
    assert formats["row"]["end_log_note"]["width"] == 72
    assert formats["row"]["end_log_note"]["padding"] == 128


def test_log_level_less_than_min(mocker):
    mocker.patch('timer_reports.layout_and_format.report_format.ReportFormatCreator._get_terminal_width',
                 return_value=118)
    template = ReportFormatTemplate(2).fetch_template()
    report_format = ReportFormatCreator(template)
    report_format.generate_format_dict()
    formats = report_format.get_formats()
    assert report_format.report_width == 118
    assert report_format.non_note_col_max_width == 135
    assert report_format.non_note_col_width == 93
    assert report_format._non_note_col_width_percent == .79
    assert formats["section"] is not None
    assert formats["row"]["log_id"]["width"] == 8
    assert formats["row"]["start_time"]["width"] == 20
    assert formats["row"]["end_time"]["width"] == 19
    assert formats["row"]["duration"]["width"] == 17
    assert formats["row"]["session_percentage"]["width"] == 12
    assert formats["row"]["project_percentage"]["width"] == 12
    assert formats["row"]["start_log_note"]["width"] == 30
    assert formats["row"]["end_log_note"]["width"] == 30
    assert formats["row"]["end_log_note"]["padding"] == 88


def test_session_level(mocker):
    mocker.patch('timer_reports.layout_and_format.report_format.ReportFormatCreator._get_terminal_width',
                 return_value=118)
    template = ReportFormatTemplate(1).fetch_template()
    report_format = ReportFormatCreator(template)
    report_format.generate_format_dict()
    formats = report_format.get_formats()
    assert report_format.report_width == 118
    assert report_format.non_note_col_max_width == 84
    assert report_format.non_note_col_width == 60
    assert report_format._non_note_col_width_percent == .51
    assert formats["section"] is not None
    assert formats["row"]["session"]["width"] == 15
    assert formats["row"]["log_count"]["width"] == 15
    assert formats["row"]["duration"]["width"] == 18
    assert formats["row"]["project_percentage"]["width"] == 15
    assert formats["row"]["session_note"]["width"] == 55


def test_session_level_max_non_note_col_width(mocker):
    mocker.patch('timer_reports.layout_and_format.report_format.ReportFormatCreator._get_terminal_width',
                 return_value=200)
    template = ReportFormatTemplate(1).fetch_template()
    report_format = ReportFormatCreator(template)
    report_format.generate_format_dict()
    formats = report_format.get_formats()
    assert report_format.report_width == 200
    assert report_format.non_note_col_max_width == 84
    assert report_format.non_note_col_width == 84
    assert report_format._non_note_col_width_percent == .51
    assert formats["section"] is not None
    assert formats["row"]["session"]["width"] == 21
    assert formats["row"]["log_count"]["width"] == 21
    assert formats["row"]["duration"]["width"] == 25
    assert formats["row"]["project_percentage"]["width"] == 21
    assert formats["row"]["session_note"]["width"] == 112


def test_session_level_less_than_min(mocker):
    mocker.patch('timer_reports.layout_and_format.report_format.ReportFormatCreator._get_terminal_width',
                 return_value=100)
    template = ReportFormatTemplate(1).fetch_template()
    report_format = ReportFormatCreator(template)
    report_format.generate_format_dict()
    formats = report_format.get_formats()
    assert report_format.report_width == 118
    assert report_format.non_note_col_max_width == 84
    assert report_format.non_note_col_width == 60
    assert report_format._non_note_col_width_percent == .51
    assert formats["section"] is not None
    assert formats["row"]["session"]["width"] == 15
    assert formats["row"]["log_count"]["width"] == 15
    assert formats["row"]["duration"]["width"] == 18
    assert formats["row"]["project_percentage"]["width"] == 15
    assert formats["row"]["session_note"]["width"] == 55


def test_project_level(mocker):
    mocker.patch('timer_reports.layout_and_format.report_format.ReportFormatCreator._get_terminal_width',
                 return_value=118)
    template = ReportFormatTemplate(0).fetch_template()
    report_format = ReportFormatCreator(template)
    report_format.generate_format_dict()
    formats = report_format.get_formats()
    assert report_format.report_width == 118
    assert report_format.non_note_col_max_width == 131
    assert report_format.non_note_col_width == 103
    assert report_format._non_note_col_width_percent == .88
    assert formats["section"] is None
    assert formats["row"]["project_name"]["width"] == 8
    assert formats["row"]["session"]["width"] == 14
    assert formats["row"]["log_id"]["width"] == 10
    assert formats["row"]["start_time"]["width"] == 17
    assert formats["row"]["end_time"]["width"] == 17
    assert formats["row"]["duration"]["width"] == 18
    assert formats["row"]["report_percentage"]["width"] == 13
    assert formats["row"]["start_log_note"]["width"] == 21
    assert formats["row"]["end_log_note"]["width"] == 21
    assert formats["row"]["end_log_note"]["padding"] == 97


def test_project_level_max_non_note_col_width(mocker):
    mocker.patch('timer_reports.layout_and_format.report_format.ReportFormatCreator._get_terminal_width',
                 return_value=200)
    template = ReportFormatTemplate(0).fetch_template()
    report_format = ReportFormatCreator(template)
    report_format.generate_format_dict()
    formats = report_format.get_formats()
    assert report_format.report_width == 200
    assert report_format.non_note_col_max_width == 131
    assert report_format.non_note_col_width == 131
    assert report_format._non_note_col_width_percent == .88
    assert formats["section"] is None
    assert formats["row"]["project_name"]["width"] == 11
    assert formats["row"]["session"]["width"] == 18
    assert formats["row"]["log_id"]["width"] == 13
    assert formats["row"]["start_time"]["width"] == 22
    assert formats["row"]["end_time"]["width"] == 22
    assert formats["row"]["duration"]["width"] == 24
    assert formats["row"]["report_percentage"]["width"] == 17
    assert formats["row"]["start_log_note"]["width"] == 73
    assert formats["row"]["end_log_note"]["width"] == 73
    assert formats["row"]["end_log_note"]["padding"] == 127


def test_project_level_less_than_min(mocker):
    mocker.patch('timer_reports.layout_and_format.report_format.ReportFormatCreator._get_terminal_width',
                 return_value=100)
    template = ReportFormatTemplate(0).fetch_template()
    report_format = ReportFormatCreator(template)
    report_format.generate_format_dict()
    formats = report_format.get_formats()
    assert report_format.report_width == 118
    assert report_format.non_note_col_max_width == 131
    assert report_format.non_note_col_width == 103
    assert report_format._non_note_col_width_percent == .88
    assert formats["section"] is None
    assert formats["row"]["project_name"]["width"] == 8
    assert formats["row"]["session"]["width"] == 14
    assert formats["row"]["log_id"]["width"] == 10
    assert formats["row"]["start_time"]["width"] == 17
    assert formats["row"]["end_time"]["width"] == 17
    assert formats["row"]["duration"]["width"] == 18
    assert formats["row"]["report_percentage"]["width"] == 13
    assert formats["row"]["start_log_note"]["width"] == 21
    assert formats["row"]["end_log_note"]["width"] == 21
    assert formats["row"]["end_log_note"]["padding"] == 97