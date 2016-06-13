# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class posts(Document):
	pass

def on_doctype_update():
	'''create index when posts table is created if missing'''
	if not frappe.db.sql("""show index from `tabposts`
		where Key_name="text_index" """):
		frappe.db.commit()
		frappe.db.sql("""create fulltext index text_index on tabposts (raw);""")

