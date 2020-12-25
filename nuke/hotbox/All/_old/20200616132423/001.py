#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: <img src="P:/vikingsShorts/shots/sh_120/comp/shotIcon/sh_120_shotIcon.jpg"> 120 </img>
#
#----------------------------------------------------------------------------------------------------------

import glob
import os

drive = 'P:'
shot = '120'
project = 'vikingsShorts'

os.environ["SHOT"] = '%s/%s/shots/sh_%s' % (drive, project, shot)

search_dir = '%s/%s/shots/SH_%s/comp/' % (drive, project, shot)
files = filter(os.path.isfile, glob.glob(search_dir + "*"))
onlyNKfiles = [i for i in files if '~' not in i and '.autosave' not in i]
onlyNKfiles.sort(key=lambda x: os.path.getmtime(x))


nuke.scriptOpen(onlyNKfiles[-1])