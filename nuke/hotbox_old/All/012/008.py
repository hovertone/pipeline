#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: <img src="P:/vikingsPoker/shots/sh_070/comp/shotIcon/SH_070_shotIcon.jpg"> 070 </img>
#
#----------------------------------------------------------------------------------------------------------

import glob
import os

search_dir = 'P:/vikingsPoker/shots/SH_070/comp/'
files = filter(os.path.isfile, glob.glob(search_dir + "*"))
onlyNKfiles = [i for i in files if '~' not in i and '.autosave' not in i]
onlyNKfiles.sort(key=lambda x: os.path.getmtime(x))
nuke.scriptOpen(onlyNKfiles[-1])