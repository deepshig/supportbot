#!/usr/bin/python

from __future__ import unicode_literals

import frappe, os

import psycopg2 

def import_posts():
	conn = psycopg2.connect(database="supportbot", user="postgres", password="deep", host="127.0.0.1", port="5432")
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
		#rank = float(row[10])
		# print iden
		# print read
		# print likes
		# print word
		# print create_date
		# print reply
		# print link
		# print doc
		# print fit
		# print rank
		# print data	

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
		# print str(i) + " : Inserted!"
		# i = i+1
		print "Inserted!"
		
	print "\n All done!"
	#conn.commit()
	conn.close()
	frappe.db.commit()

