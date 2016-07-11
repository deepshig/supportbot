#!/usr/bin/python

import numpy as np
import random
import frappe

max_answers = 15

@frappe.whitelist(allow_guest=True)
def neural_network(question):

	y = []
	name1 = []

	out = frappe.db.sql("""SELECT name, fitness, MATCH(raw) AGAINST(%s IN NATURAL LANGUAGE MODE) AS score FROM tabposts WHERE MATCH(raw) AGAINST(%s IN NATURAL LANGUAGE MODE) ORDER BY (score * fitness) DESC LIMIT %s ;""", (question, question, max_answers), as_dict=True, debug=True)

	for row in out:
		doc = frappe.get_doc('posts', row.name)
		y.append(float(doc.fitness))
		name1.append(row.name)

	Y = np.array([y])
	name = np.array([name1])
	Y = Y.T 
	name = name.T

	return (Y, name)

@frappe.whitelist(allow_guest=True)
def answer(question, i=0):
	print "In answer() : neural_net.py"
	print "question : ", question
	print "i = ", i
	Y, name = neural_network(question)

	print Y
	print name

	# for j in range(0, len(name)):
	# 	print "name array at value = ", j
	# 	print name[j][0]
	
	# if(len(name) == 0):
	# 	return false

	print "currently i = ", i
	print name[i][0]

	if name.size:
		doc = frappe.get_doc('posts', name[i][0])
		return doc
	else:
		return ''

	

