#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Cleanup Renders
# COLOR: #ff5555
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

import PL_rendersCleanup
reload(PL_rendersCleanup)
if nuke.ask('Sure you want to cleanup renders?'):
    w = PL_rendersCleanup.cleanup_progress_bar()
    w.show()