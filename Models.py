

#---- Particle representation
class ParticleModel:
    _position       = None
    _velocity       = None
    _bestPosition   = None
    _nbBestPosition = None
    _fitness        = None

    def __init__(self):
        self._position       = None
        self._velocity       = None
        self._bestPosition   = None
        self._nbBestPosition = None
        self._fitness        = None

#---- Swarm representation
class SwarmModel:
    _particles              = None
    _neighbourhoods         = None
    _bestPosition           = None
    _bestPositionFitness    = None
    
    def __init__(self):
        self._particles = []
        self._neighbourhoods        = None
        self._bestPosition          = None
        self._bestPositionFitness   = None
        

#---- Neighbourhood representation    
class NeighbourhoodModel:
    _particles              = []
    _bestPosition           = None
    _bestPositionFitness    = None
    
    def __init__(self, particles):
        self._particles             = particles
        self._bestPosition          = None
        self._bestPositionFitness   = None


