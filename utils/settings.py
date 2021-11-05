import os

#  Todo: What is the right way to do this?
#  PATHS
PROJECT_PATH = '/home/m/PycharmProjects/timer_log'
SESSION_JSON_PATH = os.path.join(PROJECT_PATH, 'timer_session/current_session.json')
TIMER_DB_PATH_PROD = os.path.join(PROJECT_PATH, 'timer_database/timerDatabase.db')
TIMER_DB_PATH_TEST = os.path.join(PROJECT_PATH, 'timer_database/TEST_timerDatabase.db')
TEST_ON = False
