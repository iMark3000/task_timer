import pprint
import pytest
import datetime

from timer_database.dbManager import DbManager


@pytest.fixture
def db_connection():
    return DbManager().dbConnect()


def test_query_before_or_equal_to_date(db_connection):
    cur = db_connection.cursor()
    project = (3,)
    date = (datetime.date(year=2022, month=1, day=1),)
    # date = ('1/10/2022',)
    statement = "SELECT * FROM time_log WHERE end_timestamp>=?"
    cur.execute(statement, date)
    result = cur.fetchall()
    db_connection.close()
    print('\n')
    pprint.pprint(result)


def test_query_after_or_equal_to_date(db_connection):
    cur = db_connection.cursor()
    project = (3,)
    date = (datetime.date(year=2021, month=11, day=3),)
    # date = ('1/10/2022',)
    statement = "SELECT * FROM time_log WHERE start_timestamp<=?"
    cur.execute(statement, date)
    result = cur.fetchall()
    db_connection.close()
    print('\n')
    pprint.pprint(result)


def test_query_between_dates(db_connection):
    cur = db_connection.cursor()
    project = (3,)
    date = {'start': datetime.date(year=2021, month=11, day=2), 'end': datetime.date(year=2021, month=11, day=3)}
    # date = ('1/10/2022',)
    statement = "SELECT * FROM time_log WHERE start_timestamp>=:start AND end_timestamp<=:end"
    cur.execute(statement, date)
    result = cur.fetchall()
    db_connection.close()
    print('\n')
    pprint.pprint(result)


def test_query_before_or_equal_to_date_with_joins(db_connection):
    cur = db_connection.cursor()
    projects = (1, 2)
    d = datetime.date(year=2022, month=1, day=1)
    # date = ('1/10/2022',)
    data = {'projects': projects}
    statement = """
        SELECT
        projects.name AS project_name,
        projects.id AS project_id,
        sessions.id AS session_id, 
        sessions.note AS session_note,
        time_log.id AS log_id, 
        time_log.start_timestamp AS start_time, 
        time_log.end_timestamp AS end_time, 
        time_log.start_note AS start_log_note, 
        time_log.end_note AS end_log_note
        FROM projects 
        INNER JOIN sessions ON sessions.project_id = projects.id 
        INNER JOIN time_log ON time_log.session_id = sessions.id 
        WHERE projects.id IN projects"""
    cur.execute(statement, data)
    result = cur.fetchall()
    db_connection.close()
    print('\n')
    pprint.pprint(result)
