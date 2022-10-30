# class for creating Google Drive folder objects
class Drive_folder:
    # init method takes in the folder id from the user
    def __init__(self, user_input_folder_id= '', file_names= [], file_ids= []):
        # declares all the instance variables
        self.file_names = file_names
        self.file_ids = file_ids
        self.user_input_folder_id = user_input_folder_id
        # imports all the necessary libraries
        import os.path
        import io
        import google.auth
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        from googleapiclient.http import MediaIoBaseDownload
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
        # creates the implementation of the API
        try:
            service = build('drive', 'v3', credentials=creds)   
            page_token = None
            #finds the files in in provided folder id
            folder_finder = service.files().list(
                                            q=f"parents in '{user_input_folder_id}'",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                       'files(id, name, webContentLink, thumbnailLink)',
                                            pageToken=page_token
                                               ).execute()
            #stores all the found items as dictionaries within a list
            self.file_names = folder_finder['files']
            #cycle through dictionaries and appends the necessary info to the instance lists
            #for file_dictionary in file_dictionaries:
                #self.file_names.append(file_dictionary['name'])
                #self.file_ids.append(file_dictionary['id'])
        # handles errors        
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    # method for listing the name of each file in the folder
    def file_lister(self):
        
        # calls on this instance list from the current object
        file_names = self.file_names
        # prints the file names
        return file_names

    
    # method for listing the url to each file in the folder
    def link_lister(self):
        # calls on this instance list from the current object
        file_ids = self.file_ids
        # prints the URLs
        print('VIEWABLE LINKS:')  
        for file_id in file_ids:
            url = f'https://drive.google.com/file/d/{file_id}/view?usp=sharing'
            print(url)

    # method for downloading all the files in the user's folder
    def file_downloader(self):
        # Since we are calling the API in a different way, I need to import the API libraries again
        import os.path
        import io
        import google.auth
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        from googleapiclient.http import MediaIoBaseDownload
        # Set the scopes for token
        SCOPES = ['https://www.googleapis.com/auth/drive']
        # call on the lists of metadata for the files in the user's folder
        file_ids = self.file_ids
        file_names = self.file_names
        # build the credentials from the token & scope
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # cycle through all the found files
        for file_id in file_ids:
            # establish service connection
            service = build('drive', 'v3', credentials=creds)   
            page_token = None
            # create a variable that stores the current index value from the list of files
            found_index = file_ids.index(file_id)
            # call the current file
            request = service.files().get_media(fileId=file_id)
            # download flow
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')
            file.seek(0)
            # saves the download to the specified folder and pulls the name from the found name
            with open(os.path.join('./downloads', file_names[found_index]), 'wb') as f:
                f.write(file.read())
                f.close()

    