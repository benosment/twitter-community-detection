from sample import sample_tweets
import networkx as nx
import matplotlib.pyplot as plt
import pdb

def get_mentions(tweet):
  return tweet['entities']['user_mentions']

def create_graph():
  g = nx.DiGraph() # do we care about the direction? 
  global sample_tweets
  for tweet in sample_tweets:
    mentions = get_mentions(tweet)
    #pdb.set_trace()
    for mention in mentions:
      g.add_edge(tweet['user']['screen_name'], 
                 mention['screen_name'],
                 text = tweet['text'],
                 weight = 1)
  return g

def print_summary(graph):
    print "Number of nodes: %d" % graph.number_of_nodes()
    print "Number of edges: %d" % graph.number_of_edges()
    print "Node degrees:", sorted(nx.degree(graph))

def save_graph(graph, filename='graph.pdf'):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos)
    plt.savefig(filename, dpi=1000)
  
if __name__ == '__main__':
    g = create_graph()
    print_summary(g)
    save_graph(g)
