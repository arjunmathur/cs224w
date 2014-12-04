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
k = 0.2
##################################

G, G_trim = initialize()
user, business = node_initialize(G)
user_trim, business_trim = node_initialize(G_trim)

emerging = [x for x in business_trim if len(G_trim[x]) < 20 and len(G[x]) > 60]

Sim = SimRankFast(G_trim)
print "Sim initialized"

positive = {}
negative = {}
potential = {}
original = {}
precison = {}
recall = {}
for b in emerging:
	positive[b] = [u for u in G_trim[b] if G_trim[b][u]['weight'] >= 4]
	negative[b] = [u fot u in G_trim[b] if G_trim[b][u]['weight'] < 4]
	potential[b] = set()
	for x in positive[b]:
		user = Sim.Query(x)
		sample = max(10,k*len(user))
		potential[b] |= user[0:sample]
	
	original[b] = [x for x in G[b] if x not in G_trim[b] and G[b][x]['weight'] >= 4]		

	tp = set(original[b]) & potential[b]
	precision[b] = len(tp)*1.0/len(original[b])
	recall[b] = len(tp)*1.0/len(potential[b])
	
import pdb; pdb.set_trace()
