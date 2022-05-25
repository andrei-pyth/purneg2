from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Gdrive:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.auth()

    def auth(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def take_file_list(self):
        try:
            service = build('drive', 'v3', credentials=self.creds)

            # Call the Drive v3 API
            results = service.files().list(
                pageSize=1000, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                    print(item['name'])
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')


    def make_folder(self, dirname):
        try:
            service = build('drive', 'v3', credentials=self.creds)
            file_metadata = {
            'name': dirname,
            'mimeType': 'application/vnd.google-apps.folder',
        }
            file_metadata['parents'] = ['1jwsdpBXt4PdP9YSHRVEgF6g51tfTEmgn']
            file = service.files().create(body=file_metadata,
                                            fields='id').execute()
            print ('Folder ID: %s' % file.get('id'))
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

