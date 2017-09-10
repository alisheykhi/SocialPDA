
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
        print 'Harmonic measns of shortest path'
        self.measure['h_o'] = self.harmonic_mean(self.original_graph)
        self.measure['h_m'] = self.harmonic_mean(self.modified_graph)
        self.measure['h_s'] = self.harmonic_mean(self.sol_graph)
        print 'subgraph centrality'
        # self.measure['s_o'] = self.subgraph_centrality(self.original_graph)
        # self.measure['s_m'] = self.subgraph_centrality(self.modified_graph)
        # self.measure['s_s'] = self.subgraph_centrality(self.sol_graph)
        print 'modularity'
        #self.measure['m_o'] = self.modularity(self.original_graph)
        # self.measure['m_m'] = self.modularity(self.modified_graph)
        # self.measure['m_s'] = self.modularity(self.sol_graph)
        print 'transitivity'
        self.measure['t_o'] = self.transitivity(self.original_graph)
        # self.measure['t_m'] = self.transitivity(self.modified_graph)
        # self.measure['t_s'] = self.transitivity(self.sol_graph)
        return self.measure

    def harmonic_mean(self,graph):
        return harmonic_centrality(graph)
    def subgraph_centrality(self,graph):
        return nx.communicability_centrality(graph)
    def modularity(self,graph):
        return nx.modularity_spectrum(graph)
    def transitivity(self,graph):
        return nx.transitivity(graph)
    def max_eigenvalue_lambda(self,graph):
        pass
    def min_eigenvalue_mu(self,graph):
        pass