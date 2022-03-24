import sqlite3
import os
from datetime import date
from typing import Tuple, List

from src.config.config_manager import ConfigFetch
from src.utils.database_setup import run_db_setup

DB_PATH = ConfigFetch().fetch_db_path()


class DbManager:

    def __init__(self):
        self.db_path = DB_PATH

    def dbConnect(self):
        if os.path.exists(self.db_path):
            return sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        else:
            run_db_setup(self.db_path)
            return sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)


class DbQueryUtility(DbManager):

    def query_projects_by_status(self, status):
        conn = self.dbConnect()
        cur = conn.cursor()
        status = (status,)
        cur.execute("SELECT * FROM projects WHERE status=?", status)
        result = cur.fetchall()
        conn.close()
        return result

    def query_all_projects(self):
        conn = self.dbConnect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects")
        result = cur.fetchall()
        conn.close()
        return result

    def fetch_project(self, project_id: tuple) -> tuple:
        conn = self.dbConnect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects WHERE project_id=?", project_id)
        result = cur.fetchone()
        conn.close()
        return result


class DbUpdate(DbManager):

    def create_project(self, data: tuple) -> None:
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """INSERT INTO projects(project_name,status) VALUES(?,?)"""
        cur.execute(sql_statement, data)
        conn.commit()
        conn.close()
        return cur.lastrowid

    def get_all_projects(self) -> List[Tuple]:
        conn = self.dbConnect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects")
        result = cur.fetchall()
        conn.close()
        return result

    def create_session(self, data: tuple) -> None:
        #  data -> project_ind (int) start_time(datetime) end_time(None) note(str or None)
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """INSERT INTO sessions(project_id,start_date,end_date,note) VALUES(?,?,?,?)"""
        cur.execute(sql_statement, data)
        session_id = cur.lastrowid
        conn.commit()
        conn.close()
        return session_id

    def close_session(self, data: tuple) -> None:
        # Param - (end_date, id): datetime
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """UPDATE sessions SET end_date = ? WHERE session_id = ?"""
        cur.execute(sql_statement, data)
        conn.commit()
        conn.close()

    def create_time_log(self, data: tuple) -> None:
        #  Tuple needs to be int and two date objects
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """INSERT INTO time_log(
        session_id,start_timestamp,end_timestamp,start_note,end_note) VALUES(?,?,?,?,?)"""
        cur.execute(sql_statement, data)
        conn.commit()
        conn.close()

    def update_logs(self):
        pass

    def check_for_project(self):
        # Checks for project name
        pass

    def reactivate_project(self, data: tuple):
        # Param - (project_id,): datetime
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """UPDATE projects SET status = 1 WHERE project_id = ?"""
        cur.execute(sql_statement, data)
        conn.commit()
        conn.close()

    def deactivate_project(self, data: tuple):
        # Param - (project_id,): datetime
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """UPDATE projects SET status = 0 WHERE project_id = ?"""
        cur.execute(sql_statement, data)
        conn.commit()
        conn.close()

    def rename_project(self, data: tuple):
        # Param - (new_name, project_id)
        conn = self.dbConnect()
        cur = conn.cursor()
        project_id = (data[1],)
        cur.execute("""SELECT * FROM projects WHERE project_id = ?""", project_id)
        old_data = cur.fetchone()
        old_name = old_data[1]

        sql_statement = """UPDATE projects SET project_name = ? WHERE project_id = ?"""
        cur.execute(sql_statement, data)
        conn.commit()
        conn.close()

        return old_name


class DbQueryReport(DbManager):

    def query_for_project_name(self, project_ids: Tuple[int]):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        cur = conn.cursor()
        proj = ', '.join(['?'] * len(project_ids))
        statement = 'SELECT projects.project_id, projects.project_name FROM projects WHERE projects.project_id IN ({p})'.format(p=proj)
        cur.execute(statement, project_ids)
        results = cur.fetchall()
        conn.close()
        return results

    def query_sessions_by_project_id(self, project_ids: Tuple[int]):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        cur = conn.cursor()
        proj = ', '.join(['?'] * len(project_ids))
        statement = """
            SELECT sessions.session_id, sessions.project_id, sessions.note 
                FROM sessions 
                WHERE sessions.project_id IN ({p})
            """.format(p=proj)
        cur.execute(statement, project_ids)
        results = cur.fetchall()
        conn.close()
        return results

    def query_sessions_by_session_id(self, session_ids: Tuple[int]):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        cur = conn.cursor()
        s = ', '.join(['?'] * len(session_ids))
        statement = """
            SELECT sessions.session_id, sessions.project_id, sessions.note 
                FROM sessions 
                WHERE sessions.session_id IN ({s})
            """.format(s=s)
        cur.execute(statement, session_ids)
        results = cur.fetchall()
        conn.close()
        return results

    def log_query(self, **data):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        cur = conn.cursor()
        if 'sessions' in data.keys():
            statement = data['statement'].format(s=data['sessions'])
        else:
            statement = data['statement']
        cur.execute(statement, data['params'])
        result = cur.fetchall()
        conn.close()
        return result


def log_query_creator(**kwargs):
    data = dict()
    statement_string = list()

    if 'session_ids' in kwargs.keys():
        sessions = ', '.join([str(sid) for sid in kwargs['session_ids']])
        data['sessions'] = sessions
        statement_string.append('SELECT timer.* FROM (SELECT * FROM time_log '
                                'WHERE time_log.session_id IN ({s})) as timer')
    else:
        statement_string.append('SELECT * from time_log as timer')

    data['params'] = dict()
    if 'start_date' not in kwargs.keys():
        # Where clause with one date
        data['params']['query_date'] = kwargs['end_date']
        statement_string.append('WHERE timer.start_timestamp < :query_date')
    elif 'end_date' not in kwargs.keys():
        # Where clause with one date
        data['params']['query_date'] = kwargs['start_date']
        statement_string.append('WHERE timer.start_timestamp > :query_date')
    else:
        # where clause with both dates
        data['params']['start'] = kwargs['start_date']
        data['params']['end'] = kwargs['end_date']
        statement_string.append('WHERE timer.start_timestamp BETWEEN :start AND :end OR timer.end_timestamp '
                                'BETWEEN :start AND :end')

    data['statement'] = ' '.join(statement_string)

    return data
