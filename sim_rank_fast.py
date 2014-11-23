import networkx as nx
import collections
import random
import math
import sys

def initialize():
  G = nx.read_edgelist("data/edges.txt", nodetype=str, data=(('weight',float),))
  # 'Uf61AA2JUGWTcxSXNoGaXg', 'xGz3WSkC96aWtqt7vE70gw'
  return G

def print_progress(i, total):
  sys.stdout.write('\r')
  sys.stdout.write('{0: .1f}%'.format(float(i)/total*100))
  sys.stdout.flush()

################### CONSTANTS ###################
R = 100  # Number of Random Walkers
T = 11    # Random walk length
C = 0.8   # Discount factor
D = 1-C   # The diagonal value of matrix D
Q = 5     # Number of indexing Random Walkers
P = 10    # Number of preprocessing iters
theta = .1 # Upper bound threshold
#################################################

class SimRankFast(object):
  """Implements a scalable SimRank calculation Algorithm
     based on the work of Maehara et al """

  # Public Functions
  def __init__(self, graph):
    self.G = graph

  def single_pair(self, u, v, R):
    '''Single pair similarity'''
    # Initialize our random walkers
    u_positions = [u]*R
    v_positions = [v]*R
    
    ct = 1 #C^t

    result = 0
    for t in range(T):
      u_counts = collections.Counter(u_positions)
      v_counts = collections.Counter(v_positions)
      for w in set(u_positions) & set(v_positions):
        alpha = u_counts[w]
        beta = v_counts[w]
        result += alpha*beta*ct # Equation (14) 
    
      self.random_step(u_positions)
      self.random_step(v_positions)
        
      ct *= C

    result *= D/(R*R)
    return result

  def Indexing(self):
    '''Preprocessing step'''
    index = {}
    for i, u in enumerate(self.G.nodes_iter()):
      print_progress(i, G.number_of_nodes())
      index[u] = set([])
      for i in range(P):
        W = [self.random_walk(u, T) for _ in range(Q+1)]
        for t in range(T):
          v = W[0][t]
          n_occurs = 0 # TODO: Is this correct?
          for j in range(1, Q+1):
            if W[j][t] == v:
              n_occurs += 1
              if n_occurs > 1:
                index[u].add(v)
                break

    self.index = index

  def prune(self, u, S):
    result = []
    beta, gamma = self.ComputeAlphaBeta(u), self.ComputeGamma(u)
    
    for v in S:
      d = nx.shortest_path_length(self.G, u, v)
      if beta[d] < theta or gamma[d] < theta: continue
      result.append(v)

    return result

  def Query(self, u):
    s = {} # s[v] = s(u,v)
    S = [v for v in self.index[u] if u in self.index[v]] # TODO: correct?
    S = self.prune(u, S)
    for v in S:
      if self.single_pair(u, v, 10) >= theta:
        s[v] = self.single_pair(u, v, 100)
    
    # return [(most_similar_id, sim),... ,(least_similar_id, sim)]
    return sorted(s.items(), reverse=True, key=lambda tup: tup[1])


  def ComputeAlphaBeta(self, u):
    # Initialize our random walkers
    u_positions = [u]*R

    alpha = collections.defaultdict(int) # alpha[(d, t)] = alpha(u, d, t)
    for t in range(T):
      counts = collections.Counter(u_positions)
      for w in counts:
        mu = D * counts[w] / R
        d = nx.shortest_path_length(self.G, u, w)
        alpha[(d, t)] = max(alpha[(d, t)], mu)
      
      self.random_step(u_positions)

    beta = collections.defaultdict(int) # beta[d] = beta(u, d)
    for d in range(T):
      ct = 1 # C^t
      for t in range(T):
        beta[d] += ct*max(alpha[(dprime, t)] for dprime in range(d-t, d+t+1))
        ct *= C
    
    return beta


  def ComputeGamma(self, u):
    gamma = {} #gamma[t] = gamma(u, t)

    u_positions = [u]*R
    for t in range(T):
      mu = 0
      counts = collections.Counter(u_positions)
      for w in counts:
        mu += D * counts[w]**2 / (R**2)

      gamma[t] = math.sqrt(mu)
      self.random_step(u_positions)

    return gamma



  def random_step(self, nbunch): #TODO: BIPARTITE THIS
    '''Take a random step for multiple nodes in place'''
    for r in range(len(nbunch)):
        nbunch[r] = random.choice(self.G.neighbors(nbunch[r])) # Random step
  

  def random_walk(self, u, k):
    walk = []
    prev = u
    for i in range(k):
      next = random.choice(self.G.neighbors(prev))
      walk.append(next)
      prev = next
    return walk



G = initialize()
print 'Initialized'
#G = nx.read_edgelist("../CA-GrQc.txt", nodetype=int)
#G = nx.Graph([(1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (3, 6)])
Sim = SimRankFast(G)
print 'Indexing...'
Sim.Indexing()
import pdb; pdb.set_trace()
print Sim.Query(1)