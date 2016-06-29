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

	# rows = frappe.db.sql("SELECT name FROM tabposts;", as_dict=True, debug=True)

	# for row in rows:
	# 	doc = frappe.get_doc('posts', row.name)
	# 	text = doc.raw
	# 	words = text.split()
	# 	tot_words = sum(len(word) for word in words)
	# 	l = len(words)
	# 	if l==0:
	# 		l = 1
	# 	average_word = float(tot_words)/l
	# 	doc.avg_word = float(average_word)

	# 	wordcounts = []
	# 	sentences = text.split('. ')
	# 	for sentence in sentences:
	# 		words = sentence.split(' ')
	# 		wordcounts.append(len(words))
	# 	l = len(wordcounts)
	# 	if l==0:
	# 		l = 1
	# 	average_sentence = float(sum(wordcounts))/l
	# 	doc.avg_sentence = float(average_sentence)

	# doc.save(ignore_permissions=True)
	# frappe.db.commit()
	return



