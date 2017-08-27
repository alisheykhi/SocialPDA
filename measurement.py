import networkx as nx

class Measurement():
    original_g = nx.Graph()
    modified_g = nx.Graph()
    def __init__(self, original_g, modified_g):
        self.original_g = original_g
        self.modified_g = modified_g

    def globalEfficiency(self,graph):
        pass

    def modularity (self , graph):
        pass

    def transitivity(self, graph):
        pass

    def subGraphCentrality(self,graph):
        pass

    def eigenvalueOfAdjacencyMatrix(self,graph):
        pass

    def eigenvalueOfLaplacianMatrix(self,graph):
        pass
