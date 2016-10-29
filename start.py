import httplib2
import os

import parser
import json
from datetime import date
# for testing
import pprint

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_config():
    f = open("config.json")
    data = json.load(f)
    return data

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
config_vars = get_config()
SCOPES = 'https://www.googleapis.com/auth/spreadsheets' # rw permissions
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'work log uploader'

SPREADSHEET_ID=config_vars.get('spreadsheet_id')

def get_credentials():
    global config_vars
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, config_vars.get('local_oauth_filename'))
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

def main():
    global config_vars
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = config_vars.get('spreadsheet_id')

    commits = fetch_logs()
    tasks = {}
    for commit in commits:
        temp = commit.split(" ")
        k, v = temp[0], " ".join(temp[1:])
        if k not in tasks:
            tasks[k] = [v]
        else:
            tasks[k].append(v)
    # note dict sorted can be used only because format is already in y-m-d
    # and left padded with 0s
    tasks = [[conv_date(k), flatten_with_index(v)] for k, v in sorted(tasks.items())]
    body = {'values': tasks}

    writerange = 'Sheet1' # ref https://developers.google.com/sheets/guides/concepts
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range=writerange,
        valueInputOption='RAW', body=body).execute()


def flatten_with_index(l):
    global config_vars
    r = []
    authorname = "(" + config_vars.get('git_author_name') + ")"
    for i, e in enumerate(l):
        if e.endswith(authorname):
            r.append(str(i+1) + ". " + e[:-len(authorname)-1])
    return " ".join(r)

def fetch_logs():
    p = parser.Parse()
    files = p.filenames("logs")
    logs = []
    for f in files:
        logs.extend(p.readfile("logs/" + f))
    return logs

def conv_date(d):
    y, m, d = [int(s) for s in d.split("-")]
    date_obj = date(y, m, d)
    return date_obj.strftime("%d-%b-%y")

if __name__ == '__main__':
    main()
