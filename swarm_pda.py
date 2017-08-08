
import math, random,sys
import numpy as np
import scipy.spatial as spp
import networkx as nx
import logging
import matplotlib.pyplot as plt
import tqdm

class SwarmPDA():
    rho_plus = []
    rho_minus = []
    delta_rho = 0
    orginal_graph = nx.Graph()
    modified_graph = nx.Graph()
    orginal_omega_clusters = []
    modified_omega_clusters = []
    logging.basicConfig()
    logger = logging.getLogger('SwarmPDA')

    def __init__(self, omega_clusters, graph_G):

        print( "____________________SwarmPDA____________________________")
        print( "-----------------------------------------------------------\n\n")
        self.orginal_graph = graph_G
        self.modified_graph = graph_G.copy()
        self.orginal_omega_clusters = omega_clusters
        self.modified_omega_clusters = omega_clusters
        rho = 0
        for cluster in self.orginal_omega_clusters:
            for node in cluster :
                if node ['avg'] <> 0: # if node not removed
                    rho = int (node['degree'] - node ['avg']) # differences between original and anonymized degree
                    node['rho'] = rho
                    if rho > 0:
                        for time in range (0,rho):
                            self.rho_minus.append(node['id']) # a set of nodes whose degree should be decreased
                    if rho < 0:
                        for time in range (0,-rho):
                            self.rho_plus.append(node['id'])# a set of nodes whose degree should be increased
                else :
                    node['rho'] = 0
        print( "top omega cluster with rho parameter")
        for item in range(0,10):
            print( self.orginal_omega_clusters[item])
        print( "len Rho Minus is %d" % len(self.rho_minus))
        print( "len Rho Plus is %d" %len(self.rho_plus))
        #print((list(self.modified_graph.edges())))
        diff = len(self.rho_minus) - len(self.rho_plus)
        print( 'diff : %d' %diff)
        if diff % 2 != 0:
            if diff >0:
                diff-=1
                self.rho_minus.pop(random.randrange(len(self.rho_minus)))
            if diff <0:
                diff +=1
                self.rho_plus.pop(random.randrange(len(self.rho_plus)))
        if diff > 0:
            print( "we should first delete 1/2 abs(delta(rho))) = %d edges in G:" % math.floor (abs(diff/2.0)))
            while diff > 0:
                bound = 0
                while True:
                    bound+=1
                    r1 = random.randrange(len(self.rho_minus))
                    r2 = random.randrange(len(self.rho_minus))
                    s1 = self.rho_minus.pop(r1)
                    s2 = self.rho_minus.pop(r2)
                    if s1 != s2:
                        if not self.edge_removal(s1,s2):
                            self.rho_minus.insert(r1,s1)
                            self.rho_minus.insert(r2,s2)
                        else:
                            # print "remove edge %d,%d" %(s1,s2)
                            break
                    if bound >50:
                        logging.error('failed to remove edge %d,%d'%(s1,s2))
                        break
                diff -= 2

        if diff < 0:
            print( "we should first add 1/2 abs(delta(rho))) = %d edges in G:" % math.floor(abs(diff/2.0)))
            while diff < 0:
                bound = 0
                while True:
                    bound+=1
                    r1 = random.randrange(len(self.rho_plus))
                    r2 = random.randrange(len(self.rho_plus))
                    s1 = self.rho_plus.pop(r1)
                    s2 = self.rho_plus.pop(r2)
                    if s1 != s2:
                        if not self.edge_add(s1,s2):
                            self.rho_plus.insert(r1,s1)
                            self.rho_plus.insert(r2,s2)
                        else:
                            # print "add edge %d,%d" %(s1,s2)
                            break
                    if bound >50:
                        logging.error('failed to add edge %d,%d'%(s1,s2))
                        break
                diff += 2


        print 'final Rho diff :', len(self.rho_minus)-len(self.rho_plus)
        # add_rmv= 0
        #
        # for i in range(0,len(DecDegNode),2):
        #     bound = 0
        #     while True:
        #         bound+=1
        #         s1 = random.choice(DecDegNode)
        #         s2 = random.choice(DecDegNode)
        #         if s1 != s2:
        #             if self.edge_removal(s1,s2):
        #                 DecDegNode.remove(s1)
        #                 DecDegNode.remove(s2)
        #                 add_rmv += 1
        #                 #print( 'remove edge (%d,%d)'%(s1,s2))
        #                 break
        #             else:
        #                 self.logger.warning('failed to remove edge %d,%d'%(s1,s2))
        #         if bound >50:
        #             break
        #
        # for i in range(0,len(IncDegNode),2):
        #     bound =0
        #     while True:
        #         bound +=1
        #         s1 = random.choice(IncDegNode)
        #         s2 = random.choice(IncDegNode)
        #         if s1 != s2:
        #             if self.edge_add(s1,s2):
        #                 IncDegNode.remove(s1)
        #                 IncDegNode.remove(s2)
        #                 add_rmv += 1
        #                 print( 'add edge %d : (%d,%d)'% (add_rmv,s1,s2))
        #                 break
        #             else:
        #                 self.logger.warning( 'failed to add edge %d,%d'%(s1,s2))
        #         if bound>50:
        #             break
        # i =0
        # randomlist = random.sample(xrange(len(self.rho_plus)), len(self.rho_plus))
        # if len(self.rho_minus) == len(self.rho_plus):
        #     for index in randomlist:
        #         self.edge_switch(self.rho_minus[index],self.rho_plus[i])
        #         i+=1
        #         #print('edge switch node1 = %d, node2 = %d' %(self.rho_minus[i],self.rho_plus[i]))
        # else:
        #     self.logger.warning('rho minus <> rho_plus')

        swarmPSO = SwarmBPSO (self.modified_graph, self.rho_plus, self.rho_minus, self.modified_omega_clusters)
        swarmPSO.initializeSwarm()







    def edge_removal (self, node1, node2):
        bound = 0
        neighbors1,neighbors2,neighbor1,neighbor2 = None,None,None,None
        if self.modified_graph.degree(node1)==self.modified_graph.degree(node1)==1\
                or node2 in self.modified_graph.neighbors(node1)\
                or node1 == node2:
            self.logger.warning('edge removal failed node1 = %s , node2= %s' % (node1,node2))
            return False
        while True:
            bound +=1
            neighbors1 = self.modified_graph.neighbors(node1)
            neighbor1 = random.choice(neighbors1)
            neighbors1.remove(neighbor1)
            neighbors2 = self.modified_graph.neighbors(node2)
            neighbor2 = random.choice(neighbors2)
            neighbors2.remove(neighbor2)
            if not self.modified_graph.has_edge(neighbor1,neighbor2)\
                    and neighbor1 != node1\
                    and neighbor2 != node2:
                break
            if bound > 50:
                self.logger.warning('there is no pivot node for edge removal,try 50 times')
                break
        self.modified_graph.remove_edge(node1,neighbor1)
        self.modified_graph.remove_edge(node2,neighbor2)
        self.modified_graph.add_edge(neighbor1,neighbor2)
        # edit modified omega cluster
        for cluster in self.modified_omega_clusters:
            for node in cluster:
                if node['id'] in [node1,node2]:
                    node['degree'] -=1
                    node['rho'] -= 1
        return True

    def edge_add (self, node1, node2):
        if node1 in self.modified_graph.neighbors(node2) or node1 == node2:
            self.logger.warning('edge add failed node1 = %s , node2= %s' % (node1,node2))
            return False
        else:
            self.modified_graph.add_edge(node1,node2)
            for cluster in self.modified_omega_clusters:
                for node in cluster:
                    if node['id'] in [node1,node2]:
                        node['degree'] +=1
                        node['rho'] += 1
        return True




