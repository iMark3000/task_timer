import sqlite3
from typing import Tuple, List

from utils.settings import TIMER_DB_PATH


class DbManager:

    def __init__(self):
        self.db_path = TIMER_DB_PATH

    def dbConnect(self):
        return sqlite3.connect(self.db_path)


class DbQuery(DbManager):

    def query_project_list(self):
        pass

    def query_project_time(self):
        pass

    def query_time_period(self):
        pass


class DbUpdate(DbManager):

    def create_project(self, data: tuple) -> None:
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """INSERT INTO projects(name,status) VALUES(?,?)"""
        cur.execute(sql_statement, data)
        conn.commit()
        conn.close()

    def get_all_projects(self) -> List[Tuple]:
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

    def del_project(self):
        pass

    def create_session(self, data: tuple) -> None:
        #  Tuple needs to be int and two datetime objects
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """INSERT INTO sessions(project_id,start_date,end_date) VALUES(?,?,?)"""
        cur.execute(sql_statement, data)
        conn.commit()
        conn.close()
        return cur.lastrowid

    def fetch_session(self, session_id: tuple) -> tuple:
        conn = self.dbConnect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects WHERE id=?", session_id)
        result = cur.fetchone()
        conn.close()
        return result

    def close_session(self, data: tuple) -> None:
        # Param - (end_date, id)
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """UPDATE session SET end_date = ? WHERE id = ?"""
        cur.execute(sql_statement, data)
        conn.commit()
        conn.close()

    def create_time_log(self, data: tuple) -> None:
        #  Tuple needs to be int and two date objects
        conn = self.dbConnect()
        cur = conn.cursor()
        sql_statement = """INSERT INTO time_log(session_id,start_timestamp,end_timestamp) VALUES(?,?,?)"""
        cur.execute(sql_statement, data)
        conn.commit()
        conn.close()

    def update_logs(self):
        pass

    def check_for_project(self):
        # Checks for project name
        pass
