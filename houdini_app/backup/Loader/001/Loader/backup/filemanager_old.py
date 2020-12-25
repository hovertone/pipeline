# -*- coding: utf-8 -*-


try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    import hou
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os, sys




from houdini.Loader.loader_v001_UIs import Ui_FileManager
from houdini.Loader.loader_preferences import LoaderPrefs



class Filemanager(QDialog, Ui_FileManager):

    _storage = "P:"
    _config_name = "project_config.csv"
    _config = None
    _file_path = None
    _last_selected = None

    def __init__(self, parent=None):
        super(Filemanager, self).__init__(parent)
        self.setupUi(self)

        # UI SETTINGS #
        self.pb_open.setEnabled(False)
        self._projects = os.listdir(self._storage)

        # CLICK SIGNALS #
        self.cbox_project.currentIndexChanged.connect(self.get_sequence)
        self.cbox_sequence.currentIndexChanged.connect(self.get_shots)
        self.cbox_shot.currentIndexChanged.connect(self.get_list)
        self.cbox_type.currentIndexChanged.connect(self.get_list)
        self.listWidget_files.itemClicked.connect(self.item_clicked)
        self.listWidget_files.itemDoubleClicked.connect(self.load_scene)
        self.pb_open.clicked.connect(self.load_scene)
        self.pb_close.clicked.connect(self.close)

        # CALL CLASS FUNCTIONS #
        self.get_projects()
        self.get_sequence()

        # UI PREFERENCES
        self.pref = LoaderPrefs()
        if not os.path.exists(self.pref.path):
            pass
        else:
            data = self.pref.load()
            print "DataPreferences: ", data
            self.loader_preferences(save=False)



    def get_projects(self):
        self.cbox_project.addItems(self._projects)


    def get_sequence(self):
        self._last_selected = None
        self.cbox_sequence.clear()
        sequence = os.listdir(os.path.join(self._storage, self.cbox_project.currentText()))
        self.cbox_sequence.addItems(sequence)



    def get_shots(self):
        self._last_selected = None
        self.cbox_shot.clear()
        path = '/'.join([self._storage, self.cbox_project.currentText(), self.cbox_sequence.currentText(), 'shots'])

        if os.path.exists(path):
            shots = os.listdir(path)
            self.cbox_shot.setEnabled(True)
            self.cbox_shot.addItems(shots)
        else:
            self.cbox_shot.clear()
            self.cbox_shot.setEnabled(False)


    def get_list(self):
        self._last_selected = None
        path = "/".join([self._storage,
                         self.cbox_project.currentText(),
                         self.cbox_sequence.currentText(),
                         "shots",
                         self.cbox_shot.currentText(),
                         self.cbox_type.currentText().lower()])
        print "FILES PATH: ", path

        self.listWidget_files.clear()
        self.pb_open.setEnabled(False)

        if os.path.exists(path):
            list = []
            for item in os.listdir(path):
                # SORTING AND REMOVE TECHNICAL FOLDERS
                if item[:1] == "!":
                    pass
                else:
                    list.append(item)
            self.listWidget_files.addItems(list)
        else:
            print "PATH ERROR"
        return self.config_read()


    def config_read(self):
        config = '/'.join([self._storage, self.cbox_project.currentText(), self.cbox_sequence.currentText(), self._config_name])
        try:
            file = open(config, "r")
            filedata = file.read()
            filedata = filedata.splitlines()[1:]
            self._config = []
            for item in filedata:
                self._config.append(item.split(","))
        except:
            print "NO CONFIG FILE"


    def item_clicked(self):
        if self.listWidget_files.currentItem().text()[-3:] == "hip":
            self.pb_open.setEnabled(True)
        # PATH
        # if not self._last_selected:
        #
        #     path = "/".join([self._storage,
        #                      self.cbox_project.currentText(),
        #                      self.cbox_sequence.currentText(),
        #                      "shots",
        #                      self.cbox_shot.currentText(),
        #                      self.cbox_type.currentText().lower(),
        #                      self.listWidget_files.currentItem().text()])
        # else:
        #     path = "/".join([self._storage,
        #                      self.cbox_project.currentText(),
        #                      self.cbox_sequence.currentText(),
        #                      "shots",
        #                      self.cbox_shot.currentText(),
        #                      self.cbox_type.currentText().lower(),
        #                      self._last_selected,
        #                      self.listWidget_files.currentItem().text()])
        #
        # if path[-3:] == "hip":
        #     ####### FIX THIS #######
        #     if self._last_selected:
        #         self.pb_open.setEnabled(True)
        #         self._file_path = "/".join([self._storage,
        #                                     self.cbox_project.currentText(),
        #                                     self.cbox_sequence.currentText(),
        #                                     "shots",
        #                                     self.cbox_shot.currentText(),
        #                                     self.cbox_type.currentText().lower(),
        #                                     self._last_selected,
        #                                     self.listWidget_files.currentItem().text()])
        #     else:
        #         self.pb_open.setEnabled(True)
        #         self._file_path = "/".join([self._storage,
        #                                     self.cbox_project.currentText(),
        #                                     self.cbox_sequence.currentText(),
        #                                     "shots",
        #                                     self.cbox_shot.currentText(),
        #                                     self.cbox_type.currentText().lower(),
        #                                     self.listWidget_files.currentItem().text()])
        #     return self._file_path


    def load_scene(self):
        path = "/".join([self._storage,
                         self.cbox_project.currentText(),
                         self.cbox_sequence.currentText(),
                         "shots",
                         self.cbox_shot.currentText(),
                         self.cbox_type.currentText().lower(),
                         self.listWidget_files.currentItem().text()])


        if self.listWidget_files.currentItem().text() == "..":
            self._last_selected = None
            self.listWidget_files.clear()
            self.get_list()
            self.item_clicked()

        elif os.path.isdir(path):
            self._last_selected = self.listWidget_files.currentItem().text()
            self.listWidget_files.clear()
            self.listWidget_files.addItem("..")
            self.listWidget_files.addItems(os.listdir(path))
            return self._last_selected

        else:
            if not self._last_selected:
                self._file_path = "/".join([self._storage,
                                            self.cbox_project.currentText(),
                                            self.cbox_sequence.currentText(),
                                            "shots",
                                            self.cbox_shot.currentText(),
                                            self.cbox_type.currentText().lower(),
                                            self.listWidget_files.currentItem().text()])
            else:
                self._file_path = "/".join([self._storage,
                                            self.cbox_project.currentText(),
                                            self.cbox_sequence.currentText(),
                                            "shots",
                                            self.cbox_shot.currentText(),
                                            self.cbox_type.currentText().lower(),
                                            self._last_selected,
                                            self.listWidget_files.currentItem().text()])


            print "DOUBLE CLICK ACTION", self.file_path
            self.loader_preferences(save=True)
            self.close()

            hou.hipFile.load(self.file_path, suppress_save_prompt=True, ignore_load_warnings=False)
            return self.setup_scene()


    def setup_scene(self):
        for i in self._config:
            if i[0] == self.cbox_shot.currentText():
                hou.hscript("setenv FSTART = " + i[1])
                hou.hscript("setenv FEND = " + i[2])
                hou.playbar.setPlaybackRange(i[1], i[2])

        hou.hscript("setenv PROJECT = " + "/".join([self._storage, self.cbox_project.currentText(), self.cbox_sequence.currentText()]))
        hou.hscript("setenv ASSETBUILDS = " + "/".join([self._storage, self.cbox_project.currentText(), "assetBuilds"]))
        hou.hscript("setenv SHOT = " + "/".join([self._storage, self.cbox_project.currentText(), self.cbox_sequence.currentText(), self.cbox_shot.currentText()]))
        hou.hscript("setenv SN = " + self.cbox_shot.currentText())


    def loader_preferences(self, save=False):
        if save:
            self.pref.save([self.cbox_project.currentIndex(),
                            self.cbox_sequence.currentIndex(),
                            self.cbox_shot.currentIndex(),
                            self.cbox_type.currentIndex()])
        else:
            try:
                data = self.pref.load()
                self.cbox_project.setCurrentIndex(data[0])
                self.cbox_sequence.setCurrentIndex(data[1])
                self.cbox_shot.setCurrentIndex(data[2])
                self.cbox_type.setCurrentIndex(data[3])
            except:
                pass

    # PUBLIC PROPERTY VARIABLES
    @property
    def file_path(self):
        return self._file_path

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




