from sample import sample_tweets
from bson.objectid import ObjectId

import networkx as nx
import matplotlib.pyplot as plt
import pdb
import sys
import db

def get_mentions(tweet):
  return tweet['entities']['user_mentions']

def create_graph(tweets_cursor, limit=None): 
  g = nx.DiGraph() 
  count = 0
  try: 
    while True:
      if limit and count > limit:
        return g
      if count % 100 == 0:
        print "processing tweet %d" % count
      count += 1
      tweet = tweets_cursor.next()
      mentions = get_mentions(tweet)
      for mention in mentions:
        g.add_edge(tweet['user']['screen_name'], 
                   mention['screen_name'],
                   text = tweet['text'],
                   weight = 1)
  except StopIteration:
    pass # ok
  except Exception,e:
    # log instead? 
    print "Exception", e
    sys.exit(-1)
  return g

def print_summary(graph):
  print "Number of nodes: %d" % graph.number_of_nodes()
  print "Number of edges: %d" % graph.number_of_edges()
  undirected_graph = graph.to_undirected()
  subgraphs = nx.connected_component_subgraphs(undirected_graph)
  print "Number of connected component subgraphs: ", len(subgraphs)
  print "Largest subgraph: ", subgraphs[0].number_of_nodes()
  print "type: ", type(graph), type(subgraphs[0])
  save_graph(subgraphs[0], 'subgraph.png')

  # not implemented for directed types
  #  print "Average Clustering: %d" % nx.average_clustering(graph)
  #  print "Size of largest clique: %d" % nx.graph_clique_number(graph)
  #  print "Number of cliques: %d" % nx.graph_number_of_cliques(graph)

def print_graph(graph, filename='graph.png'):
  pos = nx.spring_layout(graph)
  nx.draw(graph, pos, with_labels=False, node_size=50)
  plt.savefig(filename)

def display_graph(graph):
  pos = nx.spring_layout(graph)
  nx.draw(graph, pos, with_labels=False, node_size=50)
  plt.show()

def save_graph(graph, filename):
  nx.write_gexf(graph, filename)

def load_graph(filename):
  return nx.read_gexf(filename)

def get_graph(graph_name, limit=100):
  try: # try to load the graph
    g = load_graph(graph_name)
  except IOError: # if there is an issue, create the graph
    tweets = db.get_tweets()
    g = create_graph(tweets, limit)
    save_graph(g, graph_name)
  return g

def get_subgraphs(graph, k=5):
  undirected_graph = graph.to_undirected()
  subgraphs = nx.connected_component_subgraphs(undirected_graph)
  return subgraphs[:k]

if __name__ == '__main__':
  g = get_graph('/data/512/100-twitter.gexf')
  print_summary(g)
  print_graph(g) #-- get a memory error with numpy at sacle

  
