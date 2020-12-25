#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: <img src="P:/alliance2/ShotsTeaser/SH_080/comp/shotIcon/SH_080_shotIcon.jpg"> 080 </img>
#
#----------------------------------------------------------------------------------------------------------

import glob
import os

search_dir = 'P:/alliance2/ShotsTeaser/SH_080/comp/'
files = filter(os.path.isfile, glob.glob(search_dir + "*"))
onlyNKfiles = [i for i in files if '~' not in i and '.autosave' not in i]
onlyNKfiles.sort(key=lambda x: os.path.getmtime(x))
nuke.scriptOpen(onlyNKfiles[-1])