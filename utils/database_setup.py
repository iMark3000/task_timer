import sqlite3


def run_db_setup(path):

	conn = sqlite3.connect(path)
	cur = conn.cursor()

	cur.execute(
		"""CREATE TABLE IF NOT EXISTS projects ( 
			id integer PRIMARY Key, 
			name text NOT NULL, 
			status integer NOT NULL)"""
	)
	cur.execute(
		"""CREATE TABLE IF NOT EXISTS sessions (
			id integer PRIMARY Key, 
			project_id integer NOT NULL, 
			start_date date NOT NULL, 
			end_date date NOT NULL, 
			FOREIGN KEY (project_id) REFERENCES projects (id))"""
	)
	cur.execute(
		""""CREATE TABLE IF NOT EXISTS time_log (
			id integer PRIMARY Key, 
			session_id integer NOT NULL, 
			start_timestamp datetime NOT NULL, 
			end_timestamp datetime, 
			FOREIGN KEY (session_id) REFERENCES sessions (id))"""
	)
	conn.commit()
	conn.close()
