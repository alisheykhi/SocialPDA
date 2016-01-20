import re,snap,collections, operator,os


class ReadGraph():
    extension = []
    G1 = snap.TUNGraph.New()
    stuff = {}
    nodes = []
    edges = []
    sorted_degree_sequence = []

    def __init__(self, file_name):
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

        file_path = "DataSet/"+self.file_name
        ifile = open(file_path,'r')
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
                ReadGraph.G1.AddNode(int(node))
                node_count += 1
            for edge in ReadGraph.edges:
                ReadGraph.G1.AddEdge(int(edge.split(",")[0]) ,int( edge.split(",")[1]))

            sum = 0
            count = 0
            for NI in ReadGraph.G1.Nodes():
                #print "node: %d, out-degree %d, in-degree %d" % ( NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())
                sum += NI.GetInDeg()
                count+=1

            ReadGraph.stuff['edge_count'] = sum/2

            self.degree_sequence()


    def txt_to_graph(self):
        """
        convert txt graph to TNUGraph
        :return:
        """
        file_path = "DataSet/"+self.file_name
        ifile = open(file_path,'r')
        text = ifile.read()
        ifile.close()
        if text:
            print "reading txt file ... "
            nodes_list = []

            if self.file_name.split(".")[0] == 'caida':
                pattern_meas = re.compile(r"^(\d+)\s+(\d+)\s+([-]?\d+)$", re.VERBOSE | re.MULTILINE)
            if self.file_name.split(".")[0] == 'amazon':
                pattern_meas = re.compile(r"^(\d+)\s+(\d+)", re.VERBOSE | re.MULTILINE)
            for match in pattern_meas.finditer(text):
                nodes_list.append("%s" % int(match.group(1)))
                nodes_list.append("%s" % int(match.group(2)))

                ReadGraph.edges.append("%s,%s" % (match.group(1), match.group(2)))

            ReadGraph.nodes = list(set(nodes_list))
            print len (ReadGraph.nodes)

            for node in ReadGraph.nodes:
                ReadGraph.G1.AddNode(int(node))

            for edge in ReadGraph.edges:
                ReadGraph.G1.AddEdge(int(edge.split(",")[0]) ,int( edge.split(",")[1]))
            sum = 0
            count = 0
            for NI in ReadGraph.G1.Nodes():
                #print "node: %d, out-degree %d, in-degree %d" % ( NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())
                sum += NI.GetInDeg()
                count+=1
            ReadGraph.stuff['edge_count'] = sum/2
            self.degree_sequence()


    def degree_sequence(self):
        result_in_degree = snap.TIntV()
        snap.GetDegSeqV(ReadGraph.G1, result_in_degree)

        for i in range(0, result_in_degree.Len()):

            if result_in_degree[i]:
                current_node = {
                    "degree" : result_in_degree[i],
                    "id" : i,
                }
                ReadGraph.sorted_degree_sequence.append(current_node)

        ReadGraph.sorted_degree_sequence.sort(reverse=True)
        ReadGraph.stuff['node_count'] = len(ReadGraph.sorted_degree_sequence)
        ReadGraph.stuff ['max_degree_id'] = ReadGraph.sorted_degree_sequence[0]['id']
        ReadGraph.stuff ['max_degree_size'] = ReadGraph.sorted_degree_sequence[0]['degree']
        ReadGraph.stuff ['avg_degree'] =   (float (ReadGraph.stuff ['edge_count'])/float (ReadGraph.stuff ['node_count']))
        node_occur = collections.Counter (result_in_degree)
        sorted_node_oc = sorted(node_occur.items(), key=operator.itemgetter(1))
        ReadGraph.stuff ['k'] = sorted_node_oc[0][1]
        print ReadGraph.stuff

