
import sys, os
import maya.cmds as cmds
import maya.utils
import maya.mel as mel
sys.path.append('X:\app\win\maya\scripts\python\tabs')
import exporter_abc
import mat_group_attr as mg
from mat_group_attr import addAttrFromUi
import  assetNameAttr as an

def createUI():
	createMenuTool()

	
def createMenuTool():
	gMainWindow = maya.mel.eval('$temp1=$gMainWindow')
	tfx_mMenu = cmds.menu(parent=gMainWindow, tearOff=True, label='ABC')
	cmds.menuItem(parent=tfx_mMenu, label='Set AssetName', c='an.setAttrUI()')
	cmds.menuItem(parent=tfx_mMenu, label='Export Anim', c='exporter_abc.export_assets()')
	cmds.menuItem(parent=tfx_mMenu, label='Export Geo', c='exporter_abc.export_geo()')
	cmds.menuItem(parent=tfx_mMenu, label='Add Attr', c='mg.addAttrMatGroup()')
	cmds.menuItem(parent=tfx_mMenu, label='Set MatGrp', c='mg.setAttrUI()')

maya.utils.executeDeferred('createUI()')



