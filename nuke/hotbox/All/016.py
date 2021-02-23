#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Cleanup Renders&Precomps
# COLOR: #ff5555
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

import PL_rendersCleanup
reload(PL_rendersCleanup)
if nuke.ask('Sure you want to cleanup renders and precomps?'):
    w = PL_rendersCleanup.cleanup_progress_bar(remove_precomps=True)
    w.show()