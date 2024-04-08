import frappe
import os
import mimetypes
from frappe.model.document import Document
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

# Define the scope for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

def delete_from_gd(doc, method=None):
	"""Delete file from s3"""
	if doc.file_url:
		# Extract file ID from the Google Drive link
		file_id = doc.file_url.split('/')[-2]
		delete_from_drive(file_id)

def delete_from_drive(file_id):
	"""
	Deletes a file from Google Drive using its file ID.
	"""
	google_settings_doc = frappe.get_doc("Google Settings", "Google Settings")
	creds = Credentials(
		None,
		refresh_token=frappe.db.get_value("Google Drive", "Google Drive", "refresh_token"),
		token_uri="https://oauth2.googleapis.com/token",
		client_id=google_settings_doc.get("client_id"),
		client_secret=google_settings_doc.get_password("client_secret")
	)
	service = build("drive", "v3", credentials=creds)

	try:
		service.files().delete(fileId=file_id).execute()
	except Exception as e:
		frappe.msgprint("Error in google drive file delete")

def file_upload_to_gd(doc,method):
	"""
	check and upload files to s3. the path check and
	"""
	path = doc.file_url
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
	file_path = get_absolute_path(path)
	file_name = os.path.basename(file_path)
	content_type, _ = mimetypes.guess_type(file_path)
	folder=frappe.db.get_value('Google Drive Settings','Google Drive Settings','folder_name')
	folder_id = folder
	file_metadata = {"name": file_name, 'parents': [folder_id]}
	parent_doctype = doc.attached_to_doctype or 'File'
	parent_name = doc.attached_to_name

	# Upload file to Google Drive
	with open(file_path, "rb") as file_content:
		media = MediaIoBaseUpload(file_content, mimetype=content_type)
		file = service.files().create(
			body=file_metadata, media_body=media, fields="id"
		).execute()

		file_id = file.get('id')
		file_url = f"https://drive.google.com/file/d/{file_id}/view"

		os.remove(file_path)
		frappe.db.sql("""UPDATE `tabFile` SET file_url=%s, folder=%s,
			old_parent=%s WHERE name=%s""", (
			file_url, 'Home/Attachments', 'Home/Attachments', doc.name))

		doc.file_url = file_url

		if parent_doctype and frappe.get_meta(parent_doctype).get('image_field'):
			frappe.db.set_value(parent_doctype, parent_name, frappe.get_meta(parent_doctype).get('image_field'), file_url)

		frappe.db.commit()


def get_absolute_path(file_name):
	if(file_name.startswith('/files/')):
		file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}/public{file_name}'
	if(file_name.startswith('/private/')):
		file_path = f'{frappe.utils.get_bench_path()}/sites/{frappe.utils.get_site_base_path()[2:]}{file_name}'
	return file_path
