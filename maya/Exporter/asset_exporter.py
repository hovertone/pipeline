

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import sys, os, json

try:
    import maya.cmds as cmds
    import maya.mel as mel
except:
    pass

try:
    import motionblurKeyframesBake
except:
    pass


path = "X:/app/win/Pipeline/bot"
if not path in sys.path:
    sys.path.append(path)
try:
    import telegram
except:
    pass

path = "X:/app/win/Pipeline/p_utils"
if not path in sys.path:
    sys.path.append(path)
import telega


from AssetExporter_UI_UIs import Ui_AssetExportDialog
from list_dialog import ListDialog


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
        self.pb_tool.clicked.connect(self.get_nameList)

        self.le_filePath.setText("NO VARIABLE FOUND. US <Pipeline/FileManager>")
        self.pb_export.setEnabled(False)

        self.objNameList = ListDialog(parent=self)
        self.objNameList.list.itemDoubleClicked.connect(self.objectName_fromList)
        self.objNameList.pb_ok.clicked.connect(self.objectName_fromList)

        self.compNameList = ListDialog(parent=self)
        self.compNameList.list.itemDoubleClicked.connect(self.compName_fromList)
        self.compNameList.pb_ok.clicked.connect(self.compName_fromList)
        self.ch_box_message.setChecked(True)
        self.ch_box_namespace.setChecked(True)

        self.set_filePath()
        if not name:
            try:
                self.load_params()
            except:
                pass


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
        self.save_params()
        path = self.le_filePath.text().split("/")[:-1]
        p_path = "/".join(path)
        if not os.path.exists(p_path):
            os.makedirs(p_path)
        self.close()
        if "BGEO" in self.comboBoxExt.currentText():
            self.bgeo_export(self.le_filePath.text())
        else:
            if self.comboBoxType.currentText() == "ANIMATION":
                self.export_anim(self.le_filePath.text())
            else:
                self.export_geo(self.le_filePath.text())



    def bgeo_export(self, path):
        temp = os.path.join(os.path.expanduser("~"), "bgeoTemp").replace("\\", "/")
        if not os.path.exists(temp):
            os.makedirs(temp)
        cmds.delete(cmds.ls(type="houdiniAsset"))
        asset = mel.eval('houdiniEngine_loadAsset "O:/fx/mayatobgeo.hda" "Sop/mayatobgeo::001";')
        setSelectio = mel.eval("AEhoudiniAssetSetInputToSelection " + asset + ".input[0].inputNodeId;")
        start = int(cmds.playbackOptions(q=True, min=True))
        end = int(cmds.playbackOptions(q=True, max=True))

        cmds.setAttr(asset + ".houdiniAssetParm_frames__tuple0", start - 3)
        cmds.setAttr(asset + ".houdiniAssetParm_frames__tuple1", end + 3)
        cmds.setAttr(asset + ".houdiniAssetParm.houdiniAssetParm_Path", temp + "/geo.$F.bgeo.sc", type="string")
        cmds.setAttr(asset + ".houdiniAssetParm.houdiniAssetParm_f_path", path, type="string")

        preStart = start - 3
        preEnd = end + 3

        for i in range(preEnd - preStart + 1):
            cmds.setAttr(asset + ".houdiniAssetParm.houdiniAssetParm_stds__button", 1)
            cmds.currentTime(preStart)
            preStart += 1

        cmds.setAttr(asset + ".houdiniAssetParm_frames__tuple0", start)
        cmds.setAttr(asset + ".houdiniAssetParm_frames__tuple1", end)
        cmds.currentTime(start)
        cmds.setAttr(asset + ".houdiniAssetParm.houdiniAssetParm_stdf__button", 1)
        cmds.currentTime(start)
        cmds.delete(asset)
        try:
            os.rmdir(temp)
        except:
            pass
        if self.ch_box_message.isChecked():
            telega.telegramReport(path, tp='cache')



    def export_geo(self, path):
        start = cmds.playbackOptions(query=True, minTime=True)

        if self.comboBoxGeoType.currentText() == "CHAR":
            self.export_reference(cmds.ls(sl=True)[0], path, str(start), str(start), "1")
        else:
            self.export_static(frame_start=str(start), path=path)

        if self.ch_box_message.isChecked():
            telega.telegramReport(path, tp='cache')


    def export_anim(self, path):
        mel.eval("paneLayout -e -manage false $gMainPane")
        start = cmds.playbackOptions(query=True, minTime=True)
        end = cmds.playbackOptions(query=True, maxTime=True)

        self.export_reference(cmds.ls(sl=True)[0], path, str(start-1), str(end+1), "1")

        mel.eval("paneLayout -e -manage true $gMainPane")
        if self.ch_box_message.isChecked():
            telega.telegramReport(path, tp = 'cache')


    def get_export_nodes(self, nodes):
        '''Return selection set nodes or all nodes.'''
        for selection_set in cmds.ls(nodes, exactType="objectSet"):
            selection_set_name = selection_set.rsplit(':', 1)[-1].lower()
            if 'export' in selection_set_name or 'abc' in selection_set_name:
                export_nodes = cmds.sets(selection_set, query=True)
                print(
                    'Found export set: "{}" ({} nodes)'.format(
                        selection_set, len(export_nodes)
                    )
                )
                if export_nodes:
                    return cmds.ls(export_nodes, type='transform', long=True)
        return nodes


    def get_roots(self, nodes):
        '''Return roots from *nodes*.'''
        all_nodes = cmds.ls(nodes, long=True, transforms=True, dag=True)
        roots = []
        for node in all_nodes:
            parent_nodes = cmds.listRelatives(node, parent=True, fullPath=True)
            if not parent_nodes or parent_nodes[0] not in all_nodes:
                roots.append(node)
        return roots


    def export_reference(self, reference_node, export_alembic_path, frame_start, frame_end, frame_step):
        '''Export reference to Alembic.'''
        namespace = cmds.referenceQuery(reference_node, namespace=True)
        roots = cmds.ls(namespace + ":rig|mdl", recursive=True, long=True)
        nodes = cmds.ls(
            cmds.referenceQuery(reference_node, nodes=True), type='transform', long=True
        )
        all_nodes = nodes
        # If export selection set is present, then apply it
        # otherwise just use "|rig|mdl"
        nodes = self.get_export_nodes(nodes)
        # Save the selection to restore when we are done
        saved_selection = cmds.ls(selection=True, long=True)
        alembic_job_args = [
            '-uvWrite',
            '-writeFaceSets',
            '-worldSpace',
            '-writeVisibility',
            '-stripNamespaces',
            '-uvWrite',
            '-frameRange',
            str(frame_start),
            str(frame_end),
            '-step',
            str(frame_step),
        ]
        alembic_job_args += ['-selection']
        print('Alembic roots:')
        for n in roots or self.get_roots(all_nodes):
            print(n)
            alembic_job_args += ['-root', n]
        alembic_job_args += ['-file ' + export_alembic_path]
        # Select objects to include
        cmds.select(nodes, hierarchy=True)
        print('cmds.AbcExport(j={})'.format(repr(' '.join(alembic_job_args))))
        cmds.AbcExport(j=' '.join(alembic_job_args))
        cmds.select(saved_selection)


    def export_static(self, frame_start, path):
        alembic_job_args = [
            '-uvWrite',
            '-writeFaceSets',
            '-worldSpace',
            '-writeVisibility',
            '-stripNamespaces',
            '-uvWrite',
            '-frameRange',
            str(frame_start),
            str(frame_start),
            '-step',
            str("1"),
            path]

        nodes = cmds.ls(sl=True)
        for n in self.get_roots(nodes):
            print(n)
            alembic_job_args += ['-root', n]
        cmds.AbcExport(j=' '.join(alembic_job_args))


    def save_params(self):
        data = [self.comboSource.currentIndex(),
                self.comboBoxGeoType.currentIndex(),
                self.comboBoxType.currentIndex(),
                self.le_version.text(),
                self.le_objectName.text(),
                self.le_component.text()]
        print "DATA", data
        conf = os.path.join(os.path.expanduser("~"), "exporter.config")
        with open(conf, 'w') as f:
            json.dump(data, f, indent=4)


    def load_params(self):
        c = os.path.join(os.path.expanduser("~"), "exporter.config")
        conf = json.load(open(c))
        print "LOAD", conf
        self.comboSource.setCurrentIndex(conf[0])
        self.comboBoxGeoType.setCurrentIndex(conf[1])
        self.comboBoxType.setCurrentIndex(conf[2])
        self.le_version.setText(conf[3])
        self.le_objectName.setText(conf[4])
        self.le_component.setText(conf[5])


    def send_message(self, path):
        tokenFile = open("X:/app/win/Pipeline/bot" + '/token.txt', 'r')
        tokenData = tokenFile.read()
        chatidFile = open("X:/app/win/Pipeline/bot" + '/chatid.txt', 'r')
        chatidData = chatidFile.read()
        bot = telegram.Bot(token=tokenData)
        user = os.environ["COMPUTERNAME"].lower()
        bot.send_message(chat_id=chatidData, text=user + " Exported cache: " + path, parse_mode=telegram.ParseMode.HTML)


    def get_nameList(self):
        try:
            # os.environ["ASSETBUILDS"] = "P:/Raid/assetBuilds"
            chars = os.listdir(os.environ["ASSETBUILDS"]+"/char")
            self.objNameList.list.addItems(chars)
            self.objNameList.show()
        except:
            pass







if __name__ == '__main__':

    app = QApplication([])
    w=AssetExporter()
    w.show()
    sys.exit(app.exec_())
