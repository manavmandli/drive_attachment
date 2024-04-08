// Copyright (c) 2024, manav and contributors
// For license information, please see license.txt

frappe.ui.form.on("Google Drive Settings", {
	authorize(frm) {
		console.log("call");
		// frm.call({
		// 	method: "authoriztion",
		// 	doc: frm.doc,
		// 	callback: function (r) {},
		// });

		frappe.call({
			method: "authorize_access",
			doc: frm.doc,
			callback: function (r) {
				if (!r.exc) {
					frm.save();
					window.open(r.message.url);
				}
			},
		});
	},
});
