import sys, os
import maya.cmds as cmds
import maya.utils
import maya.mel as mel

sys.path.append(os.environ["PIPELINE_ROOT"])

from maya import OpenMayaUI as omui
import mat_group_attr as mg

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except:
    from shiboken import wrapInstanceff
    from PySide.QtGui import *
    from PySide.QtCore import *

from ma_filemanager_v2 import MayaManager2
from Exporter.asset_exporter import AssetExporter
import assetDailies
import playblastWithRV
import previzToMontage
import camera_publisher
import zshotmask
import setShotInOut
import soundImport

_MODULE_LIST = ['assetDailies', 'previzToMontage', 'camera_publisher', 'zshotmask', 'setShotInOut', 'soundImport']  #

try:
    ppath = os.getenv("MAYA_PLUG_IN_PATH")
    ppath += ";" + "X:/app/win/Pipeline/maya/plugins"
    os.environ["MAYA_PLUG_IN_PATH"] = ppath
except:
    os.environ["MAYA_PLUG_IN_PATH"] = "X:/app/win/Pipeline/maya/plugins"


def createUI():
    createMenuTool()


def createMenuTool():
    gMainWindow = maya.mel.eval('$temp1=$gMainWindow')
    tfx_mMenu = cmds.menu(parent=gMainWindow, tearOff=True, label='Pipeline')
    cmds.menuItem(parent=tfx_mMenu, label='FileManager', c='maya_manager()')
    cmds.menuItem(parent=tfx_mMenu, label='SaveUp', c='saveUp()')
    cmds.menuItem(parent=tfx_mMenu, label='AssetExporter', c='asset_exporter()')
    cmds.menuItem(parent=tfx_mMenu, label='Add Attr', c='mg.addAttrMatGroup()')
    cmds.menuItem(parent=tfx_mMenu, label='Set MatGrp', c='mg.setAttrUI()')
    cmds.menuItem(parent=tfx_mMenu, label='Playblast', c='playblastWithRV.createUI(playblastWithRV.applyCallback)')
    cmds.menuItem(parent=tfx_mMenu, label='Make montage Daily',
                  c='previzToMontage.createUI(previzToMontage.applyCallback)')
    cmds.menuItem(parent=tfx_mMenu, label='Make Asset Daily',
                  c='assetDailies.createUI("Make Daily", assetDailies.applyCallback)')
    cmds.menuItem(parent=tfx_mMenu, label='Import camera', c='camera_publisher.importLastCamVersionMaya()')
    cmds.menuItem(parent=tfx_mMenu, label='Export camera', c='camera_publisher.exportCamMaya()')
    cmds.menuItem(parent=tfx_mMenu, label='Import envProxy', c='asset_import_proxy()')
    cmds.menuItem(parent=tfx_mMenu, label='Export envProxy', c='asset_exporter_proxy()')
    cmds.menuItem(parent=tfx_mMenu, label='Import Sound', c='soundImport.main()')
    cmds.menuItem(parent=tfx_mMenu, label='Set Shot IN and OUT', c='setShotInOut.createUI(setShotInOut.applyCallback)')
    cmds.menuItem(parent=tfx_mMenu, label='Enable Viewport', c='enambleViewport()')


def enambleViewport():
    maya.mel.eval("paneLayout -e -manage true $gMainPane")


def maya_manager():
    if cmds.window('MayaManager', exists=True):
        cmds.deleteUI('MayaManager')
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    mayaManager = MayaManager2(parent=mayaMainWindow)
    mayaManager.show()





def asset_exporter():
    if cmds.window('AssetExporter', exists=True):
        cmds.deleteUI('AssetExporter')
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    assetExporter = AssetExporter(parent=mayaMainWindow)
    assetExporter.show()


def asset_import_proxy():
    if cmds.window('AssetExporter', exists=True):
        cmds.deleteUI('AssetExporter')
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    assetExporter = AssetExporter(name="envProxy", component="main", parent=mayaMainWindow)
    assetExporter.comboSource.setCurrentIndex(1)
    assetExporter.comboBoxGeoType.setCurrentIndex(1)
    assetExporter.get_last_version()
    path = assetExporter.le_filePath.text()
    print 'ENV PROXY', path
    cmds.AbcImport(path)


def asset_exporter_proxy():
    l = cmds.ls(transforms=True)
    for i in l:
        if "layout" in i:
            cmds.rename(i, "layout")

    cmds.select("layout")
    if cmds.window('AssetExporter', exists=True):
        cmds.deleteUI('AssetExporter')
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)
    assetExporter = AssetExporter(name="envProxy", component="main", parent=mayaMainWindow)
    assetExporter.comboSource.setCurrentIndex(1)
    assetExporter.comboBoxGeoType.setCurrentIndex(1)
    assetExporter.get_last_version(new=True)
    assetExporter.export_action()


def saveUp():
    usr = os.environ["COMPUTERNAME"].lower()
    filepath = cmds.file(q=True, sn=True)
    splited = filepath.rsplit("/", 1)
    path = splited[0]
    name = splited[1].rsplit(".", 1)[0]
    names = name.split("_")
    all_files = os.listdir(path)
    versions = []

    for f in all_files:
        if not "afanasy" in f:
            if ".mb" in f:
                v = f.split(".")[0][-3:]
                if v.isdigit() == True:
                    versions.append(int(v))

    versions = sorted(versions)
    up_version = str(versions[-1] + 1).zfill(3)
    mb_name = names[0] + "_" + names[1] + "_" + usr + "_v" + up_version + ".mb"
    full_path = os.path.join(path, mb_name).replace("\\", "/")
    cmds.file(rename=full_path)
    cmds.file(save=True)


maya.utils.executeDeferred('createUI()')
