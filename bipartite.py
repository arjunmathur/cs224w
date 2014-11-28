import networkx as nx
import collections
import itertools
import matplotlib.pyplot as plt
import json
import numpy as np
from networkx.algorithms import bipartite

def initialize():
	G = nx.read_edgelist("edges.txt", nodetype=str, data=(('weight',float),))
	# 'Uf61AA2JUGWTcxSXNoGaXg', 'xGz3WSkC96aWtqt7vE70gw'
	return G

def node_initialize(G):
	def read_node(filename):
		node = []
		with open(filename) as f:
			for line in f:	
				node.append(line.rstrip('\n'))
		return node
	user, business = read_node(USER_FILE), read_node(BUSINESS_FILE)
	return user, business

def make_bipartite(G,user,business):
	for n in user:
		G.node[n]['bipartite'] = 0	

	for n in business:
		G.node[n]['bipartite'] = 1

	return G

def main():
	G = initialize()
	user, business = node_initialize(G)
	user = list(set(user) & set(G.nodes()))
	business = list(set(business) & set(G.nodes()))
	G = make_bipartite(G, user, business)
	print nx.is_bipartite(G)
	G = list(nx.connected_component_subgraphs(G))[0]
	user, business = bipartite.sets(G)
	print "nodes separated"
	Gu = bipartite.projected_graph(G, user)
	print Gu.number_of_nodes()

########### Constants ############			
USER_FILE = 'user_id.txt'
BUSINESS_FILE = 'business_id.txt'
##################################

if __name__ == '__main__':
	main()
	