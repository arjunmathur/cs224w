import networkx as nx
import collections
import sys
import random
import math
#from networkx.algorithms import bipartite	
										
def initialize():
	G = nx.read_edgelist("edges.txt", nodetype=str, data=(('weight',float),))
	# 'Uf61AA2JUGWTcxSXNoGaXg', 'xGz3WSkC96aWtqt7vE70gw'
	return G

def sim_initialize():
	def read_sim(filename):
		sim = {}
		with open(filename) as f:
			for line in f:
				node = line.rstrip('\n')
				sim[node] = collections.Counter()
				sim[node][node] = 1.0
		return sim
	user_sim, business_sim = read_sim(USER_FILE), read_sim(BUSINESS_FILE)
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
		for i, node1 in enumerate(sorted(from_sim)):
			#print_progress(i, len(from_sim))
			print i, 'of', len(from_sim)
			for node2 in k_hops(G, node1, 2):
				#print_progress(j, len(k_neighbors))
				num = 0
				for a in G[node1]:
					#for b in k_hops(G, a, 4):
					for b in G[node2]:
						x, y = sorted((a, b)) #Keep only the upper half of the matrix
						if to_sim[x][y] == 0: continue
						num += G[node1][a]['weight'] * G[node2][b]['weight'] * to_sim[x][y]
						
				weight1 = sum(G[node1][x]['weight'] for x in G.neighbors_iter(node1))
				weight2 = sum(G[node2][x]['weight'] for x in G.neighbors_iter(node2))
				den = weight1*weight2
				from_sim[min(node1,node2)][max(node1,node2)] = C*num/den # Note: itertools.combinations emits in sorted order

	print 'Calculating User-User Similarity...'
	calculate(user_sim, business_sim, C1)
	print 'Calculating Business-Business Similarity...'
	calculate(business_sim, user_sim, C2)


def print_progress(i, total):
	sys.stdout.write('\r')
	sys.stdout.write('{0: .1f}%'.format(float(i)/total*100))
	sys.stdout.flush()


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

	for i in range(N_ITERS):
		print 'Iteration: ', i
		calculate_sim(G, user_sim, business_sim)

# if __name__ == '__main__':
# 	main()