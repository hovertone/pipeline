#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: 010
#
#----------------------------------------------------------------------------------------------------------

import os
scriptsPath = 'P:/alliance/shots/SH010/comp/scripts/'
lastScene = [i for i in sorted(os.listdir(scriptsPath)) if '~' not in i and 'autosave' not in i][-1]
path = '%s/%s' % (scriptsPath, lastScene)
print path
nuke.scriptOpen(path)