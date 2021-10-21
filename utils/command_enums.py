from enum import Enum, auto


class InputType(Enum):
    START = auto()  # Start new session
    PAUSE = auto()  # Pause session
    RESUME = auto()  # Resume Session
    STOP = auto()   # Stop (Ends) Session
    STATUS = auto()  # If session in prog, gets status
    NEW = auto()    # Creates new project
    PROJECTS = auto()   # Gets a list of projects and their IDS
    FETCH = auto()  # Fetches a project by an ID number to start session with
    MERGE = auto()
    LOG = auto()
    REPORT = auto()
    NO_SESSION = auto() # Placeholder value for when no session is in progress
