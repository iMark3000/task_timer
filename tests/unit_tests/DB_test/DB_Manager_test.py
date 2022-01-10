import pprint
import pytest

from timer_database.dbManager import DbManager


@pytest.fixture
def db_connection():
    return DbManager().dbConnect()


def test_query(db_connection):
    cur = db_connection.cursor()
    project = (10,)
    statement = "SELECT * FROM time_log WHERE session_id=?"
    cur.execute(statement, project)
    result = cur.fetchall()
    db_connection.close()
    print('\n')
    pprint.pprint(result)
    print(type(result[0][2]))
