#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: <img src="P:/alliance2/ShotsTeaser/SH_140/comp/shotIcon/SH_140_shotIcon.jpg"> 140 </img>
#
#----------------------------------------------------------------------------------------------------------

import glob
import os

search_dir = 'P:/alliance2/ShotsTeaser/SH_140/comp/'
files = filter(os.path.isfile, glob.glob(search_dir + "*"))
onlyNKfiles = [i for i in files if '~' not in i and '.autosave' not in i]
onlyNKfiles.sort(key=lambda x: os.path.getmtime(x))
nuke.scriptOpen(onlyNKfiles[-1])