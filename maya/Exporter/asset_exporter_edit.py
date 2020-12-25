

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *
import sys, os

try:
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass

from AssetExporter_UI_UIs_v2 import Ui_AssetExportDialog
from list_dialog import ListDialog
#import motionblurKeyframesBake




class AssetExporter(QDialog, Ui_AssetExportDialog):
    def __init__(self, name=None, component=None, parent=None):
        super(AssetExporter, self).__init__(parent)
        self.setupUi(self)

        if name:
            self.le_objectName.setText(name)
        if component:
            self.le_component.setText(component)





        self.horizontalSlider.valueChanged.connect(self.set_version_value)
        self.comboBoxType.currentIndexChanged.connect(self.set_get_type)
        self.comboSource.currentIndexChanged.connect(self.set_filePath)
        self.comboBoxGeoType.currentIndexChanged.connect(self.set_filePath)
        self.comboBoxExt.currentIndexChanged.connect(self.set_filePath)
        self.le_version.textChanged.connect(self.set_filePath)
        self.le_objectName.textChanged.connect(self.set_filePath)
        self.le_component.textChanged.connect(self.set_filePath)
        self.pb_export.clicked.connect(self.export_action)
        self.pb_selectObjectName.clicked.connect(self.get_object_name)
        self.pb_componet.clicked.connect(self.get_component_name)
        self.pb_setLastVer.clicked.connect(self.get_last_version)



        self.comboBoxGeoType.addItems(["PROPS", "ENV", "CHAR"])
        self.le_filePath.setText("NO VARIABLE FOUND. US <Pipeline/FileManager>")
        self.pb_export.setEnabled(False)

        self.objNameList = ListDialog(parent=self)
        self.objNameList.list.itemDoubleClicked.connect(self.objectName_fromList)
        self.objNameList.pb_ok.clicked.connect(self.objectName_fromList)

        self.compNameList = ListDialog(parent=self)
        self.compNameList.list.itemDoubleClicked.connect(self.compName_fromList)
        self.compNameList.pb_ok.clicked.connect(self.compName_fromList)

        self.set_filePath()



    def get_object_name(self):
        source = str(self.comboSource.currentText())
        try:
            assets = os.environ[source]
            if self.comboBoxType.currentText() == "ANIMATION":
                path = "/".join([assets, "cache/anim"])
            else:
                path = "/".join([assets, self.comboBoxGeoType.currentText().lower()])
            self.objNameList.list.clear()
            self.objNameList.list.addItems(os.listdir(path))
            self.objNameList.show()
        except:
            pass



    def get_component_name(self):
        source = str(self.comboSource.currentText())
        try:
            assets = os.environ[source]
            if self.comboBoxType.currentText() == "ANIMATION":
                path = "/".join([assets, "cache/anim"])
            else:
                path = "/".join([assets, self.comboBoxGeoType.currentText().lower()])

            if self.le_objectName.text():
                object_path = os.path.join(path, self.le_objectName.text())
                if os.path.exists(object_path):
                    self.compNameList.list.clear()
                    self.compNameList.list.addItems(os.listdir(object_path))
                    self.compNameList.show()
                else:
                    pass
        except:
            pass


    def objectName_fromList(self):
        if self.objNameList.list.currentItem():
            item = self.objNameList.list.currentItem().text()
            self.objNameList.close()
            self.le_objectName.setText(item)



    def compName_fromList(self):
        if self.compNameList.list.currentItem():
            item = self.compNameList.list.currentItem().text()
            self.compNameList.close()
            self.le_component.setText(item)


    def get_last_version(self, new=False):
        filepath = self.le_filePath.text().rsplit("/", 2)[0]
        folders = os.listdir(filepath)
        versions = []
        for f in folders:
            versions.append(int(f.replace("v", "")))

        if not new:
            self.horizontalSlider.setValue(versions[-1])
        else:
            self.horizontalSlider.setValue(versions[-1]+1)



    def set_version_value(self):
        self.le_version.setText(str(self.horizontalSlider.value()))


    def set_get_type(self):
        if self.comboBoxType.currentText() == "GEO":
            self.comboBoxGeoType.setEnabled(True)
        else:
            self.comboBoxGeoType.setEnabled(False)
            self.le_component.setText("main")
        self.set_filePath()


    def pad_zeoro(self, version):
        index_s = str(version)
        zeros = '000'
        zeros = zeros[0:len(zeros) - len(index_s)]
        str_index = '%s%s' % (zeros, index_s)
        return str_index


    def set_filePath(self):
        env = self.comboSource.currentText()
        try:
            assets = os.environ[env]
            version = "v"+self.pad_zeoro(int(self.le_version.text()))

            if len(self.le_component.text()) > 0:
                base_folder = os.path.join(self.le_objectName.text(), self.le_component.text()).replace("\\", "/")
                base_name = self.le_objectName.text() + "_" + self.le_component.text()
            else:
                base_folder = self.le_objectName.text()
                base_name = self.le_objectName.text()

            name = base_name + "_" + version + "." + self.comboBoxExt.currentText().lower()

            if self.comboBoxType.currentText() == "ANIMATION":
                path = "/".join([assets,
                                      "cache/anim",
                                      base_folder,
                                      version,
                                      name])
            else:
                path = "/".join([assets,
                                      self.comboBoxGeoType.currentText().lower(),
                                      base_folder,
                                      self.comboBoxType.currentText().lower(),
                                      version,
                                      name])

            self.le_filePath.setText(path)
            self.pb_export.setEnabled(True)
        except:
            self.pb_export.setEnabled(False)



    def export_action(self):
        path = self.le_filePath.text().split("/")[:-1]
        p_path = "/".join(path)
        print "PATH SKA:", p_path
        if not os.path.exists(p_path):
            os.makedirs(p_path)
        self.close()
        if self.comboBoxType.currentText() == "ANIMATION":
            self.export_anim(self.le_filePath.text())
        else:
            self.export_geo(self.le_filePath.text())



    def getSelectGeo(self):
        object_for_select = cmds.ls(sl=True)
        cmds.select(object_for_select, hi=True)
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



    def export_geo(self, path):
        if not self.ch_box.isChecked():

            start = cmds.playbackOptions(query=True, minTime=True)
            end = cmds.playbackOptions(query=True, maxTime=True)
            cmds.select(hi=True)

            motionblurKeyframesBake.addExtraKeys(first=int(start), last=int(end))

            objects = cmds.ls(sl=True, type="mesh")
            cmds.select(objects)
            cmds.pickWalk(d="Up")
            selLong = cmds.ls(sl=True, visible=True, l=True)
            selString = str(' -root '.join(selLong))

            command = (
                "-frameRange {0} {1} -step {2} -attr matGroup -writeVisibility -uvWrite -writeFaceSets -wholeFrameGeo -worldSpace -writeUVSets -dataFormat ogawa -root {3} -file  {4}").format(
                str(int(1)), str(int(2)), str(1), selString, str(path))
            print "ALEMBIC COMMAND ", command
            cmds.AbcExport(j=command)
        else:
        #objects = self.getSelectGeo()
            selLong = cmds.ls(sl=True, visible=True, l=True)
            selString = str(' -root '.join(selLong))

            command = (
                "-frameRange {0} {1} -step {2} -attr matGroup -writeVisibility -uvWrite -writeFaceSets -wholeFrameGeo -worldSpace -writeUVSets -dataFormat ogawa -root {3} -file  {4}").format(
                str(int(1)), str(int(2)), str(1), selString, str(path))
            cmds.AbcExport(j=command)


    def export_anim(self, path):
        mel.eval("paneLayout -e -manage false $gMainPane")
        start = cmds.playbackOptions(query=True, minTime=True)
        end = cmds.playbackOptions(query=True, maxTime=True)
        cmds.showHidden(a=True)
        cmds.select(hi=True)

        #motionblurKeyframesBake.addExtraKeys(first=int(start), last=int(end))

        objects = cmds.ls(sl=True, type="mesh")
        cmds.select(objects)
        cmds.pickWalk(d="Up")
        selLong = cmds.ls(sl=True, visible=True, l=True)
        selString = str(' -root '.join(selLong))

        command = (
            "-frameRange {0} {1} -step {2} -attr matGroup -writeVisibility -uvWrite -writeFaceSets -wholeFrameGeo -worldSpace -writeUVSets -dataFormat ogawa -root {3} -file  {4}").format(
            str(int(start)-1), str(int(end)+1), str(1), selString, str(path))
        print "ALEMBIC COMMAND ", command
        cmds.AbcExport(j=command)

        mel.eval("paneLayout -e -manage true $gMainPane")




if __name__ == '__main__':

    app = QApplication([])
    w=AssetExporter()
    w.show()
    sys.exit(app.exec_())
