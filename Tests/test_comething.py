import pytest
import datetime

from utils.time_string_converter import TimeStringToDateTimeObj


@pytest.fixture
def data():
    return '133p'


def test_time_convert(data):
    t = TimeStringToDateTimeObj(data)
    d = today = datetime.date.today()
    test_d = datetime.datetime(d.year, d.month, d.day, hour=13, minute=33)
    assert test_d == t.get_datetime_obj()
