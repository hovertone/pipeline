#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: # DTCH FTG #
# COLOR: #823000
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

import nuke

nodes = nuke.selectedNodes('Read')
if nodes == []: 
    nuke.message('There is no read node selected')
else:
    for n in nodes:
        n['file'].setValue(n['file'].value().replace('[file dirname [value root.name]]', os.path.dirname(nuke.root().name())))
    print '!! SUCCESS !!'