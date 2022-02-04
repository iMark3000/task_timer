from .command_handler_base_class import Handler
from src.timer_database.dbManager import DbUpdate
from src.timer_database.dbManager import DbQueryUtility
from ...command_classes.utility_commands import UtilityCommand

from src.timer_session.sessions_manager import SessionManager
from src.timer_session.sessions_manager import FetchSessionHelper
from src.utils.command_enums import InputType


class UtilityCommandHandler(Handler):

    def __init__(self, command: UtilityCommand, session_manager: SessionManager):
        self.session_manager = session_manager
        self.command = command

    def handle(self):
        if self.command.command == InputType.FETCH:
            self._fetch_project()
        elif self.command.command == InputType.STATUS:
            self._status_check()
        elif self.command.command == InputType.NEW:
            self._new_project()
        elif self.command.command == InputType.PROJECTS:
            self._get_projects()
        elif self.command.command == InputType.SWITCH:
            self._switch_project()

    def _fetch_project(self):
        project_id = (self.command.project_id,)
        results = DbQueryUtility().fetch_project(project_id)
        project_name = results[1]
        if FetchSessionHelper(project_name, self.command.project_id, self.session_manager).fetch():
            self.session_manager.export_sessions_to_json()
            print(f'Fetched {project_name} -- Use "SWITCH {self.command.project_id}" to make it current')
        else:
            print(f'{project_name} [ID: {self.command.project_id}] is already in queue')

    def _new_project(self):
        tup = (self.command.project_name, 1)
        project = DbUpdate().create_project(tup)
        print(f'{self.command.project_name} [ID: {project}] created!!!')

    def _status_check(self):
        # Todo: This will need to be reworked later
        session = self.session_manager.get_current_session()
        if session is None:
            print('No sessions are in progress')
        elif session.project_name and session.last_command != InputType.NO_SESSION:
            print(f'\nCurrent project: {session.project_name}')
            print(f'Session started on {session.session_start_time}')
            print(f'\nLast command: {session.last_command.name.upper()}')
            print(f'Last command time: {session.last_command_time}')
            print(f'\nThere are {self.session_manager.count_of_concurrent_sessions()} concurrent sessions.')
            self.session_manager.display_sessions()
        elif session.project_name:
            print(f'Project Queued Up: {session.project_name}')
            print(f'No session in progress')
            print(f'There are {self.session_manager.count_of_concurrent_sessions()} concurrent session(s).')
            self.session_manager.display_sessions()

    def _get_projects(self):
        # Todo: break this up
        if self.command.is_all():
            result = DbQueryUtility().query_all_projects()
            header = 'Here are ALL projects in database:'
        else:
            if self.command.filter_by == 0:
                result = DbQueryUtility().query_projects_by_status(0)
                header = 'Here are DEACTIVATED projects in database:'
            else:
                result = DbQueryUtility().query_projects_by_status(1)
                header = 'Here are ACTIVE projects in database:'

        print(header)
        print("====================")
        for r in result:
            print(f'{r[0]}......{r[1]}')

    def _switch_project(self):
        if self.session_manager.check_for_session(self.command.project_id):
            self.session_manager.switch_current_session(self.command.project_id)
            self.session_manager.export_sessions_to_json()
            print(f'{self.command.project_name} is queued up! Use START to start a session.')
        else:
            print(f'{self.command.project_id} is not in queue. Use FETCH to add project or NEW to create project.')
