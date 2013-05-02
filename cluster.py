from sklearn.cluster import spectral_clustering
import graph
import numpy as np

'''
Largely taken from this example: 
http://scikit-learn.org/stable/auto_examples/cluster/plot_segmentation_toy.html#example-cluster-plot-segmentation-toy-py
'''

def scluster(g):
  # TODO -- does this work? what kind of graph is returned from scikit example
  graph.data = np.exp(-graph.data / graph.data.std())
  
  # how many clusters is good?
  labels = spectral_clustering(g, n_clusters=4, eigen_solver='arpack')


if __name__ == '__main__':
  g = graph.get_graph('/data/512/100-twitter.gexf')
  scluster(g)
