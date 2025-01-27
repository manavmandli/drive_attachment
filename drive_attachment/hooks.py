app_name = "drive_attachment"
app_title = "Drive Attachment"
app_publisher = "manav"
app_description = "Drive Attachment Application"
app_email = "manavmandli2990@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/drive_attachment/css/drive_attachment.css"
# app_include_js = "/assets/drive_attachment/js/drive_attachment.js"

# include js, css files in header of web template
# web_include_css = "/assets/drive_attachment/css/drive_attachment.css"
# web_include_js = "/assets/drive_attachment/js/drive_attachment.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "drive_attachment/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "drive_attachment/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "drive_attachment.utils.jinja_methods",
# 	"filters": "drive_attachment.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "drive_attachment.install.before_install"
# after_install = "drive_attachment.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "drive_attachment.uninstall.before_uninstall"
# after_uninstall = "drive_attachment.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "drive_attachment.utils.before_app_install"
# after_app_install = "drive_attachment.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "drive_attachment.utils.before_app_uninstall"
# after_app_uninstall = "drive_attachment.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "drive_attachment.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
doc_events = {
    "File": {
        "after_insert": "drive_attachment.controller.file_upload_to_gd",
        "on_trash": "drive_attachment.controller.delete_from_gd"
    }
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"drive_attachment.tasks.all"
# 	],
# 	"daily": [
# 		"drive_attachment.tasks.daily"
# 	],
# 	"hourly": [
# 		"drive_attachment.tasks.hourly"
# 	],
# 	"weekly": [
# 		"drive_attachment.tasks.weekly"
# 	],
# 	"monthly": [
# 		"drive_attachment.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "drive_attachment.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "drive_attachment.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "drive_attachment.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["drive_attachment.utils.before_request"]
# after_request = ["drive_attachment.utils.after_request"]

# Job Events
# ----------
# before_job = ["drive_attachment.utils.before_job"]
# after_job = ["drive_attachment.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"drive_attachment.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

