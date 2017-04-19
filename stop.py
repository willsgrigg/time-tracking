#!/bin/python
import httplib2
import os
import datetime
import re

import base

def stop():
    current_row = base.get_current_row()

    body = {
      'values': [
            [
                datetime.datetime.now().strftime("%H:%M:%S"),
                '=IF(AND(NOT(ISBLANK(D' + current_row + ')),NOT(ISBLANK(E' + current_row + '))),SUM(E' + current_row + '-D' + current_row + '),0)'
            ]
        ]
    }

    base.SERVICE.spreadsheets().values().append(
        spreadsheetId=base.config.SPREADSHEET_ID, range='Times!E' + current_row + ':F' + current_row,
        valueInputOption=base.VALUE_INPUT_OPTION, body=body).execute()

    base.set_recording(False)

def main():
    if base.is_recording():
        base.authenticate()

        stop()


if __name__ == '__main__':
    main()
