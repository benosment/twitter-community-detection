from sample import sample_tweets
from bson.objectid import ObjectId

import networkx as nx
import matplotlib.pyplot as plt
import pdb
import sys
import db

def get_mentions(tweet):
  return tweet['entities']['user_mentions']

def create_graph(tweets_cursor):
  g = nx.DiGraph() # do we care about the direction? multigraph?
  count = 0
  try: 
    while True:
      if count % 100 == 0:
        print "processing tweet %d" % count
      count += 1
      tweet = tweets_cursor.next()
      mentions = get_mentions(tweet)
      #pdb.set_trace()
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

def print_graph(graph, filename='graph.pdf'):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos)
    plt.savefig(filename, dpi=1000)
  
if __name__ == '__main__':
    tweets = db.get_tweets()
    g = create_graph(tweets)
    print_summary(g)
    print_graph(g)
    # how to save? 
    #save_graph(g)
