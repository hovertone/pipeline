#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: daily R&C
# COLOR: #e9ff55
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

import shutil, os, datetime

node = nuke.selectedNode()
if node.Class() != "Write":
    nuke.message('Select a Write node')
else:
    p = node['file'].value()
    isMov = False #flag

    if '.mov' in p and 'P:' in p:
            isMov = True
            pLocal = p.replace('P:', 'D:')
            #print p, '\n', pLocal
            node['file'].setValue(pLocal)

    nuke.execute(node.name(), node.firstFrame(), node.lastFrame())

    if isMov:            
        if not os.path.exists(os.path.split(p)[0]):
            os.makedirs(os.path.split(p)[0])
        
        shutil.copy2(pLocal, p)
        node['file'].setValue(p)