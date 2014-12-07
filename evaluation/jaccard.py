import json
import numpy as np
import networkx as nx
import collections
import matplotlib.pyplot as plt
import random
from scipy.stats.stats import pearsonr

def initialize():
	G = nx.read_edgelist("edges.txt", nodetype=str, data=(('weight',float),))
	G_trim = nx.read_edgelist("edges_trim_may.txt", nodetype = str, data = (('weight', float),))
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


potential = {}
original = {}
precision = {}
recall = {}
top_similar = {}
f = open("precision_jaccard_may.txt","w")
f1 = open("recall_jaccard_may.txt","w")

for b in emerging:
	print b
#	similar = Sim.Query(b)
#	sample = max(20,k*len(similar))
#	top_similar[b] = similar[0:int(sample)]
	score = {}
	for u in business_trim:
		common = set(G_trim[u])&set(G_trim[b])
		total = set(G_trim[u])|set(G_trim[b])
		'''
		for c in common:
			if c not in G[u]:
				vec1.append(0)
			else:
				vec1.append(G[u][c]['weight'])	
			if c not in G[b]:
				vec1.append(0)
			else:
				vec1.append(G[b][c]['weight'])			
		'''
		if len(common) > 0:
			score[u] = len(common)*1.0/len(total)

	top_similar[b] =  sorted(score.items(), reverse=True, key=lambda tup: tup[1])[0:min(len(score.keys()),30)]
	
	potential[b] = set()
	for x in top_similar[b]:
		potential[b] |= set([u for u in G_trim[x[0]] if G_trim[x[0]][u]['weight'] >= 0.8])
	
	original[b] = [x for x in (set(G[b]) & set(user_trim)) if x not in G_trim[b] and G[x][b]['weight'] >= 0.8]		

	tp = set(original[b]) & potential[b]
	precision[b] = len(tp)*1.0/len(original[b])
	recall[b] = len(tp)*1.0/len(potential[b])
	
json.dump(precision, f)
json.dump(recall, f1)
f.close()
f1.close()

import pdb; pdb.set_trace()