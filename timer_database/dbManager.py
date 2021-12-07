import sqlite3
import os
from typing import Tuple, List

from config.config_manager import ConfigFetch
from utils.database_setup import run_db_setup

DB_PATH = ConfigFetch().fetch_current_env()['PATHS']['DB_PATH']


class DbManager:

    def __init__(self):
        self.db_path = DB_PATH

    def dbConnect(self):
        if os.path.exists(self.db_path):
            return sqlite3.connect(self.db_path)
        else:
            run_db_setup(self.db_path)
            return sqlite3.connect(self.db_path)


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
        cur.execute("SELECT * FROM projects WHERE id=?", project_id)
        result = cur.fetchone()
        conn.close()
        return result


class DbUpdate(DbManager):

    def create_project(self, data: tuple) -> None:
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """INSERT INTO projects(name,status) VALUES(?,?)"""
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

    def del_project(self):
        pass

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
        # Param - (end_date, id)
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """UPDATE sessions SET end_date = ? WHERE id = ?"""
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


class DbQueryReport(DbManager):

    def get_sessions_by_project(self, pid: tuple):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        cur = conn.cursor()
        proj = ', '.join(['?'] * len(pid))
        statement = """
        SELECT 
        projects.name AS project_name,
        projects.id AS project_id,
        sessions.id AS session, 
        sessions.note AS session_note,
        time_log.id AS log_id, 
        time_log.start_timestamp AS start_time, 
        time_log.end_timestamp AS end_time, 
        time_log.start_note AS start_log_note, 
        time_log.end_note AS end_log_note
        FROM projects 
        INNER JOIN sessions ON sessions.project_id = projects.id 
        INNER JOIN time_log ON time_log.session_id = sessions.id 
        WHERE projects.id IN ({p})	
        """.format(p=proj)
        cur.execute(statement, pid)
        results = cur.fetchall()
        conn.close()
        return results
