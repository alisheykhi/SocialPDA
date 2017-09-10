from graph_util import ReadGraph
from micro_pda import MicroPDA
from particle_pda1 import ParticlePDA
from swarm_pda import SwarmPDA
from Measurments import measurmnets

#graph_caida = ReadGraph("caida.txt")
#graph_caida = ReadGraph("polblogs.gml")
graph_caida = ReadGraph("polbooks.gml")
optimal_omega_cluster = MicroPDA(graph_caida.sorted_degree_sequence)
particle_pda = ParticlePDA(omega_clusters=optimal_omega_cluster.omega_clusters,beta= 0.99,
                           removed_omega_clusters=optimal_omega_cluster.removed_omega_clusters)
#particle_pda.plotResults()
anonymizedcluster = particle_pda.clusterWithAvg()
swarm_pda = SwarmPDA(omega_clusters=particle_pda.clusters_avg_embedded,graph_G= graph_caida.G)
sol = swarm_pda.run_swarm()
measurment = measurmnets(graph_caida.G, sol['original'], sol['modified'])
measure = measurment.calculate_measures()
print measure


