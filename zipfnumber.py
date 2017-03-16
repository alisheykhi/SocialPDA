import re,math
from operator import itemgetter
from numpy.random import zipf

frequency = {}
file_name = 'caida.txt'

try:
    file_path = "DataSet/"+file_name
    ifile = open(file_path ,'r')
except:
    print "can't open "+file_name
else:

    text = ifile.read()
    ifile.close()
    if text:
        print "zipf ... "
        nodes_list = []

        if file_name.split(".")[0] == 'caida':
            pattern_meas = re.compile(r"^(\d+)\s+(\d+)\s+([-]?\d+)$", re.VERBOSE | re.MULTILINE)
        if file_name.split(".")[0] == 'amazon':
            pattern_meas = re.compile(r"^(\d+)\s+(\d+)", re.VERBOSE | re.MULTILINE)
        for match in pattern_meas.finditer(text):
            nodes_list.append("%s" % int(match.group(1)))
            nodes_list.append("%s" % int(match.group(2)))

for node in nodes_list:
    count = frequency.get(node,0)
    frequency[node] = count + 1
node_ocurr = []
s = []
for key, value in reversed(sorted(frequency.items(), key = itemgetter(1))):
     node_ocurr.append([key,value/2])
     s.append(zipf(2.,value/2))


a=2
s = zipf(a, 10)

result = (s/float(max(s)))*5

for i in result:
    print (result[i])
    print s[i]
    print '------'

print min(s), max(s)
print min(result),max(result)
