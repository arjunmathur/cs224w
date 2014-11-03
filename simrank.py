import networkx as nx
import collections
import itertools
#from networkx.algorithms import bipartite	
										
def initialize():
	G = nx.read_edgelist("edges.txt", nodetype=str, data=(('weight',float),))
	# 'Uf61AA2JUGWTcxSXNoGaXg', 'xGz3WSkC96aWtqt7vE70gw'
	return G

def sim_initialize():
	user_sim, business_sim = {}, {}
	
	with open("user_id.txt") as f:
		for line in f:
			node = line.rstrip('\n')
			user_sim[node] = collections.Counter()
			user_sim[node][node] = 1.0
		
	with open("business_id.txt") as f:
		for line in f:
			node = line.rstrip('\n')
			business_sim[node] = collections.Counter()
			business_sim[node][node] = 1.0

	return user_sim, business_sim

def k_hops(G, node, k):
	'''Calculates all nodes within k edges from @node
		 that are on the same part of a bipartite graph'''
	result = set([])
	seen = set([node])
	search = set([node])
	for i in range(k):
		search = set([nbr for n in search for nbr in G.neighbors(n) if nbr not in seen])
		seen |= search
		if i%2 == 1: result |= search # Ensure we get only one part of the bipartite graph

	return result


def calculate_sim(G, user_sim, business_sim):
	def calculate(from_sim, to_sim, C):
		''' Calculates similarity of items in from_sim using similarity of items in to_sim.
				Performs one part of the bipartite simrank algorithm'''
		# For every pair of nodes
		for node1, node2 in itertools.combinations(from_sim, 2):
			num = 0
			for a in G.neighbors_iter(node1):
				#for b in k_hops(G, a, 5):
				for b in G.neighbors_iter(node2):
					x, y = sorted((a, b)) #Keep only the upper half of the matrix
					try:num += G[node1][a]['weight'] * G[node2][b]['weight'] * to_sim[x][y]
					except Exception, e: import pdb;pdb.set_trace()

			weight1 = sum(G[node1][x]['weight'] for x in G.neighbors_iter(node1))
			weight2 = sum(G[node2][x]['weight'] for x in G.neighbors_iter(node2))
			den = weight1*weight2

			from_sim[node1][node2] = C*num/den # Note: itertools.combinations emits in sorted order

	calculate(user_sim, business_sim, C1)
	calculate(business_sim, user_sim, C2)

########### Constants ############			
C1 = 0.8
C2 = 0.8
USER_FILE = 'user_id.txt'
BUSINESS_FILE = 'business_id.txt'
N_ITERS = 10
##################################

def main():
	G = initialize()
	print "Initialized"

	user_sim, business_sim = sim_initialize()
	print "sim initialized"

	for _ in range(N_ITERS):
		print _
		calculate_sim(G, user_sim, business_sim)

if __name__ == '__main__':
	main()