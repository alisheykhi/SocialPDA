
import math, random,sys
import numpy as np
import scipy.spatial as spp
from Models import *
from Controllers import *
import pylab as pyl

class ParticlePDA():
    differences =[]
    omega_cluster = []
    avg_clusters = []
    beta = 0
    _plotPoints = []

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
            if not avg.is_integer():
                self.omega_cluster.append(cluster)
                avg_info['avg'] = avg
                avg_info['omega_cluster_index'] = cluster[0]['omega_cluster_index']
                self.avg_clusters.append(avg_info)


        self._popSize = popSize = 500
        self._dimensions = dimensions  = len(ParticlePDA.omega_cluster)
        self._generations = generations = 100
        print "number of particle :",dimensions
        swarm   = SwarmModel()
        sc      = SwarmController("binary",self.beta,self.omega_cluster,self.avg_clusters)
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

    def plotResults(self):
        print self._plotPoints
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
