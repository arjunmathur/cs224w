import networkx as nx
#from networkx.algorithms import bipartite	
										
def initialize():
	G = nx.read_edgelist("edges.txt", nodetype=str, data=(('weight',float),))
	# 'Uf61AA2JUGWTcxSXNoGaXg', 'xGz3WSkC96aWtqt7vE70gw'
	return G

def get_nodes_list(user,business):
	with open("user_id.txt") as file:
		for line in file:
			user.append(line)
	with open("business_id.txt") as file:
		for line in file:
			business.append(line)

def sim_initialize(G,user,business,user_sim,business_sim):
	for node1 in user:
		user_sim[node1] = {}
		for node2 in user:
			if node1 == node2:
				user_sim[node1][node2] = 1
			else:
				user_sim[node1][node2] = 0
	for node1 in business:
		business_sim[node1] = {}
		for node2 in business:
			if node1 == node2:
				business_sim[node1][node2] = 1
			else:
				business_sim[node1][node2] = 0	


def calculate_sim(user,business,user_sim,business_sim):
	for node1 in user:
		out1 = [x for x in G[node1]]
		weight1 = [G[node1][x]['weight'] for x in G[node1]]
		for node2 in user:
			out2 = [x for x in G[node2]]
			weight2 = [G[node2][x]['weight'] for x in G[node2]]
			num = sum([G[node1][y]['weight']*sum([G[node2][x]['weight']*business_sim[x][y] for x in out2]) for y in out1])	
			den = sum(weight1)*sum(weight2)
			user_sim[node1][node2] = C1*num/den

	for node1 in business:
		out1 = [x for x in G[node1]]
		weight1 = [G[node1][x]['weight'] for x in G[node1]]
		for node2 in business:
			out2 = [x for x in G[node2]]
			weight2 = [G[node2][x]['weight'] for x in G[node2]]
			num = sum([G[node1][y]['weight']*sum([G[node2][x]['weight']*user_sim[x][y] for x in out2]) for y in out1])	
			den = sum(weight1)*sum(weight2)
			business_sim[node1][node2] = C2*num/den
			
C1 = 0.8
C2 = 0.8
G = initialize()
print "initialized"
user = []
business = []
user_sim = {}
business_sim = {}

get_nodes_list(user,business)
print "get_node_lists done"

sim_initialize(G,user,business,user_sim,business_sim)
print "sim initialized"

for i in range(10):
	calculate_sim(user,business,user_sim,business_sim)

