import json
import numpy as np
import networkx as nx
import collections
import matplotlib.pyplot as plt
import random
from sim_rank_fast import *
import pp

def initialize():
	G = nx.read_edgelist("edges.txt", nodetype=str, data=(('weight',float),))
	G_trim = nx.read_edgelist("edges_trim.txt", nodetype = str, data = (('weight', float),))
	print "initialized"
	# 'Uf61AA2JUGWTcxSXNoGaXg', 'xGz3WSkC96aWtqt7vE70gw'
	return G, G_trim

def node_initialize(G):
	user = [x for x in G.nodes() if str(x).find('u') == 0]
	business = [x for x in G.nodes() if str(x).find('b') == 0]
	return user, business

def evaluate(emerging, G, G_trim, Sim):
	precision = {}
	recall = {}
	f = open("precision_user.txt","w")
	f1 = open("recall_user.txt","w")
	ppservers = ()
	job_server = pp.Server(ppservers = ppservers)

	print "Starting pp with", job_server.get_ncpus(), "workers"

	jobs = [(b, job_server.submit(evaluateBusiness,(b,G,G_trim,Sim,), (), ("from sim_rank_fast import *", "import networkx as nx", "collections", "random"))) for b in emerging]
	for b, job in jobs:
	    precision[b] = job()[0]
	    recall[b] = job()[1]

	json.dump(precision, f)
	json.dump(recall, f1)	
	f.close()
	f1.close()
def evaluateBusiness(b, G, G_trim, Sim):
	positive = [u for u in G_trim[b] if G_trim[b][u]['weight'] >= 0.8]
	negative = [u for u in G_trim[b] if G_trim[b][u]['weight'] < 0.8]
	potential = set(G_trim[b])
	for x in positive:
		print x
		user = Sim.Query(x)
		print user
		sample = min(15,len(user))
		print sample
		potential |= set([x[0] for x in user[0:sample]])
		print potential
	
	original = [x for x in G[b] if G[b][x]['weight'] >= 0.8]		

	tp = set(original) & potential
	precision = len(tp)*1.0/len(original)
	recall = len(tp)*1.0/len(potential)

	return precision, recall

########### Constants ############			
USER_FILE = 'user_id.txt'
BUSINESS_FILE = 'business_id.txt' 
USER_MAP = "user_id_map.txt"
BUSINESS_MAP = "business_id_map.txt"
k = 0.25
##################################

G, G_trim = initialize()
user_trim, business_trim = node_initialize(G_trim)

emerging = [x for x in business_trim if len(G_trim[x]) <= 20 and len(G_trim[x]) >= 10 and len([y for y in G[x] if G[x][y]['weight'] >= 0.8]) >= 60]

Sim = SimRankFast(G_trim)
print "Sim initialized"

evaluate(emerging, G, G_trim, Sim)

import pdb; pdb.set_trace()