class SwarmBPSO:
    solution = []
    swarm = []
    modified_g= []
    original_g  = nx.Graph()
    omega_cluster = []
    rho_minus = []
    rho_plus = []
    dimension = 2
    nof_particle = 3
    gBest = []
    pBest = []
    logging.basicConfig()
    logger = logging.getLogger('SwarmBPSO')
    node_change = []


    def __init__(self,original_graph, rho_plus, rho_minus, original_omega_cluster):
        self.original_g = original_graph
        self.omega_cluster = original_omega_cluster
        self.rho_minus = rho_minus
        self.rho_plus = rho_plus


    def initializeSwarm(self):
        for i in range(self.dimension):
            positions = []
            graphs = []
            for j in range(self.nof_particle):
                pi_plus =list( self.rho_plus)
                random.shuffle(pi_plus)
                positions.append(pi_plus)
                graphs.append(self.original_g.copy())
            self.swarm.append(positions)
            self.modified_g.append(graphs)

        # modify graph based on new rho_plus

        # calculate personal best for every particle

        print "calculate original FF ..."
        original_fitness = self.fitness(self.original_g)
        print "Original FF is:" , original_fitness
        print 'Edge switch:'
        for i,dim in enumerate(self.modified_g):
            for j,g in enumerate(dim):
                indx = ((i)*self.nof_particle)+(j+1)
                if (self.dimension*self.nof_particle) == indx:
                    print '|','-' * (indx+1),'|', indx , '/' ,self.dimension*self.nof_particle
                else:
                    print '|','-' * indx,' ' * ((self.dimension*self.nof_particle)- indx),'|',indx , '/' ,self.dimension*self.nof_particle
                for k,node in enumerate(self.swarm[i][j]):
                    self.edge_switch(g,node,self.rho_minus[k])
        print 'personal best:'
        for i,dim in enumerate(self.modified_g):
            pb = []
            for j,g in enumerate(dim):
                indx = ((i)*self.nof_particle)+(j+1)
                if (self.dimension*self.nof_particle) == indx:
                    print '|','-' * (indx+1),'|', indx , '/' ,self.dimension*self.nof_particle
                else:
                    print '|','-' * indx,' ' * ((self.dimension*self.nof_particle)- indx),'|',indx , '/' ,self.dimension*self.nof_particle
                modified_fitness = self.fitness(g)
                pb.append( abs(original_fitness -  modified_fitness))

            self.pBest.append(pb)
        print self.pBest
        # calculate global best


    def fitness(self,graph):
        eigenSum = 0
        #closeness = nx.closeness_centrality(graph,701)
        eigenVector = nx.eigenvector_centrality(graph)
        for key,value in eigenVector.items():
            eigenSum+=value
        return eigenSum

    def edge_switch (self,graph, node1, node2):
        bound =0
        if node1==node2:
            self.logger.warning('edge switch failed node1 = %s , node2= %s' % (node1,node2))
            return False
        else:

            neighbors1 =graph.neighbors(node1)
            neighbors2 = graph.neighbors(node2)
            while True:
                bound+=1
                try:
                    pivot = (0,float('inf'))
                    for node in graph.degree_iter(neighbors1):
                        if node[1] < pivot[1]:
                            pivot = node
                except:
                    self.logger.warning('edge switch failed (no neighbor) node1 = %s , node2= %s' % (node1,node2))
                    return False
                #print pivot[0], neighbors1
                if  not neighbors1:
                    self.logger.warning('edge switch failed (no neighbor) node1 = %s , node2= %s, neighbors1 = %s' % (node1,node2,neighbors1))
                    return False
                neighbors1.remove(pivot[0])
                if pivot[0] not in neighbors2 and pivot[0] != node1:
                    break
                if bound > (len(graph.neighbors(node1))+5):
                    self.logger.warning('there is no pivot node for edge switch, try 50 times. node1=%d,node2=%d'%(node1,node2))
                    break

            graph.remove_edge(node1,pivot[0])
            graph.add_edge(node2,pivot[0])
            # for cluster in self.omega_cluster:
            #     for node in cluster:
            #         if node['id']  == node1:
            #             node['degree'] -=1
            #             node['rho'] -= 1
            #         if node['id']  == node2:
            #             node['degree'] +=1
            #             node['rho'] += 1
            #print 'perform edge switch ',node1,'->',node2
        return True











