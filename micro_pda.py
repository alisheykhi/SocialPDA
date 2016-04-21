
import networkx as nx




class MicroPDA():
    g_phi = nx.DiGraph()
    shortest_path = []

    def __init__(self, sorted_degree_sequence):
        print "-----------------------------------------------------------"
        print "____________________MicroPDA_______________________________"
        print "-----------------------------------------------------------"
        for i in range (0,len(sorted_degree_sequence)):
            sorted_degree_sequence[i]['index']=i+1
        # add node_zero or phi_0
        node_zero = dict(degree=0, id=-1, privacy_level=0 , index = 0)
        sorted_degree_sequence.insert(0,node_zero)
        #print len(degree)
        self.find_shortest_path(sorted_degree_sequence)


    def find_shortest_path (self,degree):

        for i in range(0,len(degree)-2):
            j = i + int(degree[i+1]['privacy_level'])
            while (j <= len(degree)-1 and j <= i+2*(int(degree[j]['privacy_level']))-1) :
                degree_sum = 0
                weight = 0
                for id in range(i+1,j+1):
                    degree_sum += int(degree[id]['degree'])
                mu = (float(degree_sum)/(j-i))
                for id in range(i+1,j+1):
                    weight += ((int(degree[id]['degree'])- mu) ** 2)
                MicroPDA.g_phi.add_edge(i,j,weight=weight)
                j += 1
        MicroPDA.shortest_path = nx.dijkstra_path(MicroPDA.g_phi,source=0,target=int(degree[-1]['index']))
        print "shortest path is:"
        print MicroPDA.shortest_path
        print "-----------------------------------------------------------"
        return MicroPDA.shortest_path










