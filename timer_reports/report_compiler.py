from datetime import timedelta
from format_dict import FORMAT_DICT


class SummerizeReport:

    def __init__(self, report):
        self.report = report
        self.report_duration = None

    def duration_project_iter(self):
        for project in self.report.get_projects():
            duration = self.duration_session_iter(project.get_sessions())
            project.add_to_summary('duration', duration)
            project.add_to_summary('session_count', project.count_of_sessions())
            project.add_to_summary('PROJECT NAME', project.project_name)
            project.add_to_summary('project id', project.project_id)
            if self.report_duration is None:
                self.report_duration = duration
            else:
                self.report_duration += duration
        self.report.summary['report duration'] = self.report_duration
        self.report.summary['project count'] = len(self.report.project_reports)

    def duration_session_iter(self, sessions: list):
        total_session_duration = None
        for session in sessions:
            logs = session.get_logs()
            duration = self.sum_session_duration(logs)
            session.add_to_summary('duration', duration)
            session.add_to_summary('log_count', session.count_of_logs())
            session.add_to_summary('session', session.session_id)
            if total_session_duration is None:
                total_session_duration = duration
            else:
                total_session_duration += duration

        return total_session_duration

    def sum_session_duration(self, logs):
        session_duration = None
        for log in logs:
            if session_duration is None:
                session_duration = log['duration']
            else:
                session_duration += log['duration']
        return session_duration

    def percent_project_iter(self):
        for project in self.report.get_projects():
            self.percent_session_iter(project.get_sessions(), project.summary['duration'])
            project.summary['percent_report'] = self.calculate_percentage(project.summary['duration'],
                                                                          self.report_duration)

    def percent_session_iter(self, sessions, project_total):
        for session in sessions:
            for log in session.get_logs():
                log['percent_session'] = self.calculate_percentage(log['duration'], session.summary['duration'])
                log['percent_project'] = self.calculate_percentage(log['duration'], project_total)
                log['percent_report'] = self.calculate_percentage(log['duration'], self.report_duration)
            session.summary['percent_report'] = self.calculate_percentage(session.summary['duration'], project_total)
            session.summary['percent_project'] = self.calculate_percentage(session.summary['duration'],
                                                                           self.report_duration)

    def calculate_percentage(self, t1, t2):
        return round((t1 / t2 * 100), 2)

    def process_report(self):
        self.duration_project_iter()
        self.percent_project_iter()


class PrintReport:

    def __init__(self, report, detail_level):
        self.report = report
        self.detail_level = detail_level
        self.format_report_row = FORMAT_DICT[detail_level]['REPORT_ROW']
        self.format_section_header = FORMAT_DICT[detail_level]['SECTION_HEADER']
        self.format_report_header = FORMAT_DICT[detail_level]['REPORT_HEADER']

    def print_report(self):
        if self.detail_level == 'LOG':
            self._process_log_level()
        elif self.detail_level == 'SESSION':
            pass
        elif self.detail_level == 'PROJECT':
            pass

    def report_header(self, summary):
        print('\nTHIS IS THE REPORT HEADER')
        # print(summary)

    def section_header(self, summary):
        print('\nTHIS IS THE SECTION HEADER')
        # print(summary)
        print('\n')

    def print_column_headers(self):
        line = ''
        for k, v in self.format_report_row['FIELDS'].items():
            if 'DISPLAY' in v.keys():
                column_header = v['DISPLAY']
                align = v['ALIGN']
                length = v['LENGTH']
                line += '{0:{fill}{align}{length}}'.format(column_header, fill='', align=align, length=length-1) + '|'
        print(line)

    def report_row(self, row):
        line = ''
        end_note = None
        for column, form in self.format_report_row['FIELDS'].items():
            if column in row.keys():
                value = row[column]
                if column == 'endLogNote' and value is None:
                    pass
                elif column == 'endLogNote' and value is not None:
                    value = 'END: ' + value[:16]
                    formatting = form
                    align = formatting['ALIGN']
                    length = formatting['LENGTH']
                    end_note = '\n{0:{fill}{align}{length}}'.format(value, fill='', align=align, length=length)
                else:
                    if column == 'startLogNote' and value is None:
                        pass
                    elif column == 'startLogNote' and value is not None:
                        value = 'START: ' + value[:13]
                        formatting = form
                        align = formatting['ALIGN']
                        length = formatting['LENGTH']
                        line += '{0:{fill}{align}{length}}'.format(value, fill='', align=align, length=length)
                    else:
                        value = str(value)
                        formatting = form
                        align = formatting['ALIGN']
                        length = formatting['LENGTH']
                        line += '{0:{fill}{align}{length}}'.format(value, fill='', align=align, length=length)
        print(line)

    def _process_log_level(self):
        breaker = '=' * 118
        self.report_header(self.report.summary)
        print('\n')
        for project in self.report.get_projects():
            self.section_header(project.summary)
            print('\n')
            for session in project.get_sessions():
                self.section_header(session.summary)
                self.print_column_headers()
                print(breaker)
                for log in session.get_logs():
                    self.report_row(log)
