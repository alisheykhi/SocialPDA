
import math, random,sys
import numpy as np
import scipy.spatial as spp
from Models import *
from Controllers import *
import pylab as pyl

class ParticlePDA():
    differences =[]
    clusters = []
    avg_clusters = []
    beta = 0
    _plotPoints = []
    solution = []
    clusters_avg_embedded = []

    def __init__(self,omega_clusters,beta):
        print "____________________ParticlePDA____________________________"
        print "-----------------------------------------------------------"
        self.beta = float(beta)
        for cluster in omega_clusters:
            avg_info = {}
            sum, avg  = 0 , 0
            for node in cluster:
                sum += int (node['degree'])
            avg = float (sum)/len(cluster)
            for node in cluster:
                node['avg'] = avg
            if not avg.is_integer():
                self.clusters.append(cluster)
                avg_info['avg'] = avg
                avg_info['omega_cluster_index'] = cluster[0]['omega_cluster_index']
                self.avg_clusters.append(avg_info)

            else:
                self.clusters_avg_embedded.append(cluster)


        self._popSize = popSize = 50
        self._dimensions = dimensions  = len(self.clusters)
        self._generations = generations = 10
        print "number of particle :",dimensions
        print "\nBinary PSO output:"
        swarm   = SwarmModel()
        sc      = SwarmController("binary",self.beta,self.clusters,self.avg_clusters)
        sc.initSwarm(swarm, "binary", popSize, dimensions)
        fitness = 1
        idx = 0
        for i in range(generations):
            sc.updateSwarm(swarm)
            if swarm._bestPositionFitness < fitness:
                fitness = swarm._bestPositionFitness
                idx = i
            gen = i+1
            #fit = dimensions - (dimensions * swarm._bestPositionFitness)
            fit = swarm._bestPositionFitness
            self._plotPoints.append( (gen, fit) )
#            self._plotPoints += (i+1, 1 - swarm._bestPositionFitness)
            print "Generation", i+1,"\t-> BestPos:", swarm._bestPosition, \
                "\tBestFitness:", swarm._bestPositionFitness
        self.solution = swarm._bestPosition

    def clusterWithAvg(self):
        i = 0
        for x in self.solution:
            if x:
                for node in self.clusters[i]:
                    node['avg']= math.ceil((self.avg_clusters[i]['avg']))
            else:
                for node in self.clusters[i]:
                    node['avg']= math.floor((self.avg_clusters[i]['avg']))
            self.clusters_avg_embedded.append(self.clusters[i])
            i+=1
        self.clusters_avg_embedded.sort(key=lambda x:(x[0]['omega_cluster_index']), reverse=False)
        print "\n after Particle PDA"
        print "first 10 omega cluster:"
        for index in range(10):
            print self.clusters_avg_embedded[index]
        print "\nlast 10 omega cluster:"
        for index in range(len(self.clusters_avg_embedded)-10,len(self.clusters_avg_embedded)):
            print self.clusters_avg_embedded[index]
        return self.clusters_avg_embedded

    def plotResults(self):
        #print self._plotPoints
        x = []
        y = []
        for (generation, fitness) in self._plotPoints:
            x.append(generation)
            y.append(fitness)
#            print "%d" % (fitness)
        pyl.plot(x, y)

        pyl.grid(True)
        pyl.title('Particle PDA')
        pyl.xlabel('Fitness')
        pyl.ylabel('Generation (i)')
        pyl.savefig('particle_pda_plot')

        pyl.show()
