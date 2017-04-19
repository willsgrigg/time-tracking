from __future__ import print_function
import sys
import httplib2
import os
import datetime
import re
from Tkinter import *

import config

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets Time Tracking'
VALUE_INPUT_OPTION = 'USER_ENTERED'
RECORDING = 'data/recording.txt'
CURRENT_ROW = 'data/current_row.txt'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-timetracking.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def authenticate():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')

    global SERVICE

    SERVICE = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

def is_recording():
    with open(RECORDING) as f:
        recording = f.readline()

    if recording == 'True':
        return True
    else:
        return False

def set_recording(recording):
    file = open(RECORDING, 'w')

    file.truncate()

    file.write(str(recording))

def set_current_row(row):
    file = open(CURRENT_ROW, 'w')

    file.truncate()

    file.write(str(row))

def get_current_row():
    with open(CURRENT_ROW) as f:
        current_row = f.readline()

    return current_row

def get_last_n_projects(n):
    return get_last_n_rows_for_column(n,'A');

def get_last_n_tasks(n):
    return get_last_n_rows_for_column(n,'B');

def get_last_n_rows_for_column(n,column):
    current = get_current_row()

    prev = int(current) - n

    if prev < 2:
        prev = 2

    range = 'Times!' + column + current + ':' + column + str(prev)

    result = SERVICE.spreadsheets().values().get(
        spreadsheetId=config.SPREADSHEET_ID, range=range).execute()

    values = result.get('values', [])

    return values;
