# -*- coding: utf-8 -*-


try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import hou
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os, sys, time

from functools import partial
from  loader_v001_UIs import Ui_FileManager
from loader_preferences import LoaderPrefs
from p_utils.csv_parser_bak import projectDict
from item import FileItem
from loader_pref import LoaderPreferencesUI
from assetSave import AssetSaveUI


class Filemanager(QDialog, Ui_FileManager):


    _config_name = "project_config.csv"
    _config = None
    _file_path = None
    _path = None
    _last_selected = None

    def __init__(self, parent=None):
        super(Filemanager, self).__init__(parent)
        self.setupUi(self)

        # UI SETTINGS #
        self.pb_open.setEnabled(False)
        self.pb_select_shot.setEnabled(False)
        self.pb_save.setEnabled(False)
        self.pb_new.setEnabled(False)
        self.listWidget_files.setSortingEnabled(False)

        self.new_asset = AssetSaveUI()

        # CLICK SIGNALS #
        self.cbox_project.currentIndexChanged.connect(self.get_sequence)
        self.cbox_sequence.currentIndexChanged.connect(self.get_shots)
        self.cbox_shot.currentIndexChanged.connect(self.get_list)
        self.cbox_type.currentIndexChanged.connect(self.typ_action)
        self.listWidget_files.itemClicked.connect(self.item_clicked)
        self.listWidget_files.itemDoubleClicked.connect(self.load_scene)
        self.pb_pref.clicked.connect(self.loader_preferences_UI)
        self.pb_open.clicked.connect(self.load_scene)
        self.pb_save.clicked.connect(self.save_scene)
        self.pb_new.clicked.connect(self.new_asset.show)
        self.pb_select_shot.clicked.connect(self.setup_scene)
        self.pb_close.clicked.connect(self.close)
        self.pb_byname.clicked.connect(partial(self.sorting_btn_clicked, self.pb_byname.text()))
        self.pb_bydate.clicked.connect(partial(self.sorting_btn_clicked, self.pb_bydate.text()))
        self.pb_reverse.clicked.connect(partial(self.sorting_btn_clicked, self.pb_reverse.text()))
        self.new_asset.pb_save.clicked.connect(self.save_new_asset)
        self.new_asset.pressEnter.connect(self.save_new_asset)


        # UI PREFERENCES
        self.pref = LoaderPrefs()
        data = self.pref.load()["indexes"]
        self._storage = self.pref.load()["storage"]["projects"]
        self._projects = os.listdir(self._storage)

        # CALL CLASS FUNCTIONS #
        self.get_projects()
        print "DataPreferences: ", data
        if data:
            self.loader_preferences(save=False)
        else:
            pass

        self.sorting_btn_clicked(btn="By Date")
        self.sorting_btn_clicked(btn="Reverse")



    def get_projects(self):
        self.cbox_project.addItems(self._projects)


    def get_sequence(self):
        self.cbox_sequence.clear()
        self._last_selected = None
        config = projectDict(self.cbox_project.currentText())
        self.cbox_sequence.addItem("assetBuilds")
        self.cbox_sequence.addItems(config.getSequences())


    def get_shots(self):
        if self.cbox_sequence.currentText()== "assetBuilds":
            self.label_shot.setEnabled(False)
            self.cbox_shot.clear()
            self.cbox_shot.setEnabled(False)
            self.get_types(t="assetBuilds")
        else:

            self.label_shot.setEnabled(True)
            self.cbox_shot.setEnabled(True)
            self.cbox_shot.clear()
            self._last_selected = None
            self.get_types(t="shots")
            try:
                config = projectDict(self.cbox_project.currentText())
                shots = config.getShots(self.cbox_sequence.currentText())
                self.cbox_shot.addItems(shots)
            except:
                print "ERROR TO GET SHOTS"


    def get_types(self, t):
        if t == "shots":
            self.cbox_type.clear()
            self.cbox_type.addItems(['fx', "light", "animation", "model"])
        else:
            self.cbox_type.clear()
            path = "/".join([self._storage, self.cbox_project.currentText(), "assetBuilds"])
            list_dir = os.listdir(path)
            self.cbox_type.addItems(list_dir)


    def typ_action(self):
        self._path = None
        return self.get_list()


    def get_list(self):
        self.listWidget_files.clear()
        self.pb_open.setEnabled(False)
        self.pb_save.setEnabled(False)
        self.pb_new.setEnabled(True)
        self.pb_select_shot.setEnabled(True)
        # PATH DIR

        if not self.path:
            if self.cbox_sequence.currentText() == "assetBuilds":
                path = "/".join([self._storage,
                                 self.cbox_project.currentText(),
                                 self.cbox_sequence.currentText(),
                                 self.cbox_type.currentText().lower()])
            else:
                path = "/".join([self._storage,
                                 self.cbox_project.currentText(),
                                 "sequences",
                                 self.cbox_sequence.currentText(),
                                 self.cbox_shot.currentText(),
                                 self.cbox_type.currentText().lower()])

        else:
            path = self.path
            model = FileItem(path=self.path, text="..", type="..")
            listItem = QListWidgetItem()
            self.listWidget_files.addItem(listItem)
            listItem.setSizeHint(QSize(0, 30))
            self.listWidget_files.setItemWidget(listItem, model)

        # LIST DIR AND REMOVE TECHNICAL FOLDERS FROM LIST
        list = []
        if os.path.exists(path):
            for item in os.listdir(path):
                if item[:1] == "!":
                    pass
                else:
                    list.append(item)

            # GET FILES INFO
            for i in list:
                # GET DATE AND TIME
                stats = os.stat(path + "/" + i)
                d = time.localtime(stats[8])
                dd = ".".join([str(d[2]), str(d[1]), str(d[0])])
                dt = ":".join([str(d[3]), str(d[4])])
                date = dict(day=dd, time=dt)

                # GET TYPE IS FILE OR FOLDER
                full_path = os.path.join(path, i)
                if os.path.isdir(full_path):
                    item_type = "folder"

                else:
                    item_type = "file"

                model = FileItem(path=path, text=i, type=item_type, date=date)

                listItem = QListWidgetItem()
                self.listWidget_files.addItem(listItem)
                listItem.setSizeHint(QSize(0, 30))
                self.listWidget_files.setItemWidget(listItem, model)

        self.sorting_btn_clicked(btn="By Date")
        self.sorting_btn_clicked(btn="Reverse")


    def item_clicked(self):
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        item_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).type
        if item_text[-3:] == "hip":
            self.pb_open.setEnabled(True)

        if item_type == "folder":
            self.pb_save.setEnabled(True)


    def load_scene(self):
        item_path = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        item_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).type
        item_date = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).date

        if item_type == "folder":
            self._path = os.path.join(item_path, item_text)
            return self._path, self.get_list()

        elif item_type == "..":
            self._path = None
            return self._path, self.get_list()

        elif item_type == "file":
            self._file_path = os.path.join(item_path, item_text)
            self.close()
            hou.hipFile.load(self.file_path, suppress_save_prompt=True, ignore_load_warnings=False)
            return self.setup_scene()


    # HOUDINI SETUP SCENE
    def setup_scene(self):
        hou.hscript("setenv PROJECT = " + "/".join([self._storage,
                                                    self.cbox_project.currentText()]))
        hou.hscript("setenv ASSETBUILDS = " + "/".join([self._storage,
                                                        self.cbox_project.currentText(),
                                                        "assetBuilds"]))
        storage = self.pref.load()["storage"]
        cache = "/".join([storage["caches"], self.cbox_project.currentText()])

        hou.hscript("setenv CACHE = " + cache)
        hou.hscript("setenv LIB = " + storage["lib"])
        hou.setFps(25)

        if self.cbox_sequence.currentText() != "assetBuilds":
            config = projectDict(self.cbox_project.currentText())
            shot_data = config.getAllShotData(seq=self.cbox_sequence.currentText(),
                                              shot=self.cbox_shot.currentText())


            hou.hscript("setenv FSTART = " + shot_data["first_frame"])
            hou.hscript("setenv FEND = " + shot_data["last_frame"])
            setGobalFrangeExpr = "tset `({0}-1)/$FPS` `{1}/$FPS`".format(int(shot_data["first_frame"]),
                                                                         int(shot_data["last_frame"]))
            hou.hscript(setGobalFrangeExpr)
            hou.playbar.setPlaybackRange(int(shot_data["first_frame"]),
                                         int(shot_data["last_frame"]))
            hou.hscript("setenv SQ = " + self.cbox_sequence.currentText())
            hou.hscript("setenv SHOT = " + "/".join([self._storage,
                                                     self.cbox_project.currentText(),
                                                     "sequences",
                                                     self.cbox_sequence.currentText(),
                                                     self.cbox_shot.currentText()]))
            hou.hscript("setenv SN = " + self.cbox_shot.currentText())
        self.loader_preferences(save=True)


    def sorting_btn_clicked(self, btn):
        print "SORTING: ", btn
        items = self.listWidget_files.count()
        list = []
        zero_item = None

        for item in range(items):
            i = self.listWidget_files.item(item)
            item = self.listWidget_files.itemWidget(i)

            if not item.text == "..":
                list.append(item)
            else:
                zero_item = item

        # SORTING LIST
        if btn == "By Name":
            list.sort(key=self.by_name)
        elif btn == "By Date":
            list.sort(key=self.by_date)
        else:
            list.reverse()

        self.listWidget_files.clear()

        if zero_item:
            list.insert(0, zero_item)

        for i in list:
            model = FileItem(path=i.path, text=i.text, type=i.type, date=i.date)
            listItem = QListWidgetItem()
            self.listWidget_files.addItem(listItem)
            listItem.setSizeHint(QSize(0, 30))
            self.listWidget_files.setItemWidget(listItem, model)



    def by_name(self, item):
        return item.text


    def by_date(self, item):
        filename = os.path.join(item.path, item.text)
        return os.stat(filename).st_mtime



    def config_read(self):
        config = '/'.join([self._storage,
                           self.cbox_project.currentText(),
                           self.cbox_sequence.currentText(),
                           self._config_name])
        try:
            file = open(config, "r")
            filedata = file.read()
            filedata = filedata.splitlines()[1:]
            self._config = []
            for item in filedata:
                self._config.append(item.split(","))
        except:
            print "NO CONFIG FILE"


    def loader_preferences(self, save=False):
        if save:
            old_data = self.pref.load()
            storage = old_data["storage"]
            index = [self.cbox_project.currentIndex(),
                            self.cbox_sequence.currentIndex(),
                            self.cbox_shot.currentIndex(),
                            self.cbox_type.currentIndex()]
            data = dict(storage=storage, indexes=index)
            self.pref.save(data)
        else:
            try:
                data = self.pref.load()["indexes"]
                self.cbox_project.setCurrentIndex(data[0])
                self.cbox_sequence.setCurrentIndex(data[1])
                self.cbox_shot.setCurrentIndex(data[2])
                self.cbox_type.setCurrentIndex(data[3])
            except:
                pass


    def loader_preferences_UI(self):
        global pref
        pref = LoaderPreferencesUI()
        pref.show()


    # SAVE SCENE AS NEW
    def save_new_asset(self):
        print "ENTER EVENT TO NEW ASSET"
        name = self.new_asset.le_assetName.text()
        user = os.environ['COMPUTERNAME'].lower()
        v_ext = "v001.hip"
        file_name = '_'.join([self.cbox_shot.currentText(), name, user, v_ext])

        if self.cbox_sequence.currentText() == "assetBuilds":
            path = "/".join([self._storage,
                             self.cbox_project.currentText(),
                             self.cbox_sequence.currentText(),
                             self.cbox_type.currentText().lower(),
                             name])
        else:
            path = "/".join([self._storage,
                             self.cbox_project.currentText(),
                             "sequences",
                             self.cbox_sequence.currentText(),
                             self.cbox_shot.currentText(),
                             self.cbox_type.currentText().lower(),
                             name])

        if not os.path.exists(path):
            os.makedirs(path)

        full_path = os.path.join(path, file_name)
        return hou.hipFile.save(full_path), self.new_asset.close(), self.setup_scene(), self.close()


    # SAVE SCENE TO EXISTING
    def save_scene(self, exists=False):
        item_path = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        item_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).type
        item_date = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).date

        path = os.path.join(item_path, item_text)
        user = os.environ['COMPUTERNAME'].lower()
        str_version = self.get_last_version(path)
        fileName = "_".join([self.cbox_shot.currentText(), item_text, user, "v"+str_version+".hip"])

        full_path = os.path.join(path, fileName)
        return hou.hipFile.save(full_path), self.setup_scene()


    def get_last_version(self, path):
        list = os.listdir(path)
        files = []
        versions = []

        for f in list:
            ff = os.path.join(path, f)
            if os.path.isfile(ff):
                files.append(f)

        for f in files:
            versions.append(int(f.rsplit(".", 1)[0][-3:]))

        print "VERSIONS: ", versions
        print "LAST IS: ", versions[-1]
        print  "NEW VERSION IS: ", self.pad_zeoro(versions[-1] + 1)
        return self.pad_zeoro(versions[-1] + 1)


    def pad_zeoro(self, version):
        index_s = str(version)
        zeros = '000'
        zeros = zeros[0:len(zeros) - len(index_s)]
        str_index = '%s%s' % (zeros, index_s)
        return str_index


    # PUBLIC PROPERTY VARIABLES
    @property
    def file_path(self):
        return self._file_path


    @property
    def path(self):
        return self._path


    @property
    def last_selected(self):
        return self._last_selected


    @property
    def config(self):
        return self._config




if __name__ == '__main__':

    app = QApplication([])
    w=Filemanager()
    w.show()
    sys.exit(app.exec_())




