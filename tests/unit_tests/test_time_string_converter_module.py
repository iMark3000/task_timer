import pytest
import datetime

from utils.time_string_converter import *


def test_all_numbers():
    test_string = '1632'
    today = datetime.datetime.now()
    expected = datetime.datetime(today.year, today.month, today.day, hour=16, minute=32)
    result = TimeDateStrToDateTimeObj(test_string).get_datetime_obj()
    assert result == expected


def test_raise_NonNumberTimeFormatError():
    test_string = 'hamburger'
    with pytest.raises(NonNumberTimeFormatError) as e:
        TimeDateStrToDateTimeObj(test_string).get_datetime_obj()


def test_military_with_colon():
    test_string = '13:44'
    today = datetime.datetime.now()
    expected = datetime.datetime(today.year, today.month, today.day, hour=13, minute=44)
    result = TimeDateStrToDateTimeObj(test_string).get_datetime_obj()
    assert result == expected


def test_military_with_colon_and_p():
    test_string = '13:44p'
    today = datetime.datetime.now()
    expected = datetime.datetime(today.year, today.month, today.day, hour=13, minute=44)
    result = TimeDateStrToDateTimeObj(test_string).get_datetime_obj()
    assert result == expected


def test_military_with_colon_and_pm():
    test_string = '13:44pm'
    today = datetime.datetime.now()
    expected = datetime.datetime(today.year, today.month, today.day, hour=13, minute=44)
    result = TimeDateStrToDateTimeObj(test_string).get_datetime_obj()
    assert result == expected


def test_regular_with_colon_and_p():
    test_string = '1:44p'
    today = datetime.datetime.now()
    expected = datetime.datetime(today.year, today.month, today.day, hour=13, minute=44)
    result = TimeDateStrToDateTimeObj(test_string).get_datetime_obj()
    assert result == expected


def test_regular_with_colon_and_pm():
    test_string = '1:44pm'
    today = datetime.datetime.now()
    expected = datetime.datetime(today.year, today.month, today.day, hour=13, minute=44)
    result = TimeDateStrToDateTimeObj(test_string).get_datetime_obj()
    assert result == expected


def test_regular_just_numbers():
    test_string = '144'
    today = datetime.datetime.now()
    expected = datetime.datetime(today.year, today.month, today.day, hour=1, minute=44)
    result = TimeDateStrToDateTimeObj(test_string).get_datetime_obj()
    assert result == expected


def test_regular_with_colon_am():
    test_string = '1:44'
    today = datetime.datetime.now()
    expected = datetime.datetime(today.year, today.month, today.day, hour=1, minute=44)
    result = TimeDateStrToDateTimeObj(test_string).get_datetime_obj()
    assert result == expected


def test_raise_MinutesValueError():
    test_string = '1388'
    with pytest.raises(MinutesValueError) as e:
        TimeDateStrToDateTimeObj(test_string).get_datetime_obj()


def test_raise_TooManyNumsTimeFormatError():
    test_string = '138822'
    with pytest.raises(TooManyNumsTimeFormatError) as e:
        TimeDateStrToDateTimeObj(test_string).get_datetime_obj()


def test_raise_HoursValueError():
    test_string = '2512'
    with pytest.raises(HoursValueError) as e:
        TimeDateStrToDateTimeObj(test_string).get_datetime_obj()
