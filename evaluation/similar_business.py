import json
import numpy as np
import networkx as nx
import collections
import matplotlib.pyplot as plt
import random
from sim_rank_fast import *

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


########### Constants ############			
USER_FILE = 'user_id.txt'
BUSINESS_FILE = 'business_id.txt' 
USER_MAP = "user_id_map.txt"
BUSINESS_MAP = "business_id_map.txt"
k = 0.25
##################################

G, G_trim = initialize()
#user, business = node_initialize(G)
user_trim, business_trim = node_initialize(G_trim)

emerging = [x for x in business_trim if len(G_trim[x]) <= 20 and len(G_trim[x]) >= 10 and len([y for y in G[x] if G[x][y]['weight'] >= 0.8]) >= 60]
print len(emerging)

Sim = SimRankFast(G_trim)
print "Sim initialized"

potential = {}
original = {}
precision = {}
recall = {}
top_similar = {}
#f = open("precision_business.txt","w")
#f1 = open("recall_business.txt","w")

#with open("top_similar_business.txt","r") as f2:
#	for line in f2:
#		top_similar = json.loads(line)


for b in emerging:
#for b in top_similar.keys():
	print b
	similar = Sim.Query(b)
	print len(similar)
	sample = min(20,len(similar))
	top_similar[b] = similar[0:int(sample)]
	
	#potential[b] = set(G_trim[b])
	potential[b] = set()
	for x in top_similar[b]:
		potential[b] |= set([u for u in G_trim[x[0]] if G_trim[x[0]][u]['weight'] >= 0.8])
	
	original[b] = [x for x in G[b] if x in user_trim and x not in G_trim[b]]		

	tp = set(original[b]) & potential[b]
	precision[b] = len(tp)*1.0/len(original[b])
	recall[b] = len(tp)*1.0/len(potential[b])
	
#json.dump(precision, f)
#json.dump(recall, f1)
#f.close()
#f1.close()
import pdb; pdb.set_trace()
