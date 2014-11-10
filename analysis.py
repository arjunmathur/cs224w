import networkx as nx
import collections
import itertools
import matplotlib.pyplot as plt
import json

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

def k_hops(G, node, k):
	'''Calculates all nodes within k edges from @node
		 that are on the same part of a bipartite graph'''
	result = set([])
	seen = set([node])
	search = set([node])
	for i in range(k):
		#search = set([nbr for n in search for nbr in G[n]])
		search = set([nbr for n in search for nbr in G[n] if nbr not in seen])
		seen |= search
		if i%2 == 1: result |= search # Ensure we get only one part of the bipartite graph

	return result


########### Constants ############			
C1 = 0.8
C2 = 0.8
USER_FILE = 'user_id.txt'
BUSINESS_FILE = 'business_id.txt'
N_ITERS = 10
##################################

def main():
	#f = open("hops.txt","w")
	G = initialize()
	print "initialized"
	user, business = node_initialize(G)
	print "sim initialized"	
	G1 = nx.cycle_graph(10)
	#print user[1]
	#print type(G.nodes()[1])
	
	degree_sequence=[G.degree(x) for x in user]
	dist = collections.Counter(degree_sequence)
	plt.loglog(dist.values())
	plt.show()
	
	degree_sequence1=[G.degree(x) for x in business]
	
	dist1 = {}
	for n in degree_sequence1:
		if n in dist1.keys():
			dist1[n] += 1
		else:
			if type(n) is int:	
				dist1[n] = 1		

	plt.loglog(dist1.values())
	plt.show()
	
	'''
	hop = {}
	#for node in (set(business) & set(G.nodes())):
	for node in G1.nodes():	
		#print node
		hop[node] = len(k_hops(G1,node,2))
		print node, hop[node]
	
	hop_dist = collections.Counter(hop)
	'''
	#plt.loglog(hop_dist.values())
	#plt.show()
		#print >> f, node, k_hops(G,node,2)

if __name__ == '__main__':
		main()	

### within 1-hop: number of user connections - 130217058		