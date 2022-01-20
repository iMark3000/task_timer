import pytest
from pytest_mock import mocker
from datetime import datetime
from datetime import timedelta

from src.timer_reports.report_printer.report_fields import ProjectField
from src.timer_reports.report_printer.report_fields import TimeField
from src.timer_reports.report_printer.report_fields import IntField
from src.timer_reports.report_printer.report_fields import DurationField
from src.timer_reports.report_printer.report_fields import PercentField
from src.timer_reports.report_printer.report_fields import NoteField


def test_project_field():
    field = ProjectField()
    field.set_field_width(110)
    line = field.print_field('test_yo')
    assert field.field_width == 9
    assert len(line) == 9


def test_project_field_truncate():
    field = ProjectField()
    field.set_field_width(150)
    line = field.print_field('will this truncate?')
    assert field.field_width == 12
    assert len(line) == 12
    print(f'\n{line}')


def test_project_field_min_size():
    field = ProjectField()
    field.set_field_width(100)
    line = field.print_field('Test')
    assert field.field_width == 9
    assert len(line) == 9


def test_project_field_as_not_row():
    field = ProjectField(row_field=False)
    field.set_field_width(100)
    line = field.print_field('Test')
    assert field.field_width == 100
    assert len(line) == 4
    print(f'\n{line}')


def test_time_field():
    field = TimeField()
    field.set_field_width(110)
    line = field.print_field(datetime(year=2021, day=12, month=12, hour=12, minute=12))
    assert field.field_width == 26
    assert len(line) == 26
    print(f'\n{line}')


def test_int_field():
    field = IntField()
    field.set_field_width(110)
    line = field.print_field(3)
    assert field.field_width == 15
    assert len(line) == 15
    print(f'\n{line}')


def test_duration_field():
    field = DurationField()
    field.set_field_width(110)
    line = field.print_field(timedelta(days=1, hours=1, minutes=23))
    assert field.field_width == 18
    assert len(line) == 18
    print(f'\n{line}')


def test_percent_field():
    field = PercentField()
    field.set_field_width(110)
    line = field.print_field(0.99)
    assert field.field_width == 14
    assert len(line) == 14
    print(f'\n{line}')


def test_note_field():
    field = NoteField()
    field.set_field_width(50)
    line = field.print_field('TEST TEST TEST')
    assert field.field_width == 50
    assert len(line) == 50
    print(f'\n{line}')


def test_end_note_field():
    field = NoteField(end_note=True)
    field.set_field_width(50)
    line = field.print_field('TEST TEST TEST', 100)
    assert field.field_width == 50
    assert len(line) == 151
    print(f'{line}')


def test_full_row():
    field1 = ProjectField()
    field1.set_field_width(110)
    line1 = field1.print_field('TEST IT')

    field2 = TimeField()
    field2.set_field_width(110)
    line2 = field2.print_field(datetime(year=2021, day=12, month=12, hour=12, minute=12))

    field3 = TimeField()
    field3.set_field_width(110)
    line3 = field3.print_field(datetime(year=2021, day=12, month=12, hour=12, minute=12))

    field4 = PercentField()
    field4.set_field_width(110)
    line4 = field4.print_field(.90)

    field5 = NoteField()
    field5.set_field_width(50)
    line5 = field5.print_field('TEST TEST TEST')

    padding = field1.field_width + field2.field_width + field3.field_width + field4.field_width
    field6 = NoteField(end_note=True)
    field6.set_field_width(50)
    line6 = field6.print_field('TEST TEST TEST', padding)

    print('\n' + line1 + line2 + line3 + line4 + line5 + line6)
