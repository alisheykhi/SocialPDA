
import math, random,sys
import numpy as np
import scipy.spatial as spp
import networkx as nx
import logging
import matplotlib.pyplot as plt
import tqdm
import pylab as pyl
import multiprocessing
from multiprocessing import Pool
from harmonic_centrality import harmonic_centrality
from networkx_viewer import Viewer
from matplotlib import pylab

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
        if abs(diff) % 2 != 0:
            if diff >0:
                diff -=1
                print self.rho_minus.pop(random.randrange(len(self.rho_minus)))
            if diff <0:
                diff +=1
                print self.rho_plus.pop(random.randrange(len(self.rho_plus)))
        diff = len(self.rho_minus) - len(self.rho_plus)
        print( 'diff : %d' %diff)
        if diff >= 0:
            print( "we should first delete 1/2 abs(delta(rho))) = %d edges in G:" % math.floor (abs(diff/2.0)))
            while len(self.rho_plus) <> len(self.rho_minus):
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
                            print 'remove edge %r,%r'%(s1,s2)
                            # print "remove edge %d,%d" %(s1,s2)
                            break
                    if bound >50:
                        logging.error('failed to remove edge %r,%r'%(s1,s2))
                        break

        if diff < 0:
            print( "we should first add 1/2 abs(delta(rho))) = %d edges in G:" % math.floor(abs(diff/2.0)))
            while len(self.rho_plus) <> len(self.rho_minus):
                bound = 0
                while True:
                    bound+=1
                    if  self.rho_minus and  self.rho_plus:
                        r1 = random.randrange(len(self.rho_plus)) - 1
                        r2 = random.randrange(len(self.rho_plus)) - 1
                        s1 = self.rho_plus.pop(r1)
                        s2 = self.rho_plus.pop(r2)
                        if s1 != s2:
                            if not self.edge_add(s1,s2):
                                self.rho_plus.insert(r1,s1)
                                self.rho_plus.insert(r2,s2)

                            else:
                                print 'add edge %r,%r'%(s1,s2)
                                break
                        if bound >50:
                            logging.error('failed to add edge %r,%r'%(s1,s2))
                            break


    def run_swarm(self):
        swarmPSO = SwarmBPSO (self.modified_graph, self.rho_plus, self.rho_minus, self.modified_omega_clusters)
        solution =  swarmPSO.initializeSwarm()
        return solution

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
        if bound < 50:
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
        else:
            return False

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



def fitness(graph):
    harmonicSum = 0
    #harmonic = nx.closeness_centrality(graph)
    harmonic = harmonic_centrality(graph)
    for key,value in harmonic.iteritems():
        harmonicSum += value
    return harmonicSum
    #
    # eigenSum = 0
    # #closeness = nx.closeness_centrality(graph,701)
    # eigenVector = nx.eigenvector_centrality(graph)
    # for key,value in eigenVector.items():
    #     eigenSum+=value
    # return eigenSum

