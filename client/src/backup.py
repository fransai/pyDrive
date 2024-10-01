import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    creds = None
    if os.path.exists('data/token.pickle'):
        with open('data/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials/client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
        with open('data/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def upload_file(service, file_path, folder_id=None):
    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name}
    
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    media = MediaFileUpload(file_path, resumable=True)
    uploaded_file = service.files().create(
        body=file_metadata, media_body=media, fields='id').execute()
    
    return uploaded_file.get("id")

def backup_files():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    folder_to_backup = "path/to/your/folder"
    backup_files = [os.path.join(folder_to_backup, f) for f in os.listdir(folder_to_backup) if os.path.isfile(os.path.join(folder_to_backup, f))]

    for file_path in backup_files:
        upload_file(service, file_path)
        print(f"{file_path} uploaded successfully.")
