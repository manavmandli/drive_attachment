# # Copyright (c) 2024, manav and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document

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
