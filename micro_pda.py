import networkx as nx

class MicroPDA():
    g_phi = nx.DiGraph()
    shortest_path = []
    omega_clusters = []
    removed_omega_clusters = []

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
        #print "shortest path is:",MicroPDA.shortest_path

        print "number of Omega Clusters: " + str(len(MicroPDA.shortest_path)-1)
        print "\n pruning:"
        for index in range(0,len(MicroPDA.shortest_path)-1):
            lb = int (MicroPDA.shortest_path[index])
            ub = int (MicroPDA.shortest_path[index+1])
            omega_cluster =[]
            for item in range(lb+1,ub+1):
                degree[item]['omega_cluster_index'] = index+1
                omega_cluster.append(degree[item])
            #pruning

            max_degree = 0
            min_degree = float("inf")
            for node in omega_cluster:
                max_degree = max(max_degree, node['degree'])
                min_degree = min(min_degree, node['degree'])
            if (max_degree-min_degree) >200: #threshold
                self.removed_omega_clusters.append(omega_cluster)
                print "difference between max degree and min degree in omega cluster %d is: %d" %(omega_cluster[1]['omega_cluster_index'],max_degree-min_degree)
            else:
                MicroPDA.omega_clusters.append(omega_cluster)
        print "\nfirst 10 omega cluster :"
        for z in range(0,10):
            print MicroPDA.omega_clusters[z]
        print "\nlast 10 omega cluster: "
        for z in range(len(MicroPDA.omega_clusters)-10,len(MicroPDA.omega_clusters)):
            print MicroPDA.omega_clusters[z]
        print "-----------------------------------------------------------"











