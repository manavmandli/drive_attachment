import frappe
import os
import mimetypes
from frappe.model.document import Document
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials

# Define the scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

class DriveFileUploader(Document):
	def before_submit(self):
		self.upload_to_drive()


	def upload_to_drive(self):
		google_settings_doc = frappe.get_doc("Google Settings","Google Settings")
		creds = Credentials(
		None,
		refresh_token=frappe.db.get_value("Google Drive","Google Drive","refresh_token"),
		token_uri="https://oauth2.googleapis.com/token",
		client_id=google_settings_doc.get("client_id"),
		client_secret=google_settings_doc.get_password("client_secret")
		)
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
