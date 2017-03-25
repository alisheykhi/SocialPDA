# Created by Adam Maus (http://a-ma.us)
# Last updated 2012-01-24
import random
import math
import sys

# The dimension of the function
num_dimensions = 2
# The number of particles in the swarm
num_particles = 2

# Bounds on the positions and velocities
v_max = 20
v_min = -20
p_min = -32
p_max = 32
# The number of updates to do
cmax = 1000
# The amount to dampen the velocity by each update
dampener = 1
dampen_rate = 1

# Leave the orig_* variables alone
orig_dampen_rate = dampen_rate
orig_dampener = dampener
#

# Function we are attempting to optimize (minimize)
def F(x):
  global num_dimensions
  D = num_dimensions
  summation = 0

  # D-dimensional Rastrigin Function
  # http://en.wikipedia.org/wiki/Rastrigin_function
  # Global Min: f(0,0,...,0) = 0
  # Position Min: -5.12; Position Max: 5.12
  i = 0
  summation = D*10
  while i < D:
    summation += x[i]**2 - 10 * math.cos(2 * math.pi * x[i])
    i = i + 1
  return summation

# The main function that constructs the swarm and attempts to optimize F
def main():
  global cmax, dampener, dampen_rate, num_dimensions
  # You could wrap the rest of the function in a while loop
  # to do more than one iteration
  dampen_rate = orig_dampen_rate
  dampener = orig_dampener
  # Construct the swarm
  swarm = []
  i = 0
  while i < num_particles:
    swarm.append(Particle())
    i = i + 1

  # Initialize the best position, velocity, error
  best_pos = []
  best_velocity = []
  best_err = -1
  # Run <cmax> updates to the swarm and output the best position / error
  i = 0
  while i <= cmax:
    # Iterate the swarm and evaluate their position on the function
    j = 0
    while j < len(swarm):
      err = swarm[j].Evaluate()
      # If this particle is performing better than the rest
      # Save its positionvelocity, and error
      if err < best_err or best_err == -1:
        best_pos = []
        best_velocity = []
        k = 0
        while k < num_dimensions:
          best_pos.append(swarm[j].pos[len(swarm[j].pos)-1][k])
          best_velocity.append(swarm[j].velocity[len(swarm[j].velocity)-1][k])
          k = k + 1
        best_err = err
      j = j + 1

    # Update the swarm based on the new positions
    j = 0
    while j < len(swarm):
      swarm[j].UpdateVelocity(best_pos)
      swarm[j].UpdatePosition()
      j = j + 1

    dampener = dampener * dampen_rate # Dampen the velocity
    i = i + 1
  # Output Statistics
  print "Best Error: ", best_err
  print "Best Position: ", best_pos

# Each particle is an object with the following attributes:
# This is for a minimization problem so we are looking for smaller errors
#   err: the error of the position that the particle holds right now
#   best_pos: the location of the lowest error the particle has seen
#   best_err: the error of the best performing location (lowest error)
#   pos: an array of positions the particle has seen (you could recycle old positions)
#   velocity: an array of velocities that the particle has had
class Particle:
  def __init__(self):
    global num_dimensions
    # this function sets up each particle
    # we can initialize the position and velocity of the particles
    # using the InitPosition() and InitVelocity() functions
    self.err = 0
    self.best_pos = []
    self.best_err = -1 # this is set to -1 so we update after the first step
    self.pos = []
    self.velocity = []

    # Since we are operating in a potentially multi-dimensional space
    # we have to run through each of the positions, initializing the
    # positions and velocities for each dimension
    temp_pos = []
    temp_velocity = []
    j = 0
    while j < num_dimensions:
      temp_pos.append(self.InitPosition())
      temp_velocity.append(self.InitVelocity())
      self.best_pos.append(0) # initialize the best position array
      j = j + 1
    self.pos.append(temp_pos)
    self.velocity.append(temp_velocity)

  # Evaluate the performance of each particle
  # The current position of the particle is the last
  # array in the position array.
  def Evaluate(self):
    global num_dimensions
    # The function F is the function we are trying to optimize (minimize)
    self.err = F(self.pos[len(self.pos)-1])
    if self.best_err == -1 or self.err < self.best_err:
      self.first_update = False
      self.best_err = self.err
      self.best_pos = []
      j = 0
      while j < num_dimensions:
        self.best_pos.append(self.pos[len(self.pos)-1][j])
        j = j + 1
    return self.err
  # Initialize the position of the particle between -30 and 30
  # for each dimension
  def InitPosition(self):
    temp = 30*random.random()
    if random.random() > 0.5:
      temp = -1 * temp
    if temp > p_max:
      return p_max
    elif temp < p_min:
      return p_min
    return temp

  # Initialize the velocity of the particle between 1 and -1
  # for each dimension
  def InitVelocity(self):
    if random.random() > 0.5:
      return random.random()
    return -1*random.random()

  # A function that is used to randomize the cognitive term
  def RandomizeCognitive(self):
    return random.random()

  # A function that is used to randomize the social term
  def RandomizeSocial(self):
    return random.random()

  # A function that is used to update the velocity
  # of the particle the particle's past and the global best position seen
  def UpdateVelocity(self, global_best_pos):
    global v_max, dampener, num_dimensions
    # w is a control parameter that tells the particle
    # how much to discount the previous velocity
    w = 1
    # c1 is a control parameter that tells the particle
    # how much to weight its own previous positions
    c1 = 2
    # c2 is a control parameter that tells the particle
    # how much to weight the swarms best best position
    c2 = 2
    # r1 and r2 are random numbers that weight the
    # cognitive and social terms
    r1 = self.RandomizeCognitive()
    r2 = self.RandomizeSocial()

    t = len(self.velocity)

    # Construct the new velocity for the particle
    new_velocity_arr = []
    j = 0
    while j < num_dimensions:
      # Apply the control parameters to the particle's previous velocity
      # in the direction that we are working on
      v_term = dampener*w*self.velocity[t-1][j]

      # Create the cognitive and social terms
      own_term = c1 * r1 * (self.best_pos[j] - self.pos[t-1][j])
      social_term = c2 * r2 * (global_best_pos[j] - self.pos[t-1][j])
      # Add the velocities together to make the new velocity
      new_velocity = v_term + own_term + social_term

      # If the velocity is larger than the max velocity, decrease it
      # If the velocity is smaller than the min velocity, increase it
      if new_velocity > v_max:
        new_velocity = v_max
      elif new_velocity < v_min:
        new_velocity = v_min
      new_velocity_arr.append(new_velocity)
      j = j + 1

    self.velocity.append(new_velocity_arr)

  # Update the particle's position based on its previous velocity and position
  def UpdatePosition(self):
    global p_max, p_min, num_dimensions
    t1 = len(self.velocity)
    t2 = len(self.pos)

    new_position_arr = []

    j = 0
    while j < num_dimensions:
      new_position = self.pos[t2-1][j] + self.velocity[t1-1][j]
      # If the position is smaller or larger than the bounds, change them
      if new_position > p_max:
        new_position = p_max
      elif new_position < p_min:
        new_position = p_min
      new_position_arr.append(new_position)
      j = j + 1
    self.pos.append(new_position_arr)

main()