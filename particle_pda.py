
import math, random,sys
import numpy as np
import scipy.spatial as spp

class ParticlePDA():
    differences =[]
    omega_cluster = []
    avg_clusters = []
    beta = 0
    w = 0.729844 # Inertia weight to prevent velocities becoming too large
    c1 = 1.496180 # Scaling co-efficient on the social component
    c2 = 1.496180 # Scaling co-efficient on the cognitive component
    dimension = 0 # Size of the problem
    iterations = 20
    swarmSize = 100
    solution = []
    vmax =6
    globalBest = []

    def __init__(self,omega_clusters,beta):
        print "____________________ParticlePDA____________________________"
        print "-----------------------------------------------------------"
        ParticlePDA.beta = float(beta)
        #ParticlePDA.omega_cluster = omega_clusters
        #print omega_clusters[20]
        ####
        #calculate avg of each omega cluster
        for cluster in omega_clusters:
            avg_info = {}
            sum, avg  = 0 , 0
            for node in cluster:
                sum += int (node['degree'])
            avg = float (sum)/len(cluster)
            if not avg.is_integer():
                ParticlePDA.omega_cluster.append(cluster)
                avg_info['avg'] = avg
                avg_info['omega_cluster_index'] = cluster[0]['omega_cluster_index']
                ParticlePDA.avg_clusters.append(avg_info)
            # floor, ceil = 0,0
            # for node in cluster:
            #     floor += int (math.fabs(int (node['degree']) - math.floor(avg)))
            #     ceil += int ( math.fabs(int (node['degree']) - math.ceil(avg)))
            # ParticlePDA.differences.append((floor,ceil))

        ParticlePDA.dimension = len(ParticlePDA.omega_cluster)
        print "number of particle :",ParticlePDA.dimension

        # print "omega clusters:" , ParticlePDA.omega_cluster
        # print "avg of each omega cluster: ",ParticlePDA.avg_clusters
        # print "length avg_omegacluster:" ,len(ParticlePDA.omega_cluster)
        # print "length avg_omegacluster:" ,len(ParticlePDA.avg_clusters)
        # print ParticlePDA.dimension

        #print self.particel()['velocity']


        # print omega_clusters[0]
        # sum, count, avg ,index = 0 , 0 , 0 ,1
        # for node in omega_clusters[0]:
        #     sum += int (node['degree'])
        #     print node['degree']
        # avg = float (sum)/len(omega_clusters[0])
        # print 'avg : -----> ',avg
        # floor, ceil = 0,0
        # for node in omega_clusters[0]:
        #     floor += int (math.fabs(int (node['degree']) - math.floor(avg)))
        #     ceil += int ( math.fabs(int (node['degree']) - math.ceil(avg)))
        # ParticlePDA.differences.append((floor,ceil))
        # print ParticlePDA.differences

        particleSwarmOptimizer = ParticleSwarmOptimizer()
        particleSwarmOptimizer.initParticle()
        sol = particleSwarmOptimizer.optimize()

        # particle = np.random.randint(2, size = len(ParticlePDA.omega_cluster))
        # sum = particleSwarmOptimizer.f(particle)
        # print particle
        # print sum

        print sol

class ParticleSwarmOptimizer:
    solution = []
    swarm = []

    def __init__(self):
        return

    def initParticle(self):
        for h in range(ParticlePDA.swarmSize):
            self.swarm.append(Particle())
            self.swarm[h].pos = np.random.randint(2, size = ParticlePDA.dimension)
            self.swarm[h].pBest = self.swarm[h].pos
            self.swarm[h].velocity = np.random.ranf(size=ParticlePDA.dimension)
        ParticlePDA.globalBest = np.random.randint(1, size = ParticlePDA.dimension)

    def optimize(self):
        print ParticlePDA.globalBest
        self.solution = ParticlePDA.globalBest
        for i in range(ParticlePDA.iterations): # 0 -> iter-1
            gbest = self.solution
            print gbest , self.f(gbest)
            print "iteration ", i+1 ,"---------------------------"
            for j in range(ParticlePDA.swarmSize):
                pBest = self.swarm[j].pBest
                if self.f(pBest) < self.f(gbest):
                    print "first Global",self.f(gbest)
                    gbest = pBest
                    print "second one",self.f(gbest)
                    print gbest
            self.solution = gbest

            #Update position of each paricle
            for k in range(ParticlePDA.swarmSize):
                self.swarm[k].updateVelocities(self.solution)
                self.swarm[k].updatePositions()
                print self.solution,"sol"


                #self.swarm[k].satisfyConstraints()
            #Update the personal best positions

            for l in range(ParticlePDA.swarmSize):
                if self.f(self.swarm[l].pos) < self.f(self.swarm[l].pBest):
                    self.swarm[l].pBest = self.swarm[l].pos

        return self.solution

    def f(self, particle):
        return ((ParticlePDA.beta * self.f1(particle) )+((1-ParticlePDA.beta) * self.f2(particle)))

    def f2(self,particle):
        sumarray =[]
        i = 0
        for x in particle:
            diff =0
            for node in ParticlePDA.omega_cluster[i]:
                if x:
                    diff += node['degree'] - math.ceil((ParticlePDA.avg_clusters[i]['avg']))
                else:
                    diff += node['degree'] - math.floor((ParticlePDA.avg_clusters[i]['avg']))
            i += 1
            sumarray.append(diff)
        return math.fabs(sum(sumarray))

    def f1(self,particle):
        sumarray =[]
        i = 0
        for x in particle:
            diff =0
            for node in ParticlePDA.omega_cluster[i]:
                if x:
                    diff += math.fabs(node['degree'] - math.ceil((ParticlePDA.avg_clusters[i]['avg'])))
                else:
                    diff +=math.fabs(node['degree'] - math.floor((ParticlePDA.avg_clusters[i]['avg'])))
            i += 1
            sumarray.append(diff)
        return (sum(sumarray))
    # This class contains the particle swarm optimization algorithm

class Particle:
    pos = []
    velocity =[]
    pBest = []
    def __init__(self):
        # self.pos = np.random.randint(2, size = ParticlePDA.dimension)
        # self.velocity = np.random.ranf(size=ParticlePDA.dimension)
        pass
    def updatePositions(self):
        for i in range(ParticlePDA.dimension):
            if np.random.rand(1) < self.sigmoid(self.velocity[i]):
                self.pos[i] = 0
            else:
                self.pos[i] = 1
        return

    def updateVelocities(self, gBest):

        for i in range(ParticlePDA.dimension):
            r1 = random.random()
            r2 = random.random()
            social = float(ParticlePDA.c1 * r1 * (gBest[i] - self.pos[i]))
            cognitive = float(ParticlePDA.c2 * r2 * (self.pBest[i] - self.pos[i]))
            velocity = social + cognitive
            if abs(velocity) > ParticlePDA.vmax and abs(velocity) is velocity:
                velocity = ParticlePDA.vmax
            elif abs(velocity) > ParticlePDA.vmax:
                velocity = -ParticlePDA.vmax
            self.velocity[i] =  velocity #+ (ParticlePDA.w * self.velocity[i])
        return

    def sigmoid (self, x):
        return 1 / (1+ math.exp(-x))

    def satisfyConstraints(self):
        #This is where constraints are satisfied
        return