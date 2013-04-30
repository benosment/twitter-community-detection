from sample import sample_tweets
import networkx as nx

def get_mentions(tweet):
  return tweet['entities']['user_mentions']

def create_graph():
  g = nx.DiGraph() # do we care about the direction? 
  global sample_tweets
  for tweet in sample_tweets:
    mentions = get_mentions(tweet)
    for mention in mentions:
      g.add_edge(tweet['text'], 
                 tweet['user']['screen_name'], 
                 mention['screen_name'])
  return g


def main():
    create_graph()


