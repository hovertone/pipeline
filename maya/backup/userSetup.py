import sys, os
import maya.cmds as cmds
import maya.utils
import maya.mel as mel

sys.path.append('X:/app/win/Pipeline')
import exporter_abc
import mat_group_attr as mg
from mat_group_attr import addAttrFromUi
import assetNameAttr as an


from maya import OpenMayaUI as omui

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except:
    from shiboken import wrapInstance
    from PySide.QtGui import *
    from PySide.QtCore import *


from ma_filemanager import MayaManager
from Exporter.asset_exporter import AssetExporter

def createUI():
    createMenuTool()


def createMenuTool():
    gMainWindow = maya.mel.eval('$temp1=$gMainWindow')
    tfx_mMenu = cmds.menu(parent=gMainWindow, tearOff=True, label='Pipeline')
    cmds.menuItem(parent=tfx_mMenu, label='FileManager', c='maya_manager()')
    cmds.menuItem(parent=tfx_mMenu, label='AssetExporter', c='asset_exporter()')



def maya_manager():
    if cmds.window('MayaManager', exists=True):
        cmds.deleteUI('MayaManager')
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    mayaManager = MayaManager(parent=mayaMainWindow)
    mayaManager.show()


def asset_exporter():
    if cmds.window('AssetExporter', exists=True):
        cmds.deleteUI('AssetExporter')
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    assetExporter = AssetExporter(parent=mayaMainWindow)
    assetExporter.show()


maya.utils.executeDeferred('createUI()')
