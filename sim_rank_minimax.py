import networkx as nx
import collections
import itertools
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
	#seen = set([node])
	search = set([node])
	for i in range(k):
		search = set([nbr for n in search for nbr in G.neighbors(n)])
		#search = set([nbr for n in search for nbr in G.neighbors(n) if nbr not in seen])
		#seen |= search
		if i%2 == 1: result |= search # Ensure we get only one part of the bipartite graph

	return result


def calculate_sim(G, user_sim, business_sim, k_hop_user,k_hop_business,weight_user,weight_business):
	def calculate(from_sim, to_sim, C,from_k_hop,from_weight,to_pmax):
		''' Calculates similarity of items in from_sim using similarity of items in to_sim.
				Performs one part of the bipartite simrank algorithm'''
		'''		
		# For every pair of nodes
		for node1, node2 in itertools.combinations(from_sim, 2):
			num = 0
			for a in G.neighbors_iter(node1):
				#for b in k_hops(G, a, 4):
				for b in G.neighbors_iter(node2):
					x, y = sorted((a, b)) #Keep only the upper half of the matrix
					print x,y
					#try:
					num += G[node1][a]['weight'] * G[node2][b]['weight'] * to_sim[x][y]
					#except Exception, e: import pdb;pdb.set_trace()

			weight1 = sum(G[node1][x]['weight'] for x in G.neighbors_iter(node1))
			#weight2 = sum(G[node2][x]['weight'] for x in G.neighbors_iter(node2))
			weight2 = sum([sum([G[node2][x]['weight'] for x in k_hops(G, y, 5)]) for y in G.neighbors_iter(node1)])
			den = weight1*weight2

			from_sim[node1][node2] = C*num/den # Note: itertools.combinations emits in sorted order
		'''	
		for node1 in from_sim:
			print node1 	
			for node2 in from_k_hops(G,node,2):
				num = sum(to_pmax[x][node2] for x in G[node1])	
				'''
				for b in G[node2]:
					x, y = sorted((a, b)) #Keep only the upper half of the matrix
					print x,y
					#try:
					num += G[node1][a]['weight'] * G[node2][b]['weight'] * to_sim[x][y]
					#except Exception, e: import pdb;pdb.set_trace()
				'''	
				#weight1 = sum(G[node1][x]['weight'] for x in G.neighbors_iter(node1))
				#weight2 = sum(G[node2][x]['weight'] for x in G.neighbors_iter(node2))
				#weight2 = sum([sum([G[node2][x]['weight'] for x in k_hops(G, y, 5)]) for y in G.neighbors_iter(node1)])
				#den = weight1*weight2

				from_sim[min(node1,node2)][max(node1,node2)] = C*num/from_weight[node1] # Note: itertools.combinations emits in sorted order


	pmax_business = {}
	pmax_user = {}

	for b in business_sim:
		pmax_business[b] = {}
		for u in user_sim:
			pmax_business[b][u] = max([business_sim[min(b,x)][max(b,x)] for x in G[u]])
	print "pmax1 done"
			
	for u in user_sim:
		pmax_user = {}
		for b in business_sim:
			pmax_user[u][b] = max([user_sim[min(u,x)][max(u,x)] for x in G[b]])
	print "pmax2 done"
			
	calculate(user_sim, business_sim, C1,k_hop_user,weight_user,pmax_business)
	print "user_done"
	calculate(business_sim, user_sim, C2,k_hop_business,weight_business,pmax_user)

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

	k_hop_user = {};
	k_hop_business = {};
	weight_user = {};
	weight_business = {};

	#for node1 in user_sim:
	#	k_hop_user[node1] = k_hops(G,node1,2)

	#for node2 in business_sim:
	#	k_hop_business[node2] = k_hops(G,node2,2)

	print "memoized hops"

	for node in user_sim:	
		weight_user[node] =  sum(G[node][x]['weight'] for x in G[node])	
	for node in (set(business_sim)&set(G.nodes())):
		weight_business[node] = sum(G[node][x]['weight'] for x in G[node])

	print "memoized	sum of weights"

	for i in range(N_ITERS):
		print '{0: .1f}%'.format(float(i)/N_ITERS*100)
		calculate_sim(G, user_sim, business_sim,k_hop_user,k_hop_business,weight_user,weight_business)

if __name__ == '__main__':
	main()