class SwarmBPSO:
    solution = []
    swarm = []
    modified_g= []
    original_g  = nx.Graph()
    omega_cluster = []
    rho_minus = []
    rho_plus = []
    dimension = 1
    nof_particle = 100
    gBest = {'graph':None,'fitness': float('inf')}
    pBest = []
    newFitness = []
    logging.basicConfig()
    logger = logging.getLogger('SwarmBPSO')
    node_change = []
    generation =20
    original_f= 0
    velocity = []
    r1 = .2
    r2 = .6
    r3 = .3
    _plotPoints = []


    def __init__(self,original_graph, rho_plus, rho_minus, original_omega_cluster):
        self.original_g = original_graph
        self.omega_cluster = original_omega_cluster
        self.rho_minus = rho_minus
        self.rho_plus = rho_plus
        # print 'from init',len(self.rho_minus)
        # print 'from init',len(self.rho_plus)


    def initializeSwarm(self):
        print 'initializing Swarm'
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

        for dim in xrange(self.dimension) :
            particle_vel = []
            for particle in xrange(self.nof_particle):
                NoTrasnposition = random.randrange(1,len(self.rho_plus))
                alist =random.sample(xrange( len(self.rho_plus)), NoTrasnposition)
                blist =random.sample(xrange( len(self.rho_plus)), NoTrasnposition)
                transposition = []
                for f, b in zip(alist,blist):
                    if f <> b :
                        transposition.append((f, b))
                particle_vel.append(transposition)
            self.velocity.append(particle_vel)

        # print "calculate original FF ..."
        self.original_f = fitness(self.original_g)
        print "Original graph Fitness:" , self.original_f
        iter = 0
        self.gBest['fitness'] = float('inf')
        print 'iter -> %i'%iter,"\t-> \tBestFitness:", self.gBest['fitness']
        # print 'Edge switch:'
        for i,dim in enumerate(self.modified_g):
            for j,g in enumerate(dim):
                # indx = ((i)*self.nof_particle)+(j+1)
                for k,node in enumerate(self.swarm[i][j]):
                    self.edge_switch(g,node,self.rho_minus[k])
                # if (self.dimension*self.nof_particle) == indx:
                #     print '|','-' * (indx+1),'|', indx , '/' ,self.dimension*self.nof_particle
                # else:
                #     print '|','-' * indx,' ' * ((self.dimension*self.nof_particle)- indx),'|',indx , '/' ,self.dimension*self.nof_particle
        # print 'Calculate Fitness '
        for dim in self.modified_g:
            try:
                pool = Pool(multiprocessing.cpu_count())
                data_outputs = pool.map(fitness, dim)
            finally: # To make sure processes are closed in the end, even if errors happen
                pool.close()
                pool.join()
            self.newFitness.append(data_outputs)
        for i,dim in enumerate(self.modified_g):
            pbest_list = []
            for j,g in enumerate(dim):
                init_pbest = {}
                modified_fitness = self.newFitness[i][j]
                newfit = abs(self.original_f -  modified_fitness)
                init_pbest['fitness'],init_pbest['pi'] = abs(newfit),self.swarm[i][j]
                pbest_list.append(init_pbest)
                # indx = ((i)*self.nof_particle)+(j+1)
                # if (self.dimension*self.nof_particle) == indx:
                #     print '|','-' * (indx+1),'|', indx , '/' ,self.dimension*self.nof_particle
                # else:
                #     print '|','-' * indx,' ' * ((self.dimension*self.nof_particle)- indx),'|',indx , '/' ,self.dimension*self.nof_particle
            self.pBest.append(pbest_list)
        self._plotPoints.append( (0, self.gBest['fitness']) )
        # print 'New Fitness  :',self.newFitness
        # print 'Personal Best' , self.pBest
        self.Global_Best()

        for iter in range(self.generation):
            self.Update_Swarm()
            self.Personal_Best()
            self.Global_Best()
            gen = iter+1
            print "Generation", iter+1,"\t-> \tBestFitness:", self.gBest['fitness']
            self._plotPoints.append( (gen, abs(self.gBest['fitness'])) )
            self.modified_g = []
            for i in range(self.dimension):
                graphs = []
                for j in range(self.nof_particle):
                    graphs.append(self.original_g.copy())
                self.modified_g.append(graphs)
        #self.plotResults()
        #nx.write_graphml(self.gBest['graph'],'result.graphml')
        #self.save_graph(self.gBest['graph'],"result.pdf")
        sol = {}
        sol['modified'] = self.gBest['graph']
        sol['original'] = self.original_g
        return  sol
        # for i in range(generations):
        #     sc.updateSwarm(swarm)
        #     if swarm._bestPositionFitness < fitness:
        #         fitness = swarm._bestPositionFitness
        #         idx = i
        #     gen = i+1
        #     fit = swarm._bestPositionFitness
        #     self._plotPoints.append( (gen, fit) )
        #     print "Generation", i+1,"\t-> BestPos:", swarm._bestPosition, \
        #         "\tBestFitness:", swarm._bestPositionFitness
        # self.solution = swarm._bestPosition

    def Update_Swarm(self):
        #print 'Update Velocity'
        self.Update_Velocity()
        #print 'Update Position'
        self.Update_Positions()
        #print 'Update Fitness'
        del self.newFitness[:]
        for dim in self.modified_g:
            try:
                pool = Pool(multiprocessing.cpu_count())
                data_outputs = pool.map(fitness, dim)
            finally: # To make sure processes are closed in the end, even if errors happen
                pool.close()
                pool.join()
            self.newFitness.append(data_outputs)
        for i,dim in enumerate(self.modified_g):
            pb = []
            for j,g in enumerate(dim):
                modified_fitness = self.newFitness[i][j]
                self.newFitness[i][j] = abs(self.original_f -  modified_fitness)
                # indx = ((i)*self.nof_particle)+(j+1)
                # if (self.dimension*self.nof_particle) == indx:
                #     print '|','-' * (indx+1),'|', indx , '/' ,self.dimension*self.nof_particle
                # else:
                #     print '|','-' * indx,' ' * ((self.dimension*self.nof_particle)- indx),'|',indx , '/' ,self.dimension*self.nof_particle
        # print 'New Fitness: ',  self.newFitness

    def Update_Velocity(self):
        for i,dim in enumerate(self.velocity):
            for j,_lambda in enumerate(dim):
                t1 = self.truncation(self.r1,self.velocity[i][j])
                s1 = self.subtraction(self.swarm[i][j],self.pBest[i][j]['pi'])
                t2 = self.truncation(self.r2,s1)
                s2 = self.subtraction(self.swarm[i][j],self.gBest['pi'])
                t3 = self.truncation(self.r3,s2)
                c1 = self.concatenation(t1,t2)
                v = self.concatenation(c1,t3)
                self.velocity[i][j] = v

    def Update_Positions(self):
        # print 'Update Position'
        for i,dim in enumerate(self.swarm):
            for j,pos in enumerate(dim):
                self.swarm[i][j] = self.displacement(self.swarm[i][j],self.velocity[i][j])
                # indx = ((i)*self.nof_particle)+(j+1)
                for k,node in enumerate(self.swarm[i][j]):
                    self.edge_switch(self.modified_g[i][j],node,self.rho_minus[k])
                # if (self.dimension*self.nof_particle) == indx:
                #     print '|','-' * (indx+1),'|', indx , '/' ,self.dimension*self.nof_particle
                # else:
                #     print '|','-' * indx,' ' * ((self.dimension*self.nof_particle)- indx),'|',indx , '/' ,self.dimension*self.nof_particle

    def Personal_Best (self):
        # print 'Update Personal Best'
        for i,dim in enumerate(self.pBest):
            for j,pbest in enumerate(dim):
                # indx = ((i)*self.nof_particle)+(j+1)
                # if (self.dimension*self.nof_particle) == indx:
                #     print '|','-' * (indx+1),'|', indx , '/' ,self.dimension*self.nof_particle
                # else:
                #     print '|','-' * indx,' ' * ((self.dimension*self.nof_particle)- indx),'|',indx , '/' ,self.dimension*self.nof_particle
                if (abs(pbest['fitness']) > abs(self.newFitness[i][j])):
                    self.pBest[i][j]['fitness'],self.pBest[i][j]['pi'] = self.newFitness[i][j],self.swarm[i][j]

    def Global_Best(self):
        # print 'Update Global Best'
        for i,dim in enumerate(self.pBest):
            for j,pbest in enumerate(dim):
                # indx = ((i)*self.nof_particle)+(j+1)
                # if (self.dimension*self.nof_particle) == indx:
                #     print '|','-' * (indx+1),'|', indx , '/' ,self.dimension*self.nof_particle
                # else:
                #     print '|','-' * indx,' ' * ((self.dimension*self.nof_particle)- indx),'|',indx , '/' ,self.dimension*self.nof_particle
                if (abs(self.gBest['fitness']) > abs(pbest['fitness'])):
                    self.gBest['fitness'],self.gBest['graph'],self.gBest['pi'] = pbest['fitness'],self.modified_g[i][j],pbest['pi']
        # print 'global best :', abs(self.gBest['fitness'])
        # calculate global best

    def eigenfitness(self,graph):
        pass

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
                    #self.logger.warning('edge switch failed (no neighbor) node1 = %s , node2= %s, neighbors1 = %s' % (node1,node2,neighbors1))
                    return False
                neighbors1.remove(pivot[0])
                if pivot[0] not in neighbors2 and pivot[0] != node1:
                    break
                if bound > (len(graph.neighbors(node1))+5):
                    self.logger.warning('there is no pivot node for edge switch, try 50 times. node1=%r,node2=%r'%(node1,node2))
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

    def transposition (self,position = [], lambda_tuple = (), *args):
        position[lambda_tuple[0]],position[lambda_tuple[1]] = position[lambda_tuple[1]],position[lambda_tuple[0]]
        return position

    def truncation (self, r, velocityList= [], *args):
        del velocityList[int(r*len(velocityList)):]
        return velocityList

    def concatenation (self, velocityList1= [], velocityList2= [] , *args):
        return velocityList1+velocityList2

    def displacement (self, positionList= [], velocityList = [] , * args ):
        vel = []
        while velocityList:
            vel.append(velocityList.pop())
        for _ in range(0,len(vel)):
            self.transposition(positionList ,vel.pop())
        return positionList

    def subtraction (self, positionList1 = [], positionList2 = [], *args ):
        velocityList = []
        flag = [False] * len(positionList1)
        pos1 = positionList1[:]
        pos2 = positionList2[:]
        for i, posx in enumerate(pos1):
            for j, posy in enumerate(pos2):
                if not flag[j] and posx == posy:
                    velocityList.append((posx,j))
                    flag[j] = True
        return self.__selectionSort(velocityList)

    def __selectionSort(self,alist):
        lambda_tuple =[]
        for fillslot in range(len(alist)-1,0,-1):
            positionOfMax=0
            for location in range(1,fillslot+1):
                if alist[location][1]>alist[positionOfMax][1]:
                    positionOfMax = location
            if fillslot != positionOfMax :
                alist[fillslot],alist[positionOfMax] = alist[positionOfMax],alist[fillslot]
                lambda_tuple.append((fillslot,positionOfMax))
        return lambda_tuple

    def plotResults(self):
        x = []
        y = []
        for (generation, fitness) in self._plotPoints:
            x.append(generation)
            y.append(fitness)

#            print "%d" % (fitness)
        pyl.plot(x, y)

        pyl.grid(True)
        pyl.title('Swarm PDA')
        pyl.xlabel('Generation (i)')
        pyl.ylabel('Fitness')
        pyl.savefig('swarm_pda_plot')
        pyl.show()

    def save_graph(self,graph,file_name):
        #initialze Figure
        plt.figure(num=None, figsize=(20, 20), dpi=80)
        plt.axis('off')
        fig = plt.figure(1)
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph,pos)
        nx.draw_networkx_edges(graph,pos)
        nx.draw_networkx_labels(graph,pos)

        cut = 1.00
        xmax = cut * max(xx for xx, yy in pos.values())
        ymax = cut * max(yy for xx, yy in pos.values())
        plt.xlim(0, xmax)
        plt.ylim(0, ymax)

        plt.savefig(file_name,bbox_inches="tight")
        pylab.close()
        del fig
1
