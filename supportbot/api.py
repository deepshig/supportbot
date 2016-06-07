import frappe

@frappe.whitelist(allow_guest=True)
def get_answer(question, start=0):
	out = frappe.db.sql("""select text from tabAnswer where match(text)
		against (%s IN NATURAL LANGUAGE MODE) limit {start}, 1""".format(start=start),
		question)

	if out:
		return out[0][0]
	else:
		return ''