# class ParticleSwarmOptimizer:
#     solution = []
#     swarm = []
#     gBest = []
#
#
#     def __init__(self):
#         return
#
#     def initParticle(self):
#         for h in range(ParticlePDA.swarmSize):
#             self.swarm.append(Particle())
#         self.gBest = self.swarm[0].pBest
#
#     def optimize(self):
#         print ParticlePDA.globalBest
#
#         for i in range(ParticlePDA.iterations): # 0 -> iter-1
#             print self.gBest , self.f(self.gBest)
#             print "iteration ", i+1 ,"---------------------------"
#             for j in range(ParticlePDA.swarmSize):
#                 pBest = self.swarm[j].pBest
#                 if self.f(pBest) < self.f(self.gBest):
#                     print "first Global",self.f(self.gBest)
#                     gBest = pBest
#                     print "second one",self.f(self.gBest)
#                     print self.gBest
#                 #Update position of each paricle
#                 self.swarm[j].updatePositions(self.gBest)
#                 #print self.solution,"sol"
#                 #self.swarm[k].satisfyConstraints()
#             #Update the personal best positions
#                 if self.f(self.swarm[j].pos) < self.f(self.swarm[j].pBest):
#                     self.swarm[j].pBest = self.swarm[l].pos
#
#         return self.solution
#
#     def f(self, particle):
#         return ((ParticlePDA.beta * self.f1(particle) )+((1-ParticlePDA.beta) * self.f2(particle)))
#
#     def f2(self,particle):
#         sumarray =[]
#         i = 0
#         for x in particle:
#             diff =0
#             for node in ParticlePDA.omega_cluster[i]:
#                 if x:
#                     diff += node['degree'] - math.ceil((ParticlePDA.avg_clusters[i]['avg']))
#                 else:
#                     diff += node['degree'] - math.floor((ParticlePDA.avg_clusters[i]['avg']))
#             i += 1
#             sumarray.append(diff)
#         return math.fabs(sum(sumarray))
#
#     def f1(self,particle):
#         sumarray =[]
#         i = 0
#         for x in particle:
#             diff =0
#             for node in ParticlePDA.omega_cluster[i]:
#                 if x:
#                     diff += math.fabs(node['degree'] - math.ceil((ParticlePDA.avg_clusters[i]['avg'])))
#                 else:
#                     diff +=math.fabs(node['degree'] - math.floor((ParticlePDA.avg_clusters[i]['avg'])))
#             i += 1
#             sumarray.append(diff)
#         return (sum(sumarray))
#     # This class contains the particle swarm optimization algorithm
#
# class Particle:
#
#     def __init__(self):
#         self.pos = np.random.randint(2, size = ParticlePDA.dimension)
#         self.velocity = np.random.ranf(size=ParticlePDA.dimension)
#         self.pBest = self.pos
#
#         # self.pos = np.random.randint(2, size = ParticlePDA.dimension)
#         # self.velocity = np.random.ranf(size=ParticlePDA.dimension)
#
#     def updatePositions(self, gBest):
#         for i in range(ParticlePDA.dimension):
#             r1 = random.random()
#             r2 = random.random()
#             social = float(ParticlePDA.c1 * r1 * (gBest[i] - self.pos[i]))
#             cognitive = float(ParticlePDA.c2 * r2 * (self.pBest[i] - self.pos[i]))
#             velocity = social + cognitive
#             if abs(velocity) > ParticlePDA.vmax and abs(velocity) is velocity:
#                 velocity = ParticlePDA.vmax
#             elif abs(velocity) > ParticlePDA.vmax:
#                 velocity = -ParticlePDA.vmax
#             self.velocity[i] =  velocity #+ (ParticlePDA.w * self.velocity[i])
#             if np.random.rand(1) < self.sigmoid(self.velocity[i]):
#                 self.pos[i] = 0
#             else:
#                 self.pos[i] = 1
#         return
#
#     def sigmoid (self, x):
#         return 1 / (1+ math.exp(-x))
#
#     def satisfyConstraints(self):
#         #This is where constraints are satisfied
#         return
