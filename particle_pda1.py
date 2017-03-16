import math, random,sys



# chera globalbest injure ??? Debug she har iter yadehs mire !


class ParticlePDA():
    changes_list =[]
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
            ParticlePDA.changes_list.append((floor,ceil))
        ParticlePDA.dimension = len(ParticlePDA.changes_list)
        particleSwarmOptimizer = ParticleSwarmOptimizer(ParticlePDA.changes_list)
        particleSwarmOptimizer.optimize()
        print particleSwarmOptimizer.solution

class ParticleSwarmOptimizer:
    solution = []
    swarm = []
    globalBest = []

    def __init__(self,deff):
        for h in range(ParticlePDA.swarmSize):
            self.swarm.append(Particle(deff))
        return

    def optimize(self):
        self.globalBest = self.swarm[0].pos
        for i in range(ParticlePDA.iterations):
            gBest = self.globalBest
            print "iteration ", i+1 ,"="
            for j in range(ParticlePDA.swarmSize):
                gBest = self.globalBest
                pBest = self.swarm[j].pBest
                if self.f(pBest) < self.f(gBest):
                    gBest = pBest
                    self.globalBest = gBest
                    print self.f(gBest)
            self.solution = gBest
            #Update position of each paricle
            for k in range(ParticlePDA.swarmSize):
                self.swarm[k].updateVelocities(gBest)
                self.swarm[k].updatePositions()
                #self.swarm[k].satisfyConstraints()
            #Update the personal best positions
            for l in range(ParticlePDA.swarmSize):
                pBest = self.swarm[l].pBest
                if self.f(self.swarm[l].pos) < self.f(pBest):
                    self.swarm[l].pBest = self.swarm[l].pos
        return self.solution

    def f(self, particle):
        return ((ParticlePDA.beta * self.f1(particle) )+((1-ParticlePDA.beta) * self.f2(particle)))

    def f2(self,particle):

        i = 0
        sum = 0
        for x in particle:
            sum += math.fabs(ParticlePDA.changes_list[i][x])
            i += 1
        #print (sum)
        return sum

    def f1(self,particle):
        i = 0
        sum = 0
        for x in particle:
            sum += ParticlePDA.changes_list[i][x]
            i += 1
        #print sum
        return sum
    # This class contains the particle swarm optimization algorithm
class Particle:


    def __init__(self,deff):
        self.velocity = []
        self.pos = []
        self.pBest = []
        for i in range(0,ParticlePDA.dimension):
            '''
            if (math.fabs(deff[i][0]) < math.fabs (deff[i][1])):
                self.pos.append(0)
            if (math.fabs(deff[i][0]) > math.fabs (deff[i][1])):
                self.pos.append(1)
            if (math.fabs(deff[i][0]) == math.fabs (deff[i][1])):
                self.pos.append(random.randrange(0,2))
            '''
            self.pos.append(random.randrange(0,2))
            self.velocity.append(0.01 * random.random())
            self.pBest.append(self.pos[i])
        return

    def updatePositions(self):
        for i in range(ParticlePDA.dimension):
            if (random.random() >= self.sigmoid(self.velocity[i]) ):
                self.pos[i] = 0
            else:
                self.pos[i] = 1
        return

    def updateVelocities(self, gBest):
        for i in range(ParticlePDA.dimension):
            r1 = random.random()
            r2 = random.random()
            social = ParticlePDA.c1 * r1 * (gBest[i] - self.pos[i])
            cognitive = ParticlePDA.c2 * r2 * (self.pBest[i] - self.pos[i])
            self.velocity[i] =  social + cognitive #+ (ParticlePDA.w * self.velocity[i])
        return

    def sigmoid (self, x):
        return 1 / (1+ math.exp(-x))

    def satisfyConstraints(self):
        #This is where constraints are satisfied
        return
