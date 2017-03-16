
import math, random,sys

class ParticlePDA():
    differences =[]
    beta = 0
    w = 0.729844 # Inertia weight to prevent velocities becoming too large
    c1 = 1.496180 # Scaling co-efficient on the social component
    c2 = 1.496180 # Scaling co-efficient on the cognitive component
    dimension = 0 # Size of the problem
    iterations = 20
    swarmSize = 10
    solution = []

    def __init__(self,omega_clusters,beta):
        print "____________________ParticlePDA____________________________"
        print "-----------------------------------------------------------"
        ParticlePDA.beta = float(beta)
        for cluster in omega_clusters:
            sum, count, avg ,index = 0 , 0 , 0 ,1
            for node in cluster:
                sum += int (node['degree'])
                count +=1
            avg = float (sum)/count
            floor, ceil = 0,0
            for node in cluster:
                floor += int (math.fabs(int (node['degree']) - math.floor(avg)))
                ceil += int ( math.fabs(int (node['degree']) - math.ceil(avg)))
            ParticlePDA.differences.append((floor,ceil))
        ParticlePDA.dimension = len(ParticlePDA.differences)
        print self.particel()['velocity']
        #particleSwarmOptimizer = ParticleSwarmOptimizer(ParticlePDA.changes_list)
        #particleSwarmOptimizer.optimize()
        #print particleSwarmOptimizer.solution

    def particel (self):
        particle = {}
        velocity = []
        pos = []
        pBest = []
        for i in range(0,ParticlePDA.dimension):
            '''
            if (math.fabs(deff[i][0]) < math.fabs (deff[i][1])):
                self.pos.append(0)
            if (math.fabs(deff[i][0]) > math.fabs (deff[i][1])):
                self.pos.append(1)
            if (math.fabs(deff[i][0]) == math.fabs (deff[i][1])):
                self.pos.append(random.randrange(0,2))
            '''
            pos.append(random.randrange(0,2))
            velocity.append(0.01 * random.random())
            pBest.append(pos[i])
            particle ['velocity'] = velocity
            particle ['pos'] = pos
            particle ['pBest'] = pBest
        return particle

    def bpso (self):
        pass
