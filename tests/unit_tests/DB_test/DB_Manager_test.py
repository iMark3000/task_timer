import pprint
import pytest
import datetime

from src.timer_database.dbManager import DbManager
from src.timer_database.dbManager import DbQueryReport
from src.timer_database.dbManager import log_query_creator


# Helper function to split the date strings returned by queries
def convert_date_string(s):
    d = s.split(' ')[0]
    year, month, day = d.split('-')
    return datetime.date(year=int(year), month=int(month), day=int(day))


def test_query_for_project_name():
    dbm = DbQueryReport()
    project_ids = (1, 2)
    result = dbm.query_for_project_name(project_ids)
    print(f'\n{result}')


def test_query_sessions_by_project_id():
    dbm = DbQueryReport()
    project_ids = (1, 2)
    result = dbm.query_sessions_by_project_id(project_ids)
    print(f'\n{result}')


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
    p['session_ids'] = [1, 2]
    p['end_date'] = datetime.date(year=2022, month=1, day=15)
    p['start_date'] = datetime.date(year=2022, month=1, day=1)
    result = log_query_creator(**p)
    return result


def test_query(data_for_log_query):
    dbm = DbQueryReport()
    result = dbm.log_query(**data_for_log_query)
    print('\n')
    pprint.pprint(result)
