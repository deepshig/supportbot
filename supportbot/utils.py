#!/usr/bin/python

from __future__ import unicode_literals

import os

import frappe
from frappe.utils import now

import psycopg2 

def import_posts():
	conn = psycopg2.connect(database="supportbot", user="postgres", password="qwe", host="127.0.0.1", port="5432")
	print "Opened database successfully"

	cur = conn.cursor()
	#input_string = raw_input("Input your query.. ")
	#print input_string


	cur.execute("SELECT id, like_score, reads, word_count, created_at, reply_to_post_number, incoming_link_count, raw, is_doc, fitness FROM posts;")
	rows = cur.fetchall()

	frappe.db.sql('DELETE FROM tabposts;')
	print "Hello"
	# i=1

	for row in rows:
		iden = row[0]  
		read = row[2]
		likes = row[1]
		word = row[3]
		create_date = row[4]
		reply = row[5]
		link = row[6]
		data = unicode(row[7], 'utf-8')
		doc = row[8]
		fit = float(row[9])	

		frappe.get_doc({
				'doctype': 'posts',
				'id': iden,
				'raw': data,
				'created_at': create_date,
				'reply_to_post_number': reply,
				'incoming_link_count': link,
				'reads': read,
				'like_score': likes,
				'word_count': word,
				'fitness': fit,
				'is_doc': doc,
				'no_reviewed': 0
			}).insert()
		print "Inserted!"
		
	print "\n All done!"
	conn.close()
	frappe.db.commit()
	return

def import_docs():
	out = frappe.db.sql("""SELECT AVG(`reads`) AS avg_r, AVG(like_score) AS avg_l, AVG(incoming_link_count) AS avg_in FROM tabposts;""", as_dict=True, debug=True)

	for root, dirs, files in os.walk("/home/frappe-office/en"):
		for file in files:
			if file.endswith(".md"):
				file_path = os.path.join(root, file)
				with open(file_path, 'r') as content_file:
					content = content_file.read()
					frappe.get_doc({
							'doctype': 'posts',
							'raw': unicode(content, 'utf-8'),
							'created_at': now(),
							'reply_to_post_number': 0,
							'incoming_link_count': out[0].avg_in,
							'reads': out[0].avg_r,
							'like_score': out[0].avg_l,
							'word_count': len(content.split()),
							'fitness': 0.0,
							'is_doc': 1,
							'no_reviewed': 0
						}).insert()

	print "All done!"
	frappe.db.commit()
	return

def update_avg_word_sentence():
	rows = frappe.db.sql("SELECT name FROM tabposts WHERE avg_word = 0.0 AND word_count <> 0;", as_dict=True, debug=True)
	
	for row in rows:		
		doc = frappe.get_doc('posts', row.name)
		print doc.id
		text = doc.raw
		words = text.split()
		tot_words = sum(len(word) for word in words)
		l = len(words)
		if l==0:
			l = 1
		average_word = float(tot_words)/l
		print "average word = ", average_word
		doc.avg_word = float(average_word)

		wordcounts = []
		sentences = text.split('. ')
		for sentence in sentences:
			words = sentence.split(' ')
			wordcounts.append(len(words))
		l = len(wordcounts)
		if l==0:
			l = 1
		average_sentence = float(sum(wordcounts))/l
		print "average sentence = ", average_sentence
		doc.avg_sentence = float(average_sentence)
		doc.save(ignore_permissions=True)
		frappe.db.commit()

	return



