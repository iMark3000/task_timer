import sqlite3

from utils.settings import TIMER_DB_PATH


#  TODO: What is the best way for setting up a database in a package?


class DbManager:

    def __init__(self):
        self.db_path = TIMER_DB_PATH
        self.conn = None
        self.cur = None

    def dbConnect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()


class DbQuery(DbManager):

    def query_project_list(self):
        pass

    def query_project_time(self):
        pass

    def query_time_period(self):
        pass


class DbUpdate(DbManager):

    def add_project(self, data: tuple) -> None:
        #  tuple needs to be a string and an int
        self.dbConnect()
        sql_statement = """INSERT INTO projects(name,status) VALUES(?,?)"""
        self.cur.execute(sql_statement, data)
        self.conn.commit()
        self.conn.close()

    def del_project(self):
        pass

    def add_logs(self, data: tuple) -> None:
        #  Tuple needs to be int and two date objects
        self.dbConnect()
        sql_statement = """INSERT INTO time_log(session_id,start_timestamp,end_timestamp) VALUES(?,?,?)"""
        self.cur.execute(sql_statement, data)
        self.conn.commit()
        self.conn.close()

    def update_logs(self):
        pass

    def add_session(self, data: tuple) -> None:
        #  Tuple needs to be int and two datetime objects
        self.dbConnect()
        sql_statement = """INSERT INTO sessions(project_id,start_date,end_date) VALUES(?,?,?)"""
        self.cur.execute(sql_statement, data)
        self.conn.commit()
        self.conn.close()

    def update_session(self):
        pass

    def get_session_id(self):
        pass

    def check_for_project(self):
        # Checks for project name
        pass