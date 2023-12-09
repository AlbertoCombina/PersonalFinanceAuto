import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


CLIENT_SECRET_FILE = 'secrets_n_tokens\\client_secret_personal_finance_auto.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']


def creds_auth(client_secret, scopes):

    creds = None
    token_path = 'secrets_n_tokens\\token.json'
    # To create auth token
    if not os.path.exists(token_path):
        flow = InstalledAppFlow.from_client_secrets_file(client_secret, scopes)
        creds = flow.run_local_server()
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # Refresh credentials if needed
    creds = Credentials.from_authorized_user_file(token_path, scopes)
    if not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    return creds

def create_service(api_name, api_version, client_secret, scopes):

    creds = creds_auth(client_secret, scopes)
    try:
        service = build(api_name, api_version, credentials=creds)
        print(api_name, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
        

def main():
    
    drive_service = create_service(API_NAME, API_VERSION, CLIENT_SECRET_FILE, SCOPES)
    print(drive_service)


if __name__ == "__main__":
    main()