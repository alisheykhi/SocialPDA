
from numpy.random import zipf
from math import ceil

privacy_level = []
a=1.47
s = zipf(a, 50000)
zipf_dis = (s/float(max(s)))*5

privacy_level = [x for x in zipf_dis]
privacy_level.sort()
privacy_level.reverse()
for item in privacy_level:
    print int(ceil(item))
print len(privacy_level)