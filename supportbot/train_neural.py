#!/usr/bin/python

# Original code available at
# https://github.com/stephencwelch/Neural-Networks-Demystified

from scipy import optimize
import numpy as np
import random
import frappe
import json

class Neural_Network(object):
	def __init__(self, no_parameters):        
		#Define Hyperparameters
		self.inputLayerSize = no_parameters
		self.outputLayerSize = 1
		self.hiddenLayerSize = 3
		
		#Weights (parameters)
		np.random.seed(1)
		self.W1 = np.random.randn(self.inputLayerSize,self.hiddenLayerSize)
		self.W2 = np.random.randn(self.hiddenLayerSize,self.outputLayerSize)
		
	def forward(self, X):
		#Propogate inputs though network
		self.z2 = np.dot(X, self.W1)
		self.a2 = self.sigmoid(self.z2)
		self.z3 = np.dot(self.a2, self.W2)
		yHat = self.sigmoid(self.z3) 
		return yHat
		
	def sigmoid(self, z):
		#Apply sigmoid activation function to scalar, vector, or matrix
		return 1/(1+np.exp(-z))
	
	def sigmoidPrime(self,z):
		#Gradient of sigmoid
		return np.exp(-z)/((1+np.exp(-z))**2)
	
	def costFunction(self, X, y):
		#Compute cost for given X,y, use weights already stored in class.
		self.yHat = self.forward(X)
		self.error = y-self.yHat
		# print "error"
		# print self.error
		J = 0.5*sum((y-self.yHat)**2)
		return J
		
	def costFunctionPrime(self, X, y):
		#Compute derivative with respect to W and W2 for a given X and y:
		self.yHat = self.forward(X)
		
		delta3 = np.multiply(-(y-self.yHat), self.sigmoidPrime(self.z3))
		dJdW2 = np.dot(self.a2.T, delta3)
		
		delta2 = np.dot(delta3, self.W2.T)*self.sigmoidPrime(self.z2)
		dJdW1 = np.dot(X.T, delta2)  
		
		return dJdW1, dJdW2
	
	#Helper Functions for interacting with other classes:
	def getParams(self):
		#Get W1 and W2 unrolled into vector:
		params = np.concatenate((self.W1.ravel(), self.W2.ravel()))
		return params
	
	def setParams(self, params):
		#Set W1 and W2 using single paramater vector.
		W1_start = 0
		W1_end = self.hiddenLayerSize * self.inputLayerSize
		self.W1 = np.reshape(params[W1_start:W1_end], (self.inputLayerSize , self.hiddenLayerSize))
		W2_end = W1_end + self.hiddenLayerSize*self.outputLayerSize
		self.W2 = np.reshape(params[W1_end:W2_end], (self.hiddenLayerSize, self.outputLayerSize))
		
	def computeGradients(self, X, y):
		dJdW1, dJdW2 = self.costFunctionPrime(X, y)
		return np.concatenate((dJdW1.ravel(), dJdW2.ravel()))
		

class trainer(object):
	def __init__(self, N):
		#Make Local reference to network:
		self.N = N
		
	def callbackF(self, params):
		self.N.setParams(params)
		self.J.append(self.N.costFunction(self.X, self.y))   
		
	def costFunctionWrapper(self, params, X, y):
		self.N.setParams(params)
		cost = self.N.costFunction(X, y)
		grad = self.N.computeGradients(X,y)
		return cost, grad
		
	def train(self, X, y):
		#Make an internal variable for the callback function:
		self.X = X
		self.y = y

		#Make empty list to store costs:
		self.J = []
		
		params0 = self.N.getParams()

		options = {'maxiter': 10000, 'disp' : True}
		_res = optimize.minimize(self.costFunctionWrapper, params0, jac=True, method='BFGS', \
								 args=(X, y), options=options, callback=self.callbackF)

		self.N.setParams(_res.x)
		self.optimizationResults = _res


#find max of each parameter
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


def gen_vector(name, max_word, max_link, max_like, max_read):
	doc = frappe.get_doc('posts', name)

	word = float(doc.word_count)/max_word
	like = float(doc.like_score)/max_like
	read = float(doc.reads)/max_read
	link = float(doc.incoming_link_count)/max_link
	fit_x = float(doc.fitness)
	isdoc = float(doc.is_doc)
	avg_word = float(doc.avg_word)
	avg_sentence = float(doc.avg_sentence)
	if(doc.reply_to_post_number):
		reply = float(1)
	else:
		reply = float(0)
	no_parameters = 4
	parameter_list = ["avg_sentence", "avg_word", "word", "like"]
	parameter_list = json.dumps(parameter_list)
	x_in = np.array([avg_sentence, avg_word, word, like])
	return (x_in, fit_x, no_parameters, parameter_list)

def gen_ip_op():
	max_link, max_word, max_like, max_read = find_max()

	x = []
	y = []
	name1 = []

	out = frappe.db.sql("""SELECT name FROM tabposts WHERE fitness > 0.0 AND from_neural = 0;""", as_dict=True, debug=True)

	i=0
	for row in out:
		x_in, fit_x, no_parameters, parameter_list = gen_vector(row.name, max_word, max_link, max_like, max_read)
		name1.append(row.name)
		x.append(x_in)
		y.append(fit_x)
		i = i+1

	print "Max answers : ", i
	X = np.array(x)
	Y = np.array([y])
	name = np.array([name1])
	Y = Y.T 
	name = name.T
	return (X, Y, name, no_parameters, parameter_list, i, max_link, max_word, max_like, max_read)


def neural_network():

	X, Y, name, no_parameters, parameter_list, total_answers, max_link, max_word, max_like, max_read = gen_ip_op()


	np.random.seed()

	NN = Neural_Network(no_parameters)

	T = trainer(NN)
	T.train(X, Y)

	print "X"
	print X
	
	print "Y"
	print Y

	print "yhat"
	print NN.yHat
	
	err = np.mean(np.abs(NN.error))
	print "NN.error"
	print NN.error
	print err

	print "W1"
	print NN.W1

	print "W2"
	print NN.W2	

	calculate_fitness(NN.W1, NN.W2, max_link, max_word, max_like, max_read)

	_syn1 = json.dumps(NN.W1.tolist())
	_syn2 = json.dumps(NN.W2.tolist())

	frappe.get_doc({
				'doctype': 'neural_net_traces',
				'tot_answers': total_answers,
				'params': parameter_list,
				'no_params': no_parameters,
				'hidden_size': NN.hiddenLayerSize,
				'syn1': _syn1,
				'syn2': _syn2,
				'error': err
			}).insert()
	frappe.db.commit()

	return	

def sigmoid(z):
	#Apply sigmoid activation function to scalar, vector, or matrix
	return 1/(1+np.exp(-z))
	

def calculate_fitness(syn1, syn2, max_link, max_word, max_like, max_read):
	rows = frappe.db.sql("""SELECT name FROM tabposts WHERE fitness = 0.0""", as_dict=True, debug=True)

	for row in rows:
		doc = frappe.get_doc('posts', row.name)
		print doc.name
		x_in, fit_x, no_parameters, parameter_list = gen_vector(row.name, max_word, max_link, max_like, max_read)
		print x_in 
		hidden = sigmoid(np.dot(x_in, syn1))
		print hidden
		x_out = sigmoid(np.dot(hidden, syn2))
		print x_out
		doc.fitness = float(x_out[0])
		doc.from_neural =  1
		doc.save(ignore_permissions=True)
		frappe.db.commit()

	print "DONE"
	return


