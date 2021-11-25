FORMAT_DICT = {
    'LOG': {
        'REPORT_ROW': {
            'FIELDS': {
                'logID': {
                    'DISPLAY': 'LOG ID',
                    'ALIGN': '^',
                    'LENGTH': 8
                },
                'startTime': {
                    'DISPLAY': 'Start Time',
                    'ALIGN': '^',
                    'LENGTH': 21
                },
                'endTime': {
                    'DISPLAY': 'End Time',
                    'ALIGN': '^',
                    'LENGTH': 21
                },
                'duration': {
                    'DISPLAY': 'DURATION',
                    'ALIGN': '^',
                    'LENGTH': 18
                },
                'percent_session': {
                    'DISPLAY': '%%SESSION',
                    'ALIGN': '^',
                    'LENGTH': 10
                },
                'percent_project': {
                    'DISPLAY': '%PROJECT',
                    'ALIGN': '^',
                    'LENGTH': 10
                },
                'percent_report': {
                    'DISPLAY': '%REPORT',
                    'ALIGN': '^',
                    'LENGTH': 10
                },
                'startLogNote': {
                    'DISPLAY': 'LOG NOTES',
                    'ALIGN': '<',
                    'LENGTH': 20
                },
                'endLogNote': {
                    'ALIGN': '>',
                    'LENGTH': 70
                },
            }
        },
        'SECTION_HEADER': {},
        'REPORT_HEADER': {},
    },
    'SESSION': {},
    'PROJECT': {}
}