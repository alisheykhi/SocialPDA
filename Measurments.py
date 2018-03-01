import community
import networkx as nx
from harmonic_centrality import harmonic_centrality
import pylab as pyl
import matplotlib as plt

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
        #a = self.harmonic_mean(self.original_graph)

        self.measure['h_o'] = self.harmonic_mean(self.original_graph,0)
        self.measure['h_o_1'] = self.harmonic_mean(self.original_graph,1)
        # self.measure['h_m'] = self.harmonic_mean(self.modified_graph)
        # self.measure['h_s'] = self.harmonic_mean(self.sol_graph)
        print 'subgraph centrality'
        x = (self.subgraph_centrality(self.original_graph))

        self.measure['s_o'] = self.subgraph_centrality(self.original_graph)
        # self.measure['s_m'] = self.subgraph_centrality(self.modified_graph)
        # self.measure['s_s'] = self.subgraph_centrality(self.sol_graph)
        print 'modularity'
        self.measure['m_o'] = self.modularity(self.original_graph)
        # self.measure['m_m'] = self.modularity(self.modified_graph)
        #self.measure['m_s'] = self.modularity(self.sol_graph)
        print 'transitivity'
        self.measure['t_o'] = self.transitivity(self.original_graph)
        # self.measure['t_m'] = self.transitivity(self.modified_graph)
        #self.measure['t_s'] = self.transitivity(self.sol_graph)
        #self.plotResults()
        return self.measure

    def harmonic_mean(self,graph,t):

        if t == 0 :
            h = harmonic_centrality(graph)
        else:
            h = nx.harmonic_centrality(graph)
        c = 0
        b = len(h)
        for key,value in h.iteritems():
            c+= value
        hinverse =  (c/float(b*(b-1)))
        return 1/hinverse
    def subgraph_centrality(self,graph):
        x = nx.communicability_centrality(graph)
        z = 0
        y = len(x)
        for key,value in x.iteritems():
            z+= value
        return (z/y)
    def modularity(self,G):
        #modularity = nx.modularity_spectrum(graph)
        partition = community.best_partition(G)
        mod = community.modularity(partition,G)
        return mod

        #part = community.best_partition(graph)
        #return community.modularity(part,graph)
    def transitivity(self,graph):
        return nx.transitivity(graph)
    def max_eigenvalue_lambda(self,graph):
        pass
    def min_eigenvalue_mu(self,graph):
        pass

    def plotResults(self):
        #print self._plotPoints
        x = []
        y = []
        o = []
        z = []
        for node, harmonic in self.measure['h_o'].items():
            x.append(node)
            y.append(harmonic)
        for node, harmonic in self.measure['h_s'].items():
            o.append(node)
            z.append(harmonic)

        pyl.plot(x, y)
        pyl.plot(o, z)
        pyl.grid(True)
        pyl.title('Orginal Harmonic means')
        pyl.xlabel('node')
        pyl.ylabel('Measure')
        pyl.savefig('o_h')
        pyl.show()