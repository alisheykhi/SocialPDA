#===============================================================================
# @author: Daniel V. Stankevich
# @organization: RMIT, School of Computer Science, 2012
#
#
# This package contains all PSO controllers
#===============================================================================


import numpy as np
import scipy.spatial as spp
from Models import NeighbourhoodModel
from Models import ParticleModel
import math

class BinaryParticleController:
    
    _beta = None
    _cluster = None
    _avg_cluster = None
    
    def __init__(self, beta, cluster, avg_cluster):
        self._beta = beta
        self._cluster = cluster
        self._avg_cluster = avg_cluster

    def initParticle(self, model, dimensions):
        # Create position array
        model._position = np.random.randint(2, size = dimensions)
        # Create Velocity array
        model._velocity = np.random.randint(2, size = dimensions)
        # Save best Position so far as current Position
        model._bestPosition = model._position
        self.updateFitness(model)

    def updateFitness(self, model):
        # Get Differences of vector
        hdist = self.f(model._position)
        # Save it as best position if its better than previous best
        if hdist < model._fitness or model._fitness is None:
            model._bestPosition = np.copy(model._position)
            model._fitness = hdist

    def f(self, particle):
        return ((self._beta * self.f1(particle) )+((1-self._beta) * self.f2(particle)))

    def f2(self,particle):
        sumarray =[]
        i = 0
        for x in particle:
            diff =0
            for node in self._cluster[i]:
                if x:
                    diff += node['degree'] - math.ceil((self._avg_cluster[i]['avg']))
                else:
                    diff += node['degree'] - math.floor((self._avg_cluster[i]['avg']))
            i += 1
            sumarray.append(diff)
        return math.fabs(sum(sumarray))

    def f1(self,particle):
        sumarray =[]
        i = 0
        for x in particle:
            diff =0
            for node in self._cluster[i]:
                if x:
                    diff += math.fabs(node['degree'] - math.ceil((self._avg_cluster[i]['avg'])))
                else:
                    diff +=math.fabs(node['degree'] - math.floor((self._avg_cluster[i]['avg'])))
            i += 1
            sumarray.append(diff)
        return (sum(sumarray))
    # This class contains the particle swarm optimization algorithm

    def updatePosition(self, model):
        # VELOCITY NEEDS TO BE CONSTRICTED WITH VMAX
        # Get random coefficients e1 & e2
        c = 2.5
        e1 = np.random.rand()
        e2 = np.random.rand()
        vmax = 6
        # Apply equation to each component of the velocity, add it to corresponding position component
        for i, velocity in enumerate(model._velocity):
#            velocity = 0.72984 * (velocity + c * e1 * (model._bestPosition[i] - model._position[i]) + c * e2 * (model._nbBestPosition[i] - model._position[i]))
            velocity = velocity + c * e1 * (model._bestPosition[i] - model._position[i]) + c * e2 * (model._nbBestPosition[i] - model._position[i])
            if abs(velocity) > vmax and abs(velocity) is velocity: 
                velocity = vmax
            elif abs(velocity) > vmax:
                velocity = -vmax
            velocity = self.sigmoid(velocity)
#            print "vel:", velocity
            if np.random.rand(1) < velocity:
                model._position[i] = 1
            else:
                model._position[i] = 0
            
    def sigmoid(self, x):
        return 1.0/(1.0 + np.exp(-(x)))


class SwarmController:    

    _particleController = None
    _neighbourhoodController = None
    
    def __init__(self, type, beta, cluster, avg_cluster):
        # Initialize ParticleController
        if type is "binary":
            self._particleController = BinaryParticleController(beta, cluster, avg_cluster)
        # Initialize NeighbourhoodController
        self._neighbourhoodController = NeighbourhoodController()
    
    def initSwarm(self, swarm, topology = "gbest" , nParticles = 1, dimensions = 1):
        # Create Swarm
        for i in range(nParticles):
            newParticle = ParticleModel()
            self._particleController.initParticle(newParticle, dimensions)
            swarm._particles.append(newParticle)    
        swarm._neighbourhoods = self._neighbourhoodController.initNeighbourhoods(swarm, 'gbest')
        self.updateSwarmBestPosition(swarm)
            

    def updateSwarmBestPosition(self, swarm):
        # Find swarm best position and save it in swarm
        for nb in swarm._neighbourhoods:
            self._neighbourhoodController.updateNeighbourhoodBestPosition(nb)
            if swarm._bestPositionFitness is None or nb._bestPositionFitness < swarm._bestPositionFitness:
                swarm._bestPositionFitness = nb._bestPositionFitness
                swarm._bestPosition =  np.copy(nb._bestPosition)
    
    # Update all particles in the swarm 
    def updateSwarm(self, swarm):
        for curParticle in swarm._particles:
            self._particleController.updatePosition(curParticle)
            self._particleController.updateFitness(curParticle)
        self.updateSwarmBestPosition(swarm)
        
        
#===============================================================================
# Neighborhood Controller
#===============================================================================
class NeighbourhoodController:    

    def initNeighbourhoods(self, swarm, topology = "gbest"):
        if topology is "gbest":
            return [NeighbourhoodModel(swarm._particles)]
        elif topology is "lbest":
            neighbourhoods = []
            for idx, curParticle in enumerate(swarm._particles):
                previousParticle = None
                nextParticle = None
                if idx is 0:
                    # Previous is last, next is next
                    nextParticle = swarm._particles[idx + 1]
                    previousParticle = swarm._particles[len(swarm._particles) - 1]
                elif idx is len(swarm._particles) - 1:
                    # Previous is previous, next is first
                    nextParticle = swarm._particles[0]
                    previousParticle = swarm._particles[idx - 1]
                else:
                    # Previous is previous, next is next
                    nextParticle = swarm._particles[idx + 1]
                    previousParticle = swarm._particles[idx - 1]
                neighbourhoods.append(NeighbourhoodModel([previousParticle, curParticle, nextParticle]))
            return neighbourhoods

    def updateNeighbourhoodBestPosition(self, model):
        # Find the best one in the NB
        for curParticle in model._particles:
            if model._bestPositionFitness is None or (curParticle._fitness < model._bestPositionFitness and curParticle._fitness is not None):
                model._bestPositionFitness = curParticle._fitness
                model._bestPosition = np.copy(curParticle._bestPosition)

        # Save nb best position in particles nbBestPosition 
        for curParticle in model._particles:
            curParticle._nbBestPosition = np.copy(model._bestPosition)
