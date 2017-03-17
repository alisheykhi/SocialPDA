
import re



def privacy_level_generator (file_name):
    level=[]
    try:
        file_path = "DataSet/"+file_name
        ifile = open( file_path ,'r' )
        text = ifile.read()
        ifile.close()

    except:
        print "can't open privacy file :("
    else:
        pattern = re.compile(r"(\d+)\s+", re.VERBOSE | re.MULTILINE)
        for match in pattern.finditer(text):
            level.append("%s" % (match.group(1)) )

    level.sort()
    level.reverse()
    for i in range (0,10):
            print level[i]
    return level