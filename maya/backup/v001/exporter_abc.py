import os
import maya.mel as mel
import maya.cmds as cmds




# SMART SELECT MESHES
def getSelectGeo(object_for_select):
    print "SELECT"
    cmds.select(object_for_select)
    cmds.select(hi=True)
    all_objects = cmds.ls(sl=True)
    objects = cmds.ls(type='mesh')
    cmds.select(objects)
    cmds.pickWalk(d='Up')
    to_export = []
    for i in cmds.ls(sl=True):
        if i in all_objects:
            to_export.append(i)
        else:
            pass
	cmds.select(to_export)
	return to_export


def asset_version_str(int_version):
    version = str(int_version)
    zeros = '000'
    zeros = zeros[0:len(zeros) - len(version)]
    asset_version = '%s%s' % (zeros, version)
    return asset_version





def export_assets():
	# PATH PREFIX
	prim_path = '/'.join(cmds.file(query=True, sn=True).split('/')[:-2])
	try:
		ver = cmds.file(query=True, sn=True).split('.')[:-1][1]
	except:
		ver = 0

	# FRAMES RANGE
	start = cmds.playbackOptions(query=True, minTime=True)
	end = cmds.playbackOptions(query=True, maxTime=True)

	assets = cmds.ls(sl=True)
	assets_dict = []

	# GET ATTRIBUTES AND OBJECTS
	for asset in assets:
	    try:
	        atr = cmds.getAttr(asset + '.assetname')
	        item = dict(object=asset, name=atr)
	        assets_dict.append(item)
	    except:
	        print "Selected:", asset, "has no attribute: assetname"

	mel.eval('paneLayout -e -manage false $gMainPane')
	for a in assets_dict:

	    path = '/'.join([prim_path, 'cache/anim', a['name']])
	    if not os.path.exists(path):
	        os.makedirs(path)

	    version = asset_version_str(int(ver))
	    print "VERSION: ", version
	    file_path = '/'.join([path, a['name'] + '_v' + version])
	    print "FILEPATH: ", file_path

	    objects = getSelectGeo(a['object'])

	    print "SELECTED OBJECTS NAME: ", cmds.ls(sl=True)
	    selLong = cmds.ls(objects, visible=True, l=True)
	    print selLong
	    selString = str(' -root '.join(selLong))
	    command = (
	        "-frameRange {0} {1} -step {2} -attr matGroup -writeVisibility -uvWrite -writeFaceSets -wholeFrameGeo -worldSpace -writeUVSets -dataFormat ogawa -root {3} -file  {4}.abc ").format(
	        str(int(start)), str(int(end)), str(0.2), selString, str(file_path))

	    print "ALEMBIC COMMAND ", command
	    cmds.AbcExport(j=command)
	mel.eval('paneLayout -e -manage true $gMainPane')


def export_geo():
	# PATH PREFIX
	prim_path = '/'.join(cmds.file(query=True, sn=True).split('/')[:-2])
	print "PRIM_PATH", prim_path

	# VERSION GET
	try:
		v = int(cmds.file(query=True, sn=True).split('.')[0][-3:])
		ver = asset_version_str(v)
	except:
		ver = "001"

	# SELECT OB
	assets = cmds.ls(sl=True)
	assets_dict = []

	# GET ATTRIBUTES AND OBJECTS
	for asset in assets:
		try:
			atr = cmds.getAttr(asset + '.assetname')
			item = dict(object=asset, name=atr)
			assets_dict.append(item)
		except:
			print "Selected:", asset, "has no attribute: assetname"

	for a in assets_dict:

		# PATH FOR FILE
		path = '/'.join([prim_path, 'geo', v + ver])
		if not os.path.exists(path):
			os.makedirs(path)

		# FILE PATH
		file_path = '/'.join([path, a['name'] + '_v' + ver])
		print "FILEPATH: ", file_path

		# SELECT
		objects = getSelectGeo(a['object'])

	selLong = cmds.ls(objects, visible=True, l=True)

	selString = str(' -root '.join(objects))

	command = (
		"-frameRange {0} {1} -step {2} -attr matGroup -writeVisibility -uvWrite -writeFaceSets -wholeFrameGeo -worldSpace -writeUVSets -dataFormat ogawa -root {3} -file  {4}.abc ").format(
		str(int(1)), str(int(2)), str(1), selString, str(file_path))
	print "ALEMBIC COMMAND ", command
	cmds.AbcExport(j=command)


