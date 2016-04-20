
import snap




class MicroPDA():
    g_phi = snap.TNEANet.New()


    def __init__(self, sorted_degree_sequence):
        self.create_phi_g(sorted_degree_sequence)


    def create_phi_g(self, degree):
        # add index field
        for i in range (0,len(degree)):
            degree[i]['index']=i+1
        # add node_zero or phi_0
        node_zero = dict(degree=0, id=-1, privacy_level=0 , index = 0)
        degree.insert(0,node_zero)

        self.create_graph_phi(degree)


    def create_graph_phi (self,degree):

        for node in degree:
            MicroPDA.g_phi.AddNode(node['index'])

        for i in range(0,len(degree)-4):
            j = i + int(degree[i+1]['privacy_level'])
            print j , i
            while (j <= i+2*(int(degree[j]['privacy_level']))-1) :
                MicroPDA.g_phi.AddEdge(i,j)

                degree_sum = 0
                weight = 0
                for id in range(i+1,j+1):
                    degree_sum += int(degree[id]['degree'])
                mu = (degree_sum/(j-i))
                for id in range(i+1,j+1):
                    weight += (int(degree[id]['degree'])-mu)^2

                j += 1

        node = 0
        edge = 0
        for NI in MicroPDA.g_phi.Nodes():
            node += 1
        for NI in MicroPDA.g_phi.Edges():
            edge += 1
        print "node: ",node ,"and edge: ",edge
        Length = snap.GetShortPath(MicroPDA.g_phi, 1, 26473)
        print Length


        '''
        count =0
        for i in range(0,len(MicroPDA.phi_G)-1):
            j = i + MicroPDA.phi_G[i+1]['privacy_level']
            while(j <= i + 2*(MicroPDA.phi_G[j-1]['privacy_level'])-1 ):
                MicroPDA.g_phi.AddEdge(i,j)
                j+=1
        print count
        '''
            #MicroPDA.phi_G.AddNode(node)








