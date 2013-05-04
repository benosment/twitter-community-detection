import graph
import networkx as nx
import pdb



if __name__ == '__main__':
  g = graph.get_graph('/data/512/10000-twitter.gexf', limit=10000)
  top_subgraphs = graph.get_subgraphs(g, k=1)
  subgraph = top_subgraphs[0]
  graph.display_graph(subgraph)
  graph.print_graph(subgraph, '10000-subgraph.png')
