import pprint
import pytest
import datetime

from timer_database.dbManager import DbManager
from timer_database.dbManager import DbQueryReport
from timer_database.dbManager import log_query_creator


# Helper function to split the date strings returned by queries
def convert_date_string(s):
    d = s.split(' ')[0]
    year, month, day = d.split('-')
    return datetime.date(year=int(year), month=int(month), day=int(day))


def test_query_for_project_name():
    dbm = DbQueryReport()
    project_ids = (1,)
    result = dbm.query_for_project_name(project_ids)
    print(f'\n{result}')


def test_query_sessions_by_project_id():
    dbm = DbQueryReport()
    project_ids = (1, 2)
    result = dbm.query_sessions_by_project_id(project_ids)
    print(f'\n{result}')


def test_query_by_date_range():
    dbm = DbQueryReport()
    session_ids = ['1', '2']
    start = datetime.date(year=2021, month=11, day=1)
    end = datetime.date(year=2021, month=11, day=15)
    result = dbm.query_by_date_range_by_session(session_ids, start, end)
    for r in result:
        st = convert_date_string(r["start_timestamp"])
        et = convert_date_string(r["end_timestamp"])
        assert start <= st
        assert start <= et
        assert end >= st
        assert end >= et
    print('\n')
    print(result)


def test_query_before_date():
    dbm = DbQueryReport()
    session_ids = ['1', '2']
    query_date = datetime.date(year=2021, month=11, day=15)
    result = dbm.query_before_date_by_session(session_ids, query_date)
    for r in result:
        st = convert_date_string(r["start_timestamp"])
        assert query_date >= st
    print('\n')
    print(result)


def test_query_after_date():
    dbm = DbQueryReport()
    session_ids = ['1', '2']
    query_date = datetime.date(year=2021, month=11, day=1)
    result = dbm.query_after_date_by_session(session_ids, query_date)
    for r in result:
        et = convert_date_string(r["start_timestamp"])
        assert query_date <= et
    print('\n')
    print(result)


def test_log_query_creator():
    dbm = DbQueryReport()
    p = dict()
    p['session_ids'] = ['1', '2']
    p['end_date'] = datetime.date(year=2021, month=11, day=15)
    p['start_date'] = datetime.date(year=2021, month=11, day=1)
    result = log_query_creator(**p)
    print('\n')
    pprint.pprint(result)
    print(result['statement'])
    return result


@pytest.fixture
def data_for_log_query():
    p = dict()
    p['session_ids'] = ['1', '2']
    p['end_date'] = datetime.date(year=2021, month=11, day=15)
    p['start_date'] = datetime.date(year=2021, month=11, day=1)
    result = log_query_creator(**p)
    return result


def test_query(data_for_log_query):
    dbm = DbQueryReport()
    result = dbm.log_query(**data_for_log_query)
    print('\n')
    pprint.pprint(result)
