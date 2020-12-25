#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Open Properties
#
#----------------------------------------------------------------------------------------------------------

import nuke
nodes = nuke.selectedNodes()
nuke.toNode('preferences')['maxPanels'].setValue(len(nodes))

for n in nuke.allNodes():
    n.hideControlPanel()
for n in nodes:
    n.showControlPanel()