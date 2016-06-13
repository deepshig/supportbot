import frappe

@frappe.whitelist(allow_guest=True)
def get_answer(question, start=0):
	
	out = frappe.db.sql("""SELECT name, raw, MATCH(raw) AGAINST(%s IN NATURAL LANGUAGE MODE) AS score FROM tabposts WHERE MATCH(raw) AGAINST(%s IN NATURAL LANGUAGE MODE) and created_at >= '2014-01-01' ORDER BY score DESC LIMIT {start}, 1 ;""".format(start=start), (question, question), as_dict=True, debug=True)

	print out

	if out:
		return out[0]
	else:
		return ''

@frappe.whitelist(allow_guest=True)
def set_fitness(_fit, name):
	#print "In set_fitness : api.py"
	doc = frappe.get_doc('posts', name)

	old_fit = float(doc.fitness)
	no_rev = doc.no_reviewed

	new_fit = float((old_fit*no_rev)) + float(_fit)/10
	no_rev = no_rev + 1
	new_fit = float(new_fit)/no_rev

	doc.no_reviewed = no_rev
	doc.fitness = float(new_fit)
	doc.save(ignore_permissions=True)
	frappe.db.commit()
	return



