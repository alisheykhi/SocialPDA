
import networkx as nx
from harmonic_centrality import harmonic_centrality

class measurmnets:
    original_graph = nx.Graph()
    modified_graph = nx.Graph()
    sol_graph      = nx.Graph()
    measure = {}
    def __init__(self,original_graph, modified_graph,sol_graph):
        self.original_graph = original_graph
        self.modified_graph = modified_graph
        self.sol_graph      = sol_graph

    def calculate_measures(self):
        pass
    def harmonic_mean(self,graph):
        return harmonic_centrality(graph)
    def subgraph_centrality(self,graph):
        return nx.communicability_centrality(graph)
    def modularity(self,graph):
        return nx.modularity_spectrum(graph)
    def transitivity(self,graph):
        return nx.transitivity(graph)