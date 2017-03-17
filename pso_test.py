
import random





def particle():
    particle = {}
    velocity = []
    pos = []
    pBest = []
    for i in range(0,2):
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

pp = particle()
print pp
print pp ['velocity'][1]