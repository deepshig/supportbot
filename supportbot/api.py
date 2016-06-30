import frappe
from frappe.utils import now
#import neural_net

@frappe.whitelist(allow_guest=True)
def get_answer(question, start=0):
	
	out = frappe.db.sql("""SELECT name, raw, MATCH(raw) AGAINST(%s IN NATURAL LANGUAGE MODE) AS score FROM tabposts WHERE MATCH(raw) AGAINST(%s IN NATURAL LANGUAGE MODE) and created_at >= '2014-01-01' ORDER BY score DESC LIMIT {start}, 1 ;""".format(start=start), (question, question), as_dict=True, debug=True)

	#print out

	if out:
		return out[0]
	else:
		return ''

@frappe.whitelist(allow_guest=True)
def set_fitness(_fit, name):
	#print "In set_fitness : api.py"
	print "fitness value passed : ", _fit
	doc = frappe.get_doc('posts', name)

	if doc.from_neural==0:		
		old_fit = float(doc.fitness)
		no_rev = doc.no_reviewed

		new_fit = float((old_fit*no_rev)) + float(_fit)/10
		no_rev = no_rev + 1
		new_fit = float(new_fit)/no_rev

		doc.no_reviewed = no_rev
		print "modified fitness value : ", new_fit	
		doc.fitness = float(new_fit)

	else:
		doc.fitness = float(_fit)/10
		doc.from_neural = 0
		doc.no_reviewed = 1

	doc.save(ignore_permissions=True)
	frappe.db.commit()
	return

@frappe.whitelist(allow_guest=True)
def set_log(msg, bot, session):
	print "set_log function : api.py"
	#frappe.db.sql('DELETE FROM tabconversation_log;')
	frappe.get_doc({
				'doctype': 'conversation_log',
				'message': msg,
				'from_bot': bot,
				'session_id': session,
				'timestamp': now()
			}).insert()
	frappe.db.commit()
	return

@frappe.whitelist(allow_guest=True)
def feed_detail(unam, email, cntry, dmn, fb):
	print "feed_detail function : api.py"
	#frappe.db.sql('DELETE FROM tabuser_details;')
	frappe.get_doc({
				'doctype': 'user_details',
				'uname': unam,
				'email_id': email,
				'country': cntry,
				'domain': dmn,
				'feedback': fb
			}).insert()
	frappe.db.commit()
	return





