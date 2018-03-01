from graph_util import ReadGraph
from micro_pda import MicroPDA
from particle_pda1 import ParticlePDA
from swarm_pda import SwarmPDA
from Measurments import measurmnets
import time
import datetime
import pymysql
import json

# avg , std , best for 30 times run,
# file name = datasetName_Beta_k_Delta_l

# levels = low, medium, high, and critical



#graph_caida = ReadGraph("caida.txt",6)
# graph_caida = ReadGraph("polblogs.gml",1)
# #graph_caida = ReadGraph("polbooks.gml",level=3)
# optimal_omega_cluster = MicroPDA(graph_caida.sorted_degree_sequence)
# particle_pda = ParticlePDA(omega_clusters=optimal_omega_cluster.omega_clusters,beta= 0.01,
#                            removed_omega_clusters=optimal_omega_cluster.removed_omega_clusters)
# particle_pda.plotResults()
# anonymizedcluster = particle_pda.clusterWithAvg()
# swarm_pda = SwarmPDA(omega_clusters=particle_pda.clusters_avg_embedded,graph_G= graph_caida.G)
# sol = swarm_pda.run_swarm()
# measurment = measurmnets(graph_caida.G, sol['original'], sol['modified'])
# measure = measurment.calculate_measures()


# for key,value in measure.iteritems():
#     print key , '----->' , value

graph_name = 'caida.txt'
level = 6
beta = 0.5
l = 30
run = 30
graph = ReadGraph(graph_name,level)
db = pymysql.connect(host="localhost",
                         user="root",
                         passwd="",
                         db="SocialPda")
connection = db.cursor()

optimal_omega_cluster = MicroPDA(graph.sorted_degree_sequence)
cluster = json.dump(optimal_omega_cluster.omega_clusters)

print cluster

# for i in range(1,run+1):
#     optimal_omega_cluster = MicroPDA(graph.sorted_degree_sequence)
#     cluster = json.dumps(optimal_omega_cluster.omega_clusters)
#     #insert into micropda
#     ts = time.time()
#     timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#
#     sql = "INSERT INTO `SocialPDA`.`micropda` (`dataset`, `Beta`, `l`, `date`, `k`, `delta`, `omega_cluster`, `run`) VALUES (%s,%s,%s,%s,%s,%s,%r,%s)"
#     connection.execute(sql, (graph_name, beta, l, timestamp, '1', '1',cluster , i))
#     connection.commit()
# connection.close()


# particle_pda = ParticlePDA(omega_clusters=optimal_omega_cluster.omega_clusters,beta= beta,
#                                removed_omega_clusters=optimal_omega_cluster.removed_omega_clusters)

#insert into particlepda