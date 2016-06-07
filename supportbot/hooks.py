# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "supportbot"
app_title = "Supportbot"
app_publisher = "Frappe"
app_description = "Support bot"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hello@frappe.io"
app_version = "0.0.1"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/supportbot/css/supportbot.css"
# app_include_js = "/assets/supportbot/js/supportbot.js"

# include js, css files in header of web template
# web_include_css = "/assets/supportbot/css/supportbot.css"
# web_include_js = "/assets/supportbot/js/supportbot.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "index"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "supportbot.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "supportbot.install.before_install"
# after_install = "supportbot.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "supportbot.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"supportbot.tasks.all"
# 	],
# 	"daily": [
# 		"supportbot.tasks.daily"
# 	],
# 	"hourly": [
# 		"supportbot.tasks.hourly"
# 	],
# 	"weekly": [
# 		"supportbot.tasks.weekly"
# 	]
# 	"monthly": [
# 		"supportbot.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "supportbot.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "supportbot.event.get_events"
# }

