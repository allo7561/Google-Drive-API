def upload_basic(filename, file_to_upload, new_folder):
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
        # pull the uploaded file name and path, along with the new folder id and feed it into the metadata for the new drive upload
        file_metadata = {'name': f'{filename}',
                        'parents': [f'{new_folder}']}
        # media object
        media = MediaFileUpload(f'{file_to_upload}')
        # uploads the file
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')