import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    """
    Generic function to handle authentican, authorization, setup for Google APIs

    Given a google drive folder id(source), generate a report in the current
    current working directory which displays the number of files and folders
    within the source folder.

    Parameters:
    client_secret_file(string): name of local credentials.file

    api_name (string): Google api resource name

    api_version (string): Google api version

    scopes(string, one or more, list): authorization scope for the program

    Returns:
    google drive api service

    """


    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None
    #create a pickle fgile to hold credentials
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    #grab info from file if exits
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    #if token has expired, refresh or create new credentials
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server(authorization_prompt_message="")

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
