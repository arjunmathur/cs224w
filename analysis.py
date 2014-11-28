import networkx as nx
import collections
import itertools
import matplotlib.pyplot as plt
import json
import numpy as np

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

	return len(result)

def till_k_hops(G, node, k):
	'''Calculates all nodes within k edges from @node
		 that are on the same part of a bipartite graph'''
	hop = collections.Counter()	 
	seen = set([node])
	search = set([node])
	for i in range(k):
		#search = set([nbr for n in search for nbr in G[n]])
		search = set([nbr for n in search for nbr in G[n] if nbr not in seen])
		seen |= search
		if i%2 == 1: 
			hop[i+1] = hop[i-1] + len(search)
	return hop

def alphaMLE(data,xmin):
	L = 0
	for i in data:
		L += np.log(i*1.0/xmin)
	alpha_hat = 1 + len(data)*1.0/L
	return alpha_hat	

def degree_distribution(G, nodes):
	nodes = list(set(nodes)&set(G.nodes()))
	degree_sequence=[G.degree(x) for x in nodes]
	dist = collections.Counter(degree_sequence)
	return dist, degree_sequence

def logplot(x,y):
	plt.loglog(x,y,'ro')
	plt.xlabel('Degree of node')
	plt.ylabel('No. of nodes')
	plt.show()	

def hop_distribution(G,nodes,k):
	hop = {}
	for node in (set(nodes) & set(G.nodes())):
		hop[node] = k_hops(G,node,k)

	total_pair = sum(hop.values())*0.5
	hop_dist = collections.Counter(hop.values())
	return hop_dist, total_pair

def k_hop_nodewise(G,nodes,k):
	hop_count = {}
	for node in (set(nodes) & set(G.nodes())):
		hope_count[node] = till_k_hops(G,node,k)
	return hop_count

def ranking_distribution(G):
	ranking = []
	for e in G.edges():
		ranking.append(G[e[0]][e[1]]['weight'])
	
	ranking_dist = collections.Counter(ranking)
	for i in ranking_dist.keys():
		ranking_dist[i] = ranking_dist[i]*1.0/G.number_of_edges()
	return ranking_dist

########### Constants ############			
USER_FILE = 'user_id.txt'
BUSINESS_FILE = 'business_id.txt'
##################################

def main():
	#f = open("hops.txt","w")
	G = initialize()
	print "initialized"
	user, business = node_initialize(G)
	print "node initialized"	
	'''
	ranking_dist = ranking_distribution(G)
	print ranking_dist

	plt.plot(ranking_dist.keys(), ranking_dist.values(), 'ro')
	plt.xlabel('ranking')
	plt.ylabel('count')
	plt.title('Ranking Distribution')
	plt.axis([0, 6, 0, 1])
	plt.grid(True)	
	plt.show()
	
	'''
	num_connected = nx.algorithms.number_connected_components(G)
	size_connected = [len(x) for x in nx.connected_components(G)]
	#print [x*1.0/G.number_of_nodes() for x in size_connected]
	G = list(nx.connected_component_subgraphs(G))[0]
	#print x.number_of_edges()*1.0/G.number_of_edges() 
	#print G.number_of_nodes()
	#print G.number_of_edges()
	#print num_connected 
	
	
	
	user_degree_dist, user_degree_sequence = degree_distribution(G,user)
	logplot(user_degree_dist.keys(), user_degree_dist.values())
	print sum(user_degree_dist.values())
	business_degree_dist, business_degree_sequence = degree_distribution(G,business)
	logplot(business_degree_dist.keys(), business_degree_dist.values())
	
	alpha_user = alphaMLE(user_degree_sequence, 1)
	business_degree_sequence = [x for x in business_degree_sequence if x > 2]
	alpha_business = alphaMLE(business_degree_sequence,3)
	print alpha_user, alpha_business
	## Alpha values: 2.39 1.79
	'''
	user_hop_dist, total_user_pair = hop_distribution(G,user,2)
	business_hop_dist, total_business_pair = hop_distribution(G,business,2)
	print 2.0*total_user_pair/len(set(user) & set(G.nodes()))
	print 2.0*total_business_pair/len(set(business) & set(G.nodes()))
	#print total_business_pair
	## 2-hop Values : 135217058.0, 17896957.0
	## Average at least 1 common rated user =  1069.3406669
	## ## Average at least 1 common rater business =  853.089136756
	
	plt.plot(user_hop_dist.keys(),user_hop_dist.values(),'ro')
	plt.xscale('log')
	plt.show()
	plt.plot(business_hop_dist.keys(), business_hop_dist.values(),'ro')
	plt.xscale('log')
	plt.show()
	'''


if __name__ == '__main__':
		main()	

### within 1-hop: number of user connections - 130217058		