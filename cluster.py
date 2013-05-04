import graph
import networkx as nx
import pdb
import numpy as np
from scipy import linalg
from scipy.cluster.vq import kmeans2
from sklearn.cluster import spectral_clustering
def scluster(subgraph):
  pass

def diag_example():
  a = np.matrix([[4, 1], [-8, -5]])
  d = a.diagonal()
  print "Adjacency Matrix:", a
  print "Diagonal Matrix:", d

def eig_example():
  A = np.array([[1,2], [3,4]])
  la,v = linalg.eig(A)
  l1,l2 = la
  print "Eigenvalues: ", l1, l2 
  print "First eigenvector: ", v[:,0]
  print "Second eigenvector: ", v[:,1]
  
def scluster_example():
  A = np.array([[0,1,1,1,0,0,0,0,0],
                [1,0,1,0,0,0,0,0,0],
                [1,1,0,1,0,0,0,0,0],
                [1,0,1,0,1,1,0,0,0],
                [0,0,0,1,0,1,1,1,0],
                [0,0,0,1,1,0,1,1,0],
                [0,0,0,0,1,1,0,1,1],
                [0,0,0,0,1,1,1,0,0],
                [0,0,0,0,0,0,1,0,0]])
  print scluster(A, 3)


def scluster(G, num_clusters=3):
  # given a graph, calculate an affinity matrix
  #D = distance(G)
  A = affinity(G)
  # given an affinity matrix
  # calculate the diagonal
  D = diagonal(A)
  # calculate the Laplacian matrix, L
  L = D - A
  # find the eigenvalues and vectors of L
  eigen_values, eigen_vectors = linalg.eig(L)
  # use the smallest eigenvectors
  vals = dict(zip(eigen_values, eigen_vectors.transpose()))
  keys = vals.keys()
  keys.sort()
  S = np.array([vals[k] for k in keys[:num_clusters]]).transpose()
  # return the labels based on kmeans of smallest eigenvectors
  clusters, labels = kmeans2(S, k=num_clusters, iter=30, minit='points')
  return labels

def scluster2(G, num_clusters=3):
  D = distance(G)
  A = affinity(D)
  labels = spectral_clustering(A, n_clusters=num_clusters)
  return labels


def distance(G):
  "Given a graph, return a distance matrix"
  n = G.number_of_nodes()
  D = np.zeros((n,n))
  nodes = G.nodes()
  for i in range(len(nodes)):
    for j in range(len(nodes)):
      D[i][j] = len(nx.shortest_path(G, nodes[i], nodes[j])) - 1
  return D

def affinity(G, closeness=2):
  "Given a graph, calculate affinity"
  n = G.number_of_nodes()
  A = np.zeros((n,n))
  # create node string -> index mapping and
  # index -> node string mapping
  i = 0
  i2s = {}
  s2i = {}
  for node in G.nodes():
    i2s[i] = node
    s2i[node] = i
    i +=1 
  # affinty based on direct neighbors
  for (v,w) in G.edges():
    A[s2i[v]][s2i[w]] = 1
    A[s2i[w]][s2i[v]] = 1
  return A

def diagonal(A):
  n = A.shape[0]
  D = np.zeros((n,n))
  for i in range(n):
    for j in range(n):
      if A[i][j] == 1:
        D[i][i] += 1
  return D

def sample_graph():
  g = nx.Graph()
  g.add_edge(1,2)
  g.add_edge(1,3)
  g.add_edge(1,4)
  g.add_edge(2,3)
  g.add_edge(3,4)
  g.add_edge(4,5)
  g.add_edge(4,6)
  g.add_edge(5,6)
  g.add_edge(5,7)
  g.add_edge(5,8)
  g.add_edge(6,7)
  g.add_edge(6,8)
  g.add_edge(7,8)
  g.add_edge(7,9)
  return g

if __name__ == '__main__':
  g = graph.get_graph('/data/512/100-twitter.gexf', limit=100)
  top_subgraphs = graph.get_subgraphs(g, k=1)
  g = top_subgraphs[0]
  graph.display_graph(g)
  labels = scluster2(g,2)
  graph.display_graph_clusters(g,labels)

  # working!!
  # g = sample_graph()
  # graph.display_graph(g)
  # labels = scluster(g,3)
  # graph.display_graph_clusters(g,labels)
