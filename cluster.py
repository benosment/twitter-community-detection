import graph
import networkx as nx
import pdb
import numpy as np
from scipy import linalg
from scipy.cluster.vq import kmeans2
from sklearn.cluster import spectral_clustering
from sklearn import metrics

def scluster(G, num_clusters=3, threshold=2):
  # given a graph, calculate an affinity matrix
  D = distance(G)
  A = affinity(D, threshold=threshold)
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
  # calculate silhouette score
  s_score = metrics.silhouette_score(S, labels)
  return labels, s_score

def scluster2(G, num_clusters=3):
  n = G.number_of_nodes()
  if n < 100:
    n = n / 10 + 1
  else:
    n = n / 100 + 1
  print n
  D = distance(G)
  A = affinity(D, threshold = n)
  labels = spectral_clustering(A, n_clusters=num_clusters)
  return labels


def distance(G):
  "Given a graph, return a distance matrix"
  n = G.number_of_nodes()
  D = np.zeros((n,n))
  nodes = G.nodes()
  for i in range(n):
    for j in range(n):
      D[i][j] = len(nx.shortest_path(G, nodes[i], nodes[j])) - 1
  return D

def affinity(D, threshold=2):
  "Given a graph, calculate affinity"
  n = D.shape[0]
  A = np.zeros((n,n))
  # create node string -> index mapping and
  # index -> node string mapping
  for i in range(n):
    for j in range(n):
      A[i][j] = D[i][j] if D[i][j] <= threshold else 0
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

def find_best_params(G):
  highest_score = 0
  highest_num_cluster = 0
  highest_threshold = 0
  for i in range(2,10):
    for j in range(2,10):
      labels, s_score = scluster(g, i, j)
      if s_score > highest_score:
        highest_score = s_score
        highest_num_cluster = i
        highest_threshold = j
  return (highest_score, highest_num_cluster, highest_threshold)

if __name__ == '__main__':
  g = graph.get_graph('/data/512/10000-twitter.gexf', limit=10000)
  top_subgraphs = graph.get_subgraphs(g, k=1)
  g = top_subgraphs[0]
  #graph.display_graph(g)
  #graph.display_graph_clusters(g,labels)
  print find_best_params(g)

  # working!!
  # g = sample_graph()
  # graph.display_graph(g)
  # labels = scluster2(g,2)
  # graph.display_graph_clusters(g,labels)
