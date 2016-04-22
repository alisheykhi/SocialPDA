import math, random

class ParticlePDA():
    changes_list =[]
    beta = 0


    def __init__(self,omega_clusters,beta):
        print "____________________ParticlePDA____________________________"
        print "-----------------------------------------------------------"
        ParticlePDA.beta = float(beta)
        for cluster in omega_clusters:
            sum, count, avg ,index = 0 , 0 , 0 ,1
            for node in cluster:
                sum += node['degree']
                count +=1
            avg = float (sum)/count
            ParticlePDA.changes_list.append((int (math.floor(avg) * count)-sum ,int (math.ceil(avg) * count)-sum ))
        particle = [random.randrange(0, 2) for _ in range(0, len(omega_clusters))]
        print (self.f3(particle))

    def f3(self,particle):
        return ((ParticlePDA.beta * self.f1(particle) )+((1-ParticlePDA.beta) * self.f2(particle)))

    def f2(self,particle):
        i = 0
        sum = 0
        for x in particle:
            sum += math.fabs(ParticlePDA.changes_list[i][x])
            i += 1
        print (sum)
        return sum

    def f1(self,particle):
        i = 0
        sum = 0
        for x in particle:
            sum += ParticlePDA.changes_list[i][x]
            i += 1
        print sum
        return sum


