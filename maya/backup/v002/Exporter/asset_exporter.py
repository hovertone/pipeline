

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
except:
    pass



from AssetExporter_UI_UIs import Ui_AssetExportDialog



class AssetExporter(QDialog, Ui_AssetExportDialog):
    def __init__(self, parent=None):
        super(AssetExporter, self).__init__(parent)
        self.setupUi(self)

        self.horizontalSlider.valueChanged.connect(self.set_version_value)
        self.comboBoxType.currentIndexChanged.connect(self.set_get_type)
        self.comboSource.currentIndexChanged.connect(self.set_filePath)
        self.comboBoxGeoType.currentIndexChanged.connect(self.set_filePath)
        self.comboBoxExt.currentIndexChanged.connect(self.set_filePath)
        self.le_version.textChanged.connect(self.set_filePath)
        self.le_objectName.textChanged.connect(self.set_filePath)
        self.le_component.textChanged.connect(self.set_filePath)
        self.pb_export.clicked.connect(self.export_action)

        self.comboBoxGeoType.addItems(["PROPS", "ENV", "CHAR"])
        self.le_filePath.setText("NO VARIABLE FOUND. US <Pipeline/FileManager>")
        self.pb_export.setEnabled(False)

        self.set_filePath()



    def set_version_value(self):
        self.le_version.setText(str(self.horizontalSlider.value()))


    def set_get_type(self):
        if self.comboBoxType.currentText() == "GEO":
            self.comboBoxGeoType.setEnabled(True)
        else:
            self.comboBoxGeoType.setEnabled(False)
        self.set_filePath()


    def pad_zeoro(self, version):
        index_s = str(version)
        zeros = '000'
        zeros = zeros[0:len(zeros) - len(index_s)]
        str_index = '%s%s' % (zeros, index_s)
        return str_index


    def set_filePath(self):
        try:
            assets = os.environ["ASSETBUILDS"]
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
        objects = self.getSelectGeo()
        selLong = cmds.ls(objects, visible=True, l=True)
        selString = str(' -root '.join(selLong))

        command = (
            "-frameRange {0} {1} -step {2} -attr matGroup -writeVisibility -uvWrite -writeFaceSets -wholeFrameGeo -worldSpace -writeUVSets -dataFormat ogawa -root {3} -file  {4}").format(
            str(int(1)), str(int(2)), str(1), selString, str(path))
        cmds.AbcExport(j=command)


    def export_anim(self, path):
        start = cmds.playbackOptions(query=True, minTime=True)
        end = cmds.playbackOptions(query=True, maxTime=True)

        objects = self.getSelectGeo()
        selLong = cmds.ls(objects, visible=True, l=True)
        selString = str(' -root '.join(selLong))

        command = (
            "-frameRange {0} {1} -step {2} -attr matGroup -writeVisibility -uvWrite -writeFaceSets -wholeFrameGeo -worldSpace -writeUVSets -dataFormat ogawa -root {3} -file  {4}.abc ").format(
            str(int(start)), str(int(end)), str(0.2), selString, str(path))
        print "ALEMBIC COMMAND ", command
        cmds.AbcExport(j=command)








if __name__ == '__main__':

    app = QApplication([])
    w=AssetExporter()
    w.show()
    sys.exit(app.exec_())
