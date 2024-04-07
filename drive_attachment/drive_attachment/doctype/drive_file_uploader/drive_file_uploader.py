import frappe
import os
import mimetypes
import pickle
from frappe.model.document import Document
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Define the scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

class DriveFileUploader(Document):
    def before_submit(self):
        authentication_url= self.upload_to_drive()
        frappe.msgprint(f"Please authenticate and authorize the app: <a href='{authentication_url}' target='_blank'>Click here</a>.")

    def upload_to_drive(self):
        google_drive_settings = frappe.get_single("Google Drive Settings")

        client_id = google_drive_settings.client_id
        client_secret = google_drive_settings.client_secret
        project_id = google_drive_settings.project_id
        auth_uri = google_drive_settings.auth_uri
        token_uri = google_drive_settings.token_uri
        auth_provider_x509_cert_url = google_drive_settings.auth_provider_x509_cert_url
        redirect_uri = google_drive_settings.redirect_uri

        creds = None
        token_path = 'token.pickle'  # Path to store the token

        # Load the token if it exists
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        # If there are no valid credentials available, then authenticate
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_config(
                {
                    "web": {
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "project_id": project_id,
                        "auth_uri": auth_uri,
                        "token_uri": token_uri,
                        "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
                        "redirect_uris": [redirect_uri],
                    }
                },
                scopes=SCOPES,
            )
            creds = flow.run_local_server(port=8000,launch_browser=False)
            frappe.msgprint(f"{creds}")
            authentication_url = flow.authorization_url[0]  # Get the first URL in the authorization URL list

            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            return authentication_url



        # Build the Google Drive service
        service = build("drive", "v3", credentials=creds)

        # Get file metadata and content type
        file_path = get_absolute_path(self.select_file)
        file_name = os.path.basename(file_path)
        content_type, _ = mimetypes.guess_type(file_path)
        folder_id = "1Uelmal_XDRpkLphWYbL98R9sOjj6ctaM"
        file_metadata = {"name": file_name, 'parents': [folder_id]}

        # Upload file to Google Drive
        with open(file_path, "rb") as file_content:
            media = MediaIoBaseUpload(file_content, mimetype=content_type)
            file = service.files().create(
                body=file_metadata, media_body=media, fields="id"
            ).execute()

            file_id = file.get('id')
            file_url = f"https://drive.google.com/file/d/{file_id}/view"
            frappe.msgprint(f"File uploaded successfully to Google Drive. Google Drive Path: {file_url}")
            self.drive_file_link = file_url

def get_absolute_path(file_name):
    if(file_name.startswith('/files/')):
        file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}/public{file_name}'
    if(file_name.startswith('/private/')):
        file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}{file_name}'
    return file_path

