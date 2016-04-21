
import snap


from graph_util import ReadGraph
from micro_pda import MicroPDA

#graph_blogs = ReadGraph("polblogs.gml")
#graph_books = ReadGraph("polbooks.gml")
graph_caida = ReadGraph("caida.txt")
optimal_omega_cluster = MicroPDA(graph_caida.sorted_degree_sequence)



#graph_amazoon = ReadGraph("amazon.txt")







