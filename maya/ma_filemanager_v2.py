
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import maya.cmds as cmds
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os, sys
from houdini_app.Loader.filemanager_v3 import Filemanager

from p_utils.csv_parser_bak import projectDict


class MayaManager2(Filemanager):
    def __init__(self, parent=None):
        super(MayaManager2, self).__init__(parent)



    def item_clicked(self):
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        item_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).folder_type
        if item_text[-2:] == "mb" or item_text[-2:] == "ma":
            self.pb_open.setEnabled(True)

        if item_type == "folder" or item_type == "asset":
            self.pb_save.setEnabled(True)


    def load_scene(self):
        item_path = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        asset_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).asset_type
        folder_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).folder_type
        item_date = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).date

        print "ITEM PATH", item_path
        print "ITEM TEXT", item_text
        print "ASSET TYPE", asset_type
        print "FOLDER TYPE", folder_type

        if self.cbox_sequence.currentText() == "assetBuilds":
            if not os.path.isfile(item_path+"/"+item_text):
                folder_type = "asset"
                self.pb_new.setText("Add Component")
                self.pb_save.setVisible(True)
                self.pb_open.setVisible(True)
                self.pb_select_shot.setVisible(True)

        if folder_type == "asset":
            self.pb_back.setEnabled(True)
            self._path = os.path.join(item_path, item_text).replace("\\", "/")
            return self.get_list(path=self._path, folder_type="asset")

        elif folder_type == "shot":
            self.h_slider_zoomView.setValue(50)
            self.slider_value()
            self.pb_back.setEnabled(True)
            self.pb_new.setText("Add Component")
            self.pb_save.setVisible(True)
            self.pb_open.setVisible(True)
            self.pb_select_shot.setVisible(True)

            self.pb_new.setMinimumSize(100,25)
            if self.cbox_sequence == "assetBuilds":
                self._path = os.path.join(item_path, item_text).replace("\\", "/")
            else:
                self._path = os.path.join(item_path, item_text).replace("\\", "/")
                self._path = os.path.join(self._path, asset_type).replace("\\", "/")
            self._shot = item_text
            return self._shot, self.get_list(path=self._path, folder_type="asset")

        elif folder_type == "file":
            if item_text[-2:] == "mb" or item_text[-2:] == "ma":
                self._file_path = os.path.join(item_path, item_text).replace("\\", "/")
                self.close()
                cmds.file(self.file_path, open=True, force=True, iv=True)
                return self.setup_scene(item_path)



    def load_last(self, full_path):
        print "LOAD LAST", full_path
        if os.path.isfile(full_path):
            cmds.file(full_path, open=True, force=True, iv=True)
            return self.close(), self.setup_scene(full_path.rsplit("/", 1)[0])




    # SAVE SCENE AS NEW
    def save_new_asset(self):
        print "ENTER EVENT TO NEW ASSET"
        name = self.new_asset.le_assetName.text()
        user = os.environ['COMPUTERNAME'].lower()
        v_ext = "v001.mb"

        if self.cbox_sequence.currentText() == "assetBuilds":
            file_name = '_'.join([name, user, v_ext])
            if not self.pb_new.text() == "Add Component":
                path = "/".join([self._storage,
                                 self.cbox_project.currentText(),
                                 self.cbox_sequence.currentText(),
                                 self.cbox_type.currentText().lower(),
                                 name])
                self.create_asset_folders(path)
            else:
                path = self.path
        else:
            file_name = '_'.join([self._shot, name, user, v_ext])
            massPath = [self._storage, self.cbox_project.currentText(), "sequences",
                        self.cbox_sequence.currentText(), self._shot,
                        self.cbox_type.currentText().lower(), name]
            print "MASS PATH: ", massPath
            path = "/".join(massPath)


        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                print "PATH CREATE ERROR"

        full_path = os.path.join(path, file_name).replace("\\", "/")

        self.close()

        if cmds.file(rename=full_path):
            if cmds.file(save=True):
                return self.new_asset.close(), self.setup_scene()



    # SAVE SCENE TO EXISTING
    def save_scene(self, exists=False):
        item_path = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        asset_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).asset_type
        folder_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).folder_type
        item_date = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).date

        path = os.path.join(item_path, item_text)
        user = os.environ['COMPUTERNAME'].lower()
        try:
            str_version = self.get_last_version(path)
        except:
            str_version = "001"

        if not self._shot:
            if self.cbox_sequence.currentText() == "assetBuilds":
                self._shot = item_path.split("/" +self.cbox_type.currentText()+"/")[1].split("/")[0]

        fileName = "_".join([self._shot, item_text, user, "v"+str_version+".mb"])

        full_path = os.path.join(path, fileName).replace("\\", "/")
        if cmds.file(rename=full_path):
            if cmds.file(save=True):
                return self.setup_scene(item_path=path)


    def setup_scene(self, item_path=None, new=None):
        os.environ["PROJECT"] = "/".join([self._storage, self.cbox_project.currentText()])
        os.environ["ASSETBUILDS"] = "/".join([self._storage, self.cbox_project.currentText(), "assetBuilds"])
        storage = self.pref.load()["storage"]
        cache = "/".join([storage["caches"], self.cbox_project.currentText()])

        os.environ["CACHE"] = cache
        os.environ["LIB"] = storage["lib"]
        cmds.currentUnit(time='film')

        cmds.optionVar(ca="CustomFileDialogSidebarUrls")
        cmds.optionVar(stringValueAppend=("CustomFileDialogSidebarUrls", os.environ["PROJECT"]))
        cmds.optionVar(stringValueAppend=("CustomFileDialogSidebarUrls", os.environ["ASSETBUILDS"]))
        if item_path:
            cmds.optionVar(stringValueAppend=("CustomFileDialogSidebarUrls", item_path))

        if self.cbox_sequence.currentText() != "assetBuilds":
            config = projectDict(self.cbox_project.currentText())
            shot_data = config.getAllShotData(seq=self.cbox_sequence.currentText(),
                                              shot=self._shot)
            cmds.playbackOptions(min=int(shot_data["first_frame"])-1, max=int(shot_data["last_frame"])+1)

            os.environ["SQ"] = self.cbox_sequence.currentText()
            os.environ["SHOT"] = "/".join([self._storage,
                                                     self.cbox_project.currentText(),
                                                     "sequences",
                                                     self.cbox_sequence.currentText(),
                                                     self._shot])

            cmds.optionVar(stringValueAppend=("CustomFileDialogSidebarUrls", os.environ["SHOT"]))

            os.environ["SN"] =  self._shot
            print "SHN", self._shot
        self.loader_preferences(save=True)




if __name__ == '__main__':

    app = QApplication([])
    w=MayaManager2()
    w.show()
    sys.exit(app.exec_())


