from enum import Enum, auto


class InputType(Enum):
    START = auto()  # Start new session
    PAUSE = auto()  # Pause session
    RESUME = auto()  # Resume Session
    STOP = auto()   # Stop (Ends) Session
    STATUS = auto()  # If session in prog, gets status
    NEW = auto()    # Creates new project
    PROJECTS = auto()   # Gets a list of projects and their IDS -> add optional arg to filter by name
    FETCH = auto()  # Fetches a project by an ID number to start session with
    DEACTIVATE = auto()  # Deactivates projects
    REACTIVATE = auto()  # Reactivates projects that been deactivated
    SWITCH = auto()  # Switches Queued Project...to use when multiples sessions feature is implemented
    MERGE = auto()  # Merges two projects (their sessions and logs) into one project
    LOG = auto()
    REPORT = auto()
    NO_SESSION = auto() # Placeholder value for when no session is in progress
