
import os
import time


path = r"P:\rnd\sequences\rndA\sh010\fx\grassGeoSeparete"



files = os.listdir(path)

list = []

for f in files:
    list.append(os.path.join(path, f))

list.sort(key=os.path.getmtime)

for i in list:
    print i

# for i in files:
#
#     stats = os.stat(path+ "/" + i)
#     d = time.localtime(stats[8])
#     dd = ".".join([ str(d[2]), str(d[1]), str(d[0]) ])
#     dt = ":".join([ str(d[3]), str(d[4])])
#
#
#
