#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: RENDER SELECTED
#
#----------------------------------------------------------------------------------------------------------

import nuke
for n in nuke.selectedNodes('Write'):
        nuke.execute(n.name(), n.firstFrame(), n.lastFrame())
        print '%s HAS BEED RENDERED' % n.name()