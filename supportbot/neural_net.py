#!/usr/bin/python

import numpy as np
import random
import frappe

max_answers = 15


# sigmoid function
@frappe.whitelist(allow_guest=True)
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.abs(x))

#find max of each parameter
@frappe.whitelist(allow_guest=True)
def find_max():
    max_link = max_word = max_like = max_read = 1

    rows = frappe.db.sql("""SELECT incoming_link_count, `reads`, like_score, word_count FROM tabposts;""", as_dict=True, debug=True)

    for row in rows:
        if row.incoming_link_count > max_link:
            max_link = row.incoming_link_count
        if row.word_count > max_word:
            max_word = row.word_count
        if row.like_score > max_like:
            max_like = row.like_score
        if row.reads > max_read:
            max_read = row.reads

    return (max_link, max_word, max_like, max_read) 


@frappe.whitelist(allow_guest=True)
def gen_vector(name, max_word, max_link, max_like, max_read, score):
    doc = frappe.get_doc('posts', name)

    word = float(doc.word_count)/max_word
    like = float(doc.like_score)/max_like
    read = float(doc.reads)/max_read
    link = float(doc.incoming_link_count)/max_link
    fit_x = float(doc.fitness)
    score_x = float(score)
    isdoc = float(doc.is_doc)
    if(doc.reply_to_post_number):
        reply = float(1)
    else:
        reply = float(0)
    x_in = np.array([word, like, read, link, reply, isdoc, score_x])
    return (x_in, fit_x)


@frappe.whitelist(allow_guest=True)
def gen_ip_op(question):
    max_link, max_word, max_like, max_read = find_max()

    x = []
    y = []
    name1 = []

    out = frappe.db.sql("""SELECT name, MATCH(raw) AGAINST(%s IN NATURAL LANGUAGE MODE) AS score FROM tabposts WHERE MATCH(raw) AGAINST(%s IN NATURAL LANGUAGE MODE) and created_at >= '2014-01-01' ORDER BY score DESC LIMIT %s ;""", (question, question, max_answers), as_dict=True, debug=True)

    for row in out:
        x_in, fit_x = gen_vector(row.name, max_word, max_link, max_like, max_read, row.score)
        name1.append(row.name)
        x.append(x_in)
        y.append(fit_x)

    X = np.array(x)
    Y = np.array([y])
    name = np.array([name1])
    Y = Y.T 
    name = name.T
    return (X, Y, name)


@frappe.whitelist(allow_guest=True)
def neural_network(question):

    X, Y, name = gen_ip_op(question)

    np.random.seed(1)

    # initialize weights randomly with mean 0
    syn0 = 2*np.random.random((7,max_answers)) - 1
    syn1 = 2*np.random.random((max_answers,1)) - 1

    for iter in xrange(100000):

    # Feed forward through layers 0, 1, and 2
        l0 = X

        l1 = nonlin(np.dot(l0,syn0))
        l2 = nonlin(np.dot(l1,syn1))

        # how much did we miss?
        l2_error = Y - l2

        if (iter% 10000) == 0:
            print "Error:" + str(np.mean(np.abs(l2_error)))

        # in what direction is the target value? Were we really sure? if so, don't change too much.
        l2_delta = l2_error*nonlin(l2,deriv=True)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        l1_error = l2_delta.dot(syn1.T) 

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.                                                                            
        l1_delta = l1_error * nonlin(l1,True)

        # update weights
        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)

    return (l2, name)

@frappe.whitelist(allow_guest=True)
def sort(l2, name):
    n = len(l2)

    print name, len(name)
    print l2, len(l2)

    for i in range(0, n):
        for j in range(0, n-i-1):
            if l2[j] < l2[j+1]:
                l2[j], l2[j+1] = l2[j+1], l2[j]
                name[j], name[j+1] = name[j+1], name[j]

    return (l2, name)

@frappe.whitelist(allow_guest=True)
def answer(question, i=0):
    l2, _name = neural_network(question)
    l2, _name = sort(l2, _name)

    doc = frappe.get_doc('posts', str(_name[i][0]))
    return doc

