# # Copyright (c) 2024, manav and contributors
# # For license information, please see license.txt

import frappe
import os
import urllib.request
import mimetypes
import webbrowser
import pickle
from frappe.model.document import Document
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
from frappe.integrations.google_oauth import GoogleOAuth
from urllib.parse import quote


class GoogleDriveSettings(Document):
	@frappe.whitelist(methods=["POST"])
	def authorize_access(self):
		"""
		If no Authorization code get it from Google and then request for Refresh Token.
		Google Contact Name is set to flags to set_value after Authorization Code is obtained.
		"""

		oauth_code = frappe.db.get_single_value("Google Drive Settings", "authorization_code")
		oauth_obj = GoogleOAuth("drive")

		if not oauth_code:
			return oauth_obj.get_authentication_url(
				{
					"redirect": f"/app/Form/{quote('Google Drive Settings')}",
				},
			)

		r = oauth_obj.authorize(oauth_code)
		frappe.db.set_single_value(
			"Google Drive Settings",
			{"authorization_code": oauth_code, "refresh_token": r.get("refresh_token")},
		)
	# @frappe.whitelist()
	# def authoriztion(self):
	# 	client_id = self.client_id
	# 	client_secret = self.client_secret
	# 	project_id = self.project_id
	# 	auth_uri = self.auth_uri
	# 	token_uri = self.token_uri
	# 	auth_provider_x509_cert_url = self.auth_provider_x509_cert_url
	# 	redirect_uri = self.redirect_uri

	# 	creds = None
	# 	token_path = 'token.pickle'  # Path to store the token

	# 	# Load the token if it exists
	# 	if os.path.exists(token_path):
	# 		with open(token_path, 'rb') as token:
	# 			creds = pickle.load(token)

	# 	# If there are no valid credentials available, then authenticate

	# 	if not creds or not creds.valid:
	# 		flow = InstalledAppFlow.from_client_config(
	# 			{
	# 				"web": {
	# 					"client_id": client_id,
	# 					"client_secret": client_secret,
	# 					"project_id": project_id,
	# 					"auth_uri": auth_uri,
	# 					"token_uri": token_uri,
	# 					"auth_provider_x509_cert_url": auth_provider_x509_cert_url,
	# 					"redirect_uris": [redirect_uri],
	# 				}
	# 			},
	# 			scopes=SCOPES,
	# 		)

	# 		creds = flow.run_local_server(port=0)
	# 		print("call")
	# 		# frappe.msgprint(f"Please authenticate and authorize the app: <a href='{authorization_url}' target='_blank'>Click here</a>.")

	# 		with open(token_path, 'wb') as token:
	# 			pickle.dump(creds, token)
	# 	frappe.msgprint("Authorization completed")
