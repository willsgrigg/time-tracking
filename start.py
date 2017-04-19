#!/usr/bin/python
import httplib2
import os
import datetime
import re

import base

import rumps

def start():
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    projects = base.get_last_n_projects(5)

    projectsString = ''

    for project in reversed(projects):
        try:
            projectsString += project[0] + '\n'
        except (ValueError,IndexError):
            pass

    tasks = base.get_last_n_tasks(5)

    tasksString = ''

    for task in reversed(tasks):
        try:
            tasksString += task[0] + '\n'
        except (ValueError,IndexError):
            pass

    project = rumps.Window('Last five projects:\n\n' + projectsString, 'Project').run().text
    task = rumps.Window('Last five tasks:\n\n' + tasksString, 'Task').run().text

    body = {
      'values': [
            [
                project,
                task,
                datetime.datetime.now().strftime("%d/%m/%Y"),
                datetime.datetime.now().strftime("%H:%M:%S")
            ]
        ]
    }

    result = base.SERVICE.spreadsheets().values().append(
        spreadsheetId=base.config.SPREADSHEET_ID, range='Times!A1:D1',
        valueInputOption=base.VALUE_INPUT_OPTION, body=body).execute()

    if not result:
        print('Data not updated.')
    else:
        updates = result.get('updates', [])

        updated_range = updates.get('updatedRange', [])

        current_row = re.findall(r"(?!![A-Z])[0-9]+(?=:)", updated_range)
        current_row = ''.join(current_row)

        base.set_current_row(current_row)
        base.set_recording(True)

        rumps.title = 'Currently recording...'

def main():
    base.authenticate()

    if base.is_recording():
        import stop

        stop.stop()

    start()


if __name__ == '__main__':
    main()
