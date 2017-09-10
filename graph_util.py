import re,collections,operator
import networkx as nx
from privacy_level import privacy_level_generator
from numpy.random import zipf
from math import ceil

class ReadGraph():
    extension = []
    G = nx.Graph()
    properties  = {}
    nodes = []
    edges = []
    privacy_level = []
    sorted_degree_sequence = []

    def __init__(self, file_name):
        print "-----------------------------------------------------------"
        print "___________________Developed for___________________________"
        print "-----------------------------------------------------------"
        print "title: SocialPDA: A Structure-Aware Approach for Personalized Degree Anonymity in Social Network Graphs"
        print "Author: Ali Sheykhi and Mahdi Abadi"
        print "Faculty of Electrical and Computer Engineering, Tarbiat Modares University, Tehran, Iran"
        print "{ali.sheykhi, abadi}@modares.ac.ir"
        print "-----------------------------------------------------------"
        print "___________________Initial Setup___________________________"
        print "-----------------------------------------------------------"
        self.file_name = file_name
        print "file name : ",self.file_name
        ReadGraph.extension = ["csv", "txt", "gml", "net"]
        self.converter()



    def converter(self):
        '''
        chose correct converter
        :return:
        '''
        file_type = self.file_type()

        if file_type == "gml":
            print "Convert gml file ... "
            self.gml_to_graph()
        if file_type == "txt":
            print "Convert txt file ... "
            self.txt_to_graph()


    def file_type(self):
        '''
        return dataSet file type
        :return: file name
        '''
        if self.is_valid():
            return  self.file_name.split(".")[-1]


    def is_valid(self):
        '''
        check for valid graph type
        :return:
        '''
        file_extension = self.file_name.split(".")[-1]
        if (file_extension):
            if (file_extension.lower() in ReadGraph.extension):
                return True
            else:
                print "Unknown file extension \"",file_extension,"\", use:",ReadGraph.extension
                return False
        else:
            print "file does not have an extension!"
            return False


    def gml_to_graph(self):
        '''
        convert gml graph to TUNGraph
        :return:
        '''
        # try:
        #     file_path = "DataSet/"+self.file_name
        # except:
        #     print "can't open "+self.file_name
        # else:
        #     print "reading gml file ... "
        #     M = nx.MultiGraph(nx.read_gml('DataSet/polblogs.gml'))
        #     for u,v,data in M.edges_iter(data=True):
        #         if ReadGraph.G.has_edge(u,v):
        #             pass
        #         else:
        #             ReadGraph.G.add_edge(u, v)
        #     ReadGraph.properties ['edge_count'] = len(ReadGraph.edges)
        #     print len(ReadGraph.G.node)
        #     self.degree_sequence()
        try:
            file_path = "DataSet/"+self.file_name
            ifile = open(file_path,'r')
        except:
            print "can't open "+self.file_name
        else:
            text = ifile.read()
            ifile.close()
            if text:
                print "reading gml file ... "
                pattern_meas = re.compile(r"source\s(\d+)\s+target\s(\d+)", re.VERBOSE | re.MULTILINE)
                pattern_id = re.compile(r"id\s(\d+)", re.VERBOSE | re.MULTILINE)
                for match in pattern_meas.finditer(text):
                    ReadGraph.edges.append("%s,%s" % (match.group(1), match.group(2)))
                for match in pattern_id.finditer(text):
                    ReadGraph.nodes.append("%s" % match.group(1))
                node_count = 0
                for node in ReadGraph.nodes:
                    ReadGraph.G.add_node(int(node))
                    node_count += 1
                for edge in ReadGraph.edges:
                    ReadGraph.G.add_edge(int(edge.split(",")[0]) ,int( edge.split(",")[1]))
                sum = 0
                count = 0
                for NI in ReadGraph.G.degree().values():
                    #print "node: %d, out-degree %d, in-degree %d" % ( NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())
                    sum += NI
                    count+=1
                ReadGraph.properties ['edge_count'] = sum/2
                self.degree_sequence()


    def txt_to_graph(self):
        """
        convert txt graph to TNUGraph
        :return:
        """

        try:
            file_path = "DataSet/"+self.file_name
            ifile = open(file_path ,'r')
        except:
            print "can't open "+self.file_name
        else:

            text = ifile.read()
            ifile.close()
            if text:
                print "reading txt file ... "
                nodes_list = []

                if self.file_name.split(".")[0] == 'caida':
                    pattern_meas = re.compile(r"^(\d+)\s+(\d+)\s+([-]?\d+)$", re.VERBOSE | re.MULTILINE)
                if self.file_name.split(".")[0] == 'caida_test':
                    pattern_meas = re.compile(r"^(\d+)\s+(\d+)\s+([-]?\d+)$", re.VERBOSE | re.MULTILINE)
                if self.file_name.split(".")[0] == 'amazon':
                    pattern_meas = re.compile(r"^(\d+)\s+(\d+)", re.VERBOSE | re.MULTILINE)
                for match in pattern_meas.finditer(text):
                    # nodes_list.append("%s" % int(match.group(1)))
                    # nodes_list.append("%s" % int(match.group(2)))
                    ReadGraph.G.add_edge(int(match.group(1)),int( match.group(2)))

                # ReadGraph.nodes = list(set(nodes_list))
                # for node in ReadGraph.nodes:
                #     ReadGraph.G.add_node(int(node))
                # for edge in ReadGraph.edges:
                #     ReadGraph.G.add_edge(int(edge.split(",")[0]) ,int( edge.split(",")[1]))


                sum = 0
                count = 0
                for NI in ReadGraph.G.degree().values():
                    #print "node: %d, out-degree %d, in-degree %d" % ( NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())
                    sum += NI
                    count+=1
                ReadGraph.properties ['edge_count'] = sum/2

                self.degree_sequence()

    def degree_sequence(self):
        print nx.info(ReadGraph.G)
        result_in_degree = ReadGraph.G.degree().values()
        privacy_file_name = self.file_name.split(".")[0]+"_privacy.txt"
        privacy_level = privacy_level_generator(file_name=privacy_file_name)
        for node in ReadGraph.G.nodes():
            if ReadGraph.G.degree(node):
                current_node = dict(degree = ReadGraph.G.degree(node), id=node)
                ReadGraph.sorted_degree_sequence.append(current_node)
        ReadGraph.sorted_degree_sequence.sort(key=lambda x:(x['degree']), reverse=True)

        # for i in range (0,5):
        #     print ReadGraph.sorted_degree_sequence[i]
        for i in range(0, len(ReadGraph.sorted_degree_sequence)):
            if ReadGraph.sorted_degree_sequence[i]:
                ReadGraph.sorted_degree_sequence[i]['privacy_level'] = int(privacy_level[i])*2
        #ReadGraph.sorted_degree_sequence.sort(key=lambda x:(x['privacy_level'],x['degree']), reverse=True)
        ReadGraph.properties['node_count'] = len(ReadGraph.sorted_degree_sequence)
        max_degree = None
        max_degree_id = None
        for node in ReadGraph.sorted_degree_sequence:
            if node['degree'] > max_degree:
                max_degree = node['degree']
                max_degree_id = node['id']

        ReadGraph.properties  ['max_degree_id'] = max_degree_id
        ReadGraph.properties  ['max_privacy'] = ReadGraph.sorted_degree_sequence[0]['privacy_level']
        ReadGraph.properties  ['max_privacy_id'] = ReadGraph.sorted_degree_sequence[0]['id']
        ReadGraph.properties  ['max_degree_size'] = max_degree
        ReadGraph.properties  ['avg_degree'] =  2 * (float (ReadGraph.properties  ['edge_count'])/float (ReadGraph.properties  ['node_count']))
        node_occur = collections.Counter (result_in_degree)
        sorted_node_oc = sorted(node_occur.items(), key=operator.itemgetter(1))
        ReadGraph.properties  ['k'] = sorted_node_oc[0][1]
        print ReadGraph.properties 
        print "for example, the first node in sorted degree sequence is :" + str(ReadGraph.sorted_degree_sequence[0])






