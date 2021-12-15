
def report_header_footer(width, footer=False, **fields):
    width = width - 2
    if footer:
        footer_title = ' REPORT SUMMARY '
    else:
        footer_title = ''

    first_line = '| ' +'{0:{fill}{align}{length}}'.format(footer_title, fill='*', align='^', length=width ) +'|'
    print(first_line)

    for key, value in fields.items():
        if 'count' in key:
            print('|' + '{0:{fill}{align}{length}}'.format('', fill='', align='<', length=width) + '|')
        field = f'{key}: {value}'
        field_formatted = '{0:{fill}{align}{length}}'.format(field, fill='', align='<', length=width)
        line ='|' + field_formatted + '|'
        print(line)

    print('|' + '{0:{fill}{align}{length}}'.format('', fill='*', align='^', length=width) + '|')

