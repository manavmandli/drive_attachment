frappe.provide("Drive Attachment");

drive_attachment.drive_file_uploader = {
	onload: function (frm) {
		frappe.ui.form.on("Drive File Uploader", {
			onload: function (frm) {
				frm.page.set_primary_action(__("Submit"), function () {
					frappe.call({
						method: "drive_attachment.drive_file_uploader.upload_to_drive",
						args: {},
						callback: function (response) {
							var authentication_url = response.message;
							if (authentication_url) {
								window.open(authentication_url, "_blank");
							} else {
								frappe.msgprint("Error: Authentication URL not found.");
							}
						},
					});
				});
			},
		});
	},
};
