from __future__ import unicode_literals

import frappe, os

def import_docs():
	frappe.db.sql('delete from `tabAnswer`')
	for basepath, folders, files in os.walk(frappe.get_app_path('erpnext', 'docs', 'user', 'manual', 'en')):
		for f in files:
			if f.endswith('.md'):
				path = os.path.join(basepath, f)
				with open(path, 'r') as docfile:
					frappe.get_doc({
						'doctype': 'Answer',
						'text': unicode(docfile.read(), 'utf-8')
					}).insert()
				print f

	frappe.db.commit()