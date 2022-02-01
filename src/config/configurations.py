import os

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))


PRODUCTION_CONFIGURATION = {
    "CONCURRENT_SESSIONS": 10,
    "SESSION_JSON_PATH": "timer_session/sessions.json",
    "TIMER_DB_PATH": "timer_database/timerDatabase.db",
    }

TEST_CONFIGURATION = {
    "CONCURRENT_SESSIONS": 10,
    "SESSION_JSON_PATH": "timer_session/TEST_sessions.json",
    "TIMER_DB_PATH": "timer_database/TEST_timerDatabase.db",
    }
