from graph_util import ReadGraph
from micro_pda import MicroPDA
from particle_pda import ParticlePDA


#graph_blogs = ReadGraph("polblogs.gml")
#graph_books = ReadGraph("polbooks.gml")
graph_caida = ReadGraph("caida.txt")
optimal_omega_cluster = MicroPDA(graph_caida.sorted_degree_sequence)
#particle_pda = ParticlePDA(omega_clusters=optimal_omega_cluster.omega_clusters,beta= 0.5)