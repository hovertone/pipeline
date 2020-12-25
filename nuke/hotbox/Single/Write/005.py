#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Remove files
# COLOR: #ff5555
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

import os
from nukescripts import replaceHashes

node = nuke.selectedNode()
fullpath = node['file'].value()
folder, file = os.path.split(fullpath)
file = replaceHashes(file)
p1 = file[:-8]
p2 = file[-4:]
files = [i for i in os.listdir(folder) if p1 in i and p2 in i]
files.sort()
for f in files:
    #print wave[0]
    #iterWave()
    os.remove(os.path.join(folder, f))


