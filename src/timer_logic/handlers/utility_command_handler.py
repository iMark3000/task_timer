from .command_handler_base_class import Handler
from src.timer_database.dbManager import DbUpdate
from src.timer_database.dbManager import DbQueryUtility

from ...command_classes.utility_commands import UtilityCommand
from ...command_classes.utility_commands import StatusCheck
from ...command_classes.utility_commands import ProjectsCommand
from ...command_classes.utility_commands import NewCommand
from ...command_classes.utility_commands import FetchProject
from ...command_classes.utility_commands import SwitchCommand

from src.timer_session.sessions_manager import SessionManager
from src.timer_session.sessions_manager import FetchSessionHelper
from src.utils.command_enums import InputType


class UtilityCommandHandler(Handler):

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    def handle(self, command: UtilityCommand):
        if isinstance(command, FetchProject):
            self._fetch_project(command)
        elif isinstance(command, StatusCheck):
            self._status_check()
        elif isinstance(command, NewCommand):
            self._new_project(command)
        elif isinstance(command, ProjectsCommand):
            self._get_projects(command)
        elif isinstance(command, SwitchCommand):
            self._switch_project(command)

    def _fetch_project(self, command: FetchProject):
        project_id = (command.project_id,)
        results = DbQueryUtility().fetch_project(project_id)
        project_name = results[1]
        if FetchSessionHelper(project_name, command.project_id, self.session_manager).fetch():
            self.session_manager.export_sessions_to_json()
            print(f'Fetched {project_name} -- Use "SWITCH {command.project_id}" to make it current')
        else:
            print(f'{project_name} [ID: {command.project_id}] is already in queue')

    @staticmethod
    def _new_project(command: NewCommand):
        tup = (command.project_name, 1)
        project = DbUpdate().create_project(tup)
        print(f'{command.project_name} [ID: {project}] created!!!')

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

    @staticmethod
    def _get_projects(command: ProjectsCommand):
        # Todo: break this up
        if command.is_all():
            result = DbQueryUtility().query_all_projects()
            header = 'Here are ALL projects in database:'
        else:
            if command.filter_by == 0:
                result = DbQueryUtility().query_projects_by_status(0)
                header = 'Here are DEACTIVATED projects in database:'
            else:
                result = DbQueryUtility().query_projects_by_status(1)
                header = 'Here are ACTIVE projects in database:'

        print(header)
        print("====================")
        for r in result:
            print(f'{r[0]}......{r[1]}')

    def _switch_project(self, command: SwitchCommand):
        if self.session_manager.check_for_session(command.project_id):
            self.session_manager.switch_current_session(command.project_id)
            self.session_manager.export_sessions_to_json()
            print(f'{command.project_id} is queued up! Use START to start a session.')
        else:
            print(f'{command.project_id} is not in queue. Use FETCH to add project or NEW to create project.')
