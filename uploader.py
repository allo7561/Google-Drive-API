
class Uploader:
    # init method takes in the folder id from the user
    def __init__(self):
        self = self
        
        
    def folder_maker(self):  
        import os.path
        import io
        import google.auth
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        from googleapiclient.http import MediaFileUpload
        from datetime import datetime
        
        # sets the scopes for OAuth credentials
        SCOPES = ['https://www.googleapis.com/auth/drive']
        # declares creds variable
        creds = None
        # checks if the json token exists, and if it does, creates credentials together with the scopes
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials from a token available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # declares the flow, takes in scopes and credentials
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                # declares the creds, which are pulled from the flow
                creds = flow.run_local_server(port=0)
            # writes the token file from the creds
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        # use the token to create credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        
        
        try:
            # create drive api client
            service = build('drive', 'v3', credentials=creds)
            # pulls the current datetime
            current_datetime = datetime.now()
            if current_datetime.month < 10:
                current_datetime_month = f'0{current_datetime.month}'
            else:
                current_datetime_month = f'{current_datetime.month}'
            if current_datetime.hour < 10:
                current_datetime_hour = f'0{current_datetime.hour}'
            else:
                current_datetime_hour = f'{current_datetime.hour}'
            if current_datetime.minute < 10:
                current_datetime_minute = f'0{current_datetime.minute}'
            else:
                current_datetime_minute = f'{current_datetime.minute}'
            # creates a string for pulling the date and time info into, to build a folder name
            folder_name = f'{current_datetime.year}_{current_datetime_month}{current_datetime.day}-{current_datetime_hour}{current_datetime_minute}'
            # creates folder metadata, based off the date time
            file_metadata = {
                'name': f'{folder_name}',
                'mimeType': 'application/vnd.google-apps.folder'
            }

            #creates the folder
            file = service.files().create(body=file_metadata, fields='id'
                                          ).execute()


        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file.get('id')
    

