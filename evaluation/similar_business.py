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
k = 0.5
##################################

G, G_trim = initialize()
#user, business = node_initialize(G)
user_trim, business_trim = node_initialize(G_trim)

emerging = [x for x in business_trim if len(G_trim[x]) <= 20 and len([y for y in G[x] if G[x][y]['weight'] >= 0.8]) >= 60]
print len(emerging)

Sim = SimRankFast(G_trim)
print "Sim initialized"


potential = {}
original = {}
precision = {}
recall = {}
top_similar = {}
for b in emerging:
	print b
	similar = Sim.Query(b)
	sample = max(20,k*len(similar))
	top_similar[b] = similar[0:int(sample)]

	potential[b] = set(G_trim[b])
	for x in top_similar[b]:
		potential[b] |= set([u for u in G_trim[x[0]] if G_trim[x[0]][u]['weight'] >= 0.8])
	
	original[b] = [x for x in G[b] if G[b][x]['weight'] >= 0.8]		

	tp = set(original[b]) & potential[b]
	precision[b] = len(tp)*1.0/len(original[b])
	recall[b] = len(tp)*1.0/len(potential[b])
	
import pdb; pdb.set_trace()
