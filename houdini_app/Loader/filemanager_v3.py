# -*- coding: utf-8 -*-

import os, sys, time, subprocess

if os.environ["PIPELINE_ROOT"] not in sys.path:
    sys.path.append(os.environ["PIPELINE_ROOT"])



try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

try:
    import hou
    from houdini_app import lookdev
    from houdini_app.camera_publisher import importLastCamAtStartup
except:
    pass

from modules.pyseq import pyseq

from functools import partial
from  loader_v003_UIs import Ui_FileManager
from loader_preferences import LoaderPrefs
from p_utils.csv_parser import projectDict

from itemShot import FileItemShot
from itemDetail import ItemDetail
from loader_pref import LoaderPreferencesUI
from assetSave import AssetSaveUI

from houdini_app.AssetsUpdater.assets_update import AssetsUpdate
from add_shot_UIs import AddShot
from montage import MakeMontage




class Filemanager(QDialog, Ui_FileManager):

    _config_name = "project_config.csv"
    _config = None
    _file_path = None
    _path = None
    _shot = None
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
        self.h_slider_zoomView.setMinimum(30)
        self.h_slider_zoomView.setMaximum(400)
        self.h_slider_zoomView.setValue(250)
        self.listWidget_files.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget_files.customContextMenuRequested.connect(self.openMenu)

        self.pb_playHires = QPushButton()
        self.pb_playHires.setText("Play Dailies")
        self.pb_playHires.setMinimumSize(90, 35)
        self.pb_playHires.setMaximumSize(90,35)
        self.pb_playHires.setEnabled(False)
        self.horizontalLayout_4.addWidget(self.pb_playHires)

        self.new_asset = AssetSaveUI(parent)
        self.updater = AssetsUpdate(parent)
        self.addShot = AddShot(parent)
        self.montage = MakeMontage(self)

        # CLICK SIGNALS #
        self.cbox_project.currentIndexChanged.connect(self.get_sequence)
        self.cbox_sequence.currentIndexChanged.connect(self.get_types)
        self.cbox_type.currentIndexChanged.connect(self.type_action)
        self.listWidget_files.itemClicked.connect(self.item_clicked)
        self.listWidget_files.itemDoubleClicked.connect(self.load_scene)
        self.pb_playHires.clicked.connect(self.play_hires)
        self.pb_montage.clicked.connect(self.montageManager)

        #self.listWidget_files.mou
        self.pb_pref.clicked.connect(self.loader_preferences_UI)
        self.pb_open.clicked.connect(self.load_scene)
        self.pb_save.clicked.connect(self.save_scene)
        self.pb_new.clicked.connect(self.pushBtnNewAction)
        self.pb_select_shot.clicked.connect(self.setup_scene)
        self.pb_close.clicked.connect(self.close)
        self.pb_byname.clicked.connect(partial(self.sorting_btn_clicked, self.pb_byname.text()))
        self.pb_bydate.clicked.connect(partial(self.sorting_btn_clicked, self.pb_bydate.text()))
        self.pb_reverse.clicked.connect(partial(self.sorting_btn_clicked, self.pb_reverse.text()))
        self.new_asset.pb_save.clicked.connect(self.save_new_asset)
        self.new_asset.pressEnter.connect(self.save_new_asset)
        self.pb_back.clicked.connect(self.back_next_btn)
        self.pb_viewGrid.clicked.connect(partial(self.listViewChange, "grid"))
        self.pb_viewLine.clicked.connect(partial(self.listViewChange, "list"))
        self.h_slider_zoomView.valueChanged.connect(self.slider_value)

        #UI ICONS
        icon_path = os.path.join(os.path.dirname(__file__).replace("\\", "/"), "icons")
        self.pb_back.setIcon(QPixmap(icon_path + "/back.png"))
        self.pb_viewGrid.setIcon(QPixmap(icon_path + "/grid_white.png"))
        self.pb_viewLine.setIcon(QPixmap(icon_path + "/line_white.png"))

        # UI PREFERENCES
        self.pref = LoaderPrefs()
        data = self.pref.load()["indexes"]
        self._storage = self.pref.load()["storage"]["projects"]
        print("Project storage: ", self._storage)
        proj = os.listdir(self._storage)
        self._projects = []

        for p in proj:
            fp = os.path.join(self._storage, p)
            fp = os.path.join(fp, "project_config.csv")
            if os.path.isfile(fp):
                self._projects.append(p)

        # CALL CLASS FUNCTIONS #
        self.get_projects()
        if data:
            self.loader_preferences(save=False)
        else:
            pass


    def openMenu(self, position):
        indexes = self.listWidget_files.selectedIndexes()

        if len(indexes) > 0:
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
        menu = QMenu()

        if self.listWidget_files.currentItem():
            if self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).folder_type == "shot":
                menu.addAction("Make dailies from plate", self.makeDailiesPlate)
        menu.addAction("Show in Explorer", self.show_inExplorer)
        menu.addAction("Add Image", self.file_dialog)
        menu.exec_(self.listWidget_files.viewport().mapToGlobal(position))


    def makeDailiesPlate(self):

        # PATH PREPARATION
        mpg = "X:/app/win/ffmpeg/bin/ffmpeg"
        path = os.path.join(
            self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path,
            self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text).replace("\\", "/")
        plate = path + "/src/animPlate"
        out_path = path + "/out/DAILIES_" + self.listWidget_files.itemWidget(
            self.listWidget_files.currentItem()).text + "_comp.mov"
        icon_path = path + "/out/proxy"
        if not os.path.exists(path+"/out"):
            os.mkdir(i+"/out")
        if not os.path.exists(icon_path):
            os.mkdir(icon_path)


        # SOUND
        if os.path.exists(plate):
            sound = None
            if os.path.isfile(path + "/src/plate/v001/audio.wav"):
                sound = path + "/src/plate/v001/audio.wav"

            # SEQUENCE TO DAILIES
            sqs = pyseq.get_sequences(plate)
            for s in sqs:
                if "animPlate" in (s.format('%h')):

                    # MAKE ICON
                    icon = os.path.join(s.format('%D'), s.format('%h')+s.format('%s%t'))
                    cmd = mpg + ' -gamma 2.2 -i ' + icon + ' -n -s 512x320 ' + icon_path + "/proxy.jpg"
                    subprocess.call(cmd, shell=True)

                    sq = os.path.join(s.format('%D'), s.format('%h%p%t'))
                    print("SQSQ", s.format('%s'))
                    shotName = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text

                    if sound:
                        cmd = mpg + " -threads 8 -r 24 -i " + sound + " -start_number " + s.format(
                            '%s') + " -i " + sq + \
                            ''' -vf "drawtext=fontfile=c\:/Windows/Fonts/courbd.ttf: \
                            text=''' + shotName + ''''       Frame\: %{eif\:n+1001\:d}': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: \
                            boxborderw=5: x=50: y=(h-text_h)-25" ''' + \
                            " -threads 8 -y -c:v libx264 -s 3200x1800 -r 24 -pix_fmt " \
                            "yuv420p -preset ultrafast -crf 23 " + out_path
                    else:
                        cmd = mpg + " -threads 8 -r 24 -start_number " + s.format(
                            '%s') + " -i " + sq + \
                            ''' -vf drawtext="fontfile=/path/to/font.ttf: \
                            text=''' + shotName + ''': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: \
                            boxborderw=5: x=(w-=text_w)/2: y=(h-text_h)/2" ''' + \
                            " -threads 8 -y -c:v libx264 -s 1920x1080 -r 24 -pix_fmt " \
                            "yuv420p -preset ultrafast -crf 23 " + out_path

                    print(cmd)

                    subprocess.call(cmd, shell=True)
                    self.get_list()


    def montageManager(self):
        self.get_list()
        shots = []
        for i in range(self.listWidget_files.count()):
            self.listWidget_files.setCurrentItem(self.listWidget_files.item(i))
            path = os.path.join(
                self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path,
                self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text).replace("\\", "/")
            shots.append(path)
        self.montage.set_shots(project_path=self._storage+self.cbox_project.currentText(),
                               sequence=self.cbox_sequence.currentText(),
                               shots=shots)
        self.montage.show()




    def show_inExplorer(self):
        path = os.path.join(
            self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path,
            self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text).replace("\\","/")
        subprocess.Popen(r'explorer ' + os.path.normpath(path))


    def file_dialog(self):
        fb_dialog = QFileDialog(self)
        fb_dialog.show()
        fb_dialog.filesSelected.connect(self.set_image)


    def set_image(self, image):
        item_path = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        proxy_path = item_path+"/"+item_text+"/out/proxy"

        if not os.path.exists(proxy_path):
            os.makedirs(proxy_path)
        else:
            try:
                os.remove(proxy_path+"/proxy.jpg")
            except:
                pass

        cmd = 'X:/app/win/ffmpeg/bin/ffmpeg -gamma 2.2 -i ' + image[0] + ' -n -s 720x512 ' + proxy_path + "/proxy.jpg"
        sp = subprocess.call(cmd, shell=True)
        try:
            self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).set_icon(proxy_path + "/proxy.jpg")
        except:
            pass


    def set_icon(self, icon):
        self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).set_icon(icon)



    def get_projects(self):
        self.cbox_project.addItems(self._projects)
        self.lb_path.setText(self.cbox_project.currentText())


    def get_sequence(self):
        self.cbox_sequence.clear()
        self._last_selected = None
        config = projectDict(self.cbox_project.currentText(), dr=self._storage)
        sqs = config.getSequences()
        sqs = sorted(sqs)
        sqs.insert(0, "assetBuilds")
        self.cbox_sequence.addItems(sqs)



    def get_types(self):
        self._shot = None
        self._path = None
        if self.cbox_sequence.currentText() != "assetBuilds":
            self.cbox_type.clear()
            self.cbox_type.addItems(['fx', "light", "animation", "model", "comp"])
        else:
            self.cbox_type.clear()
            path = "/".join([self._storage, self.cbox_project.currentText(), "assetBuilds"])
            list_dir = os.listdir(path)
            self.cbox_type.addItems("fx")
        return self._shot, self.type_action()


    def type_action(self):
        if self._shot:
            self._path = self.get_path(self._shot)
            return self.get_list(path=self._path, folder_type="asset")
        else:
            return self.get_list()




    def get_path(self, shot=None):
        if self.cbox_sequence.currentText() == "assetBuilds":
            path = "/".join([self._storage, self.cbox_project.currentText(),
                             self.cbox_sequence.currentText(),self.cbox_type.currentText()])
        else:
            if not shot:
                path = "/".join([self._storage, self.cbox_project.currentText(),
                                 "sequences", self.cbox_sequence.currentText()])
            else:
                path = "/".join([self._storage, self.cbox_project.currentText(), "sequences",
                                 self.cbox_sequence.currentText(), shot, self.cbox_type.currentText()])
        return path


    def get_list(self, path=None, asset_type=None, text=None, folder_type=None):
        self.listWidget_files.clear()
        self.pb_open.setEnabled(False)
        self.pb_save.setEnabled(False)
        self.pb_new.setEnabled(True)
        self.pb_select_shot.setEnabled(True)
        self.pb_playHires.setEnabled(False)

        if not path:
            self._path = self.get_path()
        else:
            self._path = path

        self.lb_path.setText(self._path)
        if not folder_type:
            f_type = "shot"
        else:
            f_type = folder_type

        # Checking keys in path, for "Up to" button
        tags = self._path.rsplit("/", 2)

        if tags[1] == "assetBuilds" and tags[2] == self.cbox_type.currentText():
            f_type = "shot"
            self.pb_back.setEnabled(False)
            self.pb_new.setText("Add Asset")
            self.pb_new.setMinimumSize(70, 25)
        elif tags[2] == self.cbox_sequence.currentText():
            f_type = "shot"
            self.pb_new.setText("Add Shot")
            self.pb_new.setMinimumSize(70, 25)
            self.pb_back.setEnabled(False)
            self.pb_save.setVisible(False)
            self.pb_open.setVisible(False)
            self.pb_select_shot.setVisible(False)


        # List View - Grid or List
        if f_type == "shot":
            self.listWidget_files.setFlow(QListView.LeftToRight)
            self.listWidget_files.setProperty("isWrapping", True)
            self.listWidget_files.setResizeMode(QListView.Adjust)
            self.listWidget_files.setLayoutMode(QListView.Batched)
        else:
            self.listWidget_files.setFlow(QListView.TopToBottom)
            self.listWidget_files.setProperty("isWrapping", False)
            self.listWidget_files.setResizeMode(QListView.Adjust)
            self.listWidget_files.setLayoutMode(QListView.Batched)

        if not asset_type:
            a_type = self.cbox_type.currentText()
        else:
            a_type = asset_type

        #TODO: KASTILIK. NEED FIX
        #LIST DIR AND REMOVE TECHNICAL FOLDERS FROM LIST
        list = []
        if os.path.exists(self._path):
            for item in os.listdir(self._path):
                if item[:1] == "!":
                    pass
                elif "afanasy" in item:
                    pass
                else:
                    list.append(item)
            for i in list:
                # GET DATE AND TIME
                stats = os.stat(self._path + "/" + i)
                d = time.localtime(stats[8])
                dd = ".".join([str(d[2]), str(d[1]), str(d[0])])
                dt = ":".join([str(d[3]), str(d[4])])
                date = dict(day=dd, time=dt)
                # GET TYPE IS FILE OR FOLDER
                full_path = os.path.join(self._path, i)
                if os.path.isdir(full_path):
                    pass
                    # f_type = "asset"
                else:
                    f_type = "file"
                # LIST ITEM MODEL BASE
                if f_type == "asset" or f_type == "file":
                    model = ItemDetail(path=self._path, asset_type=a_type, text=i, folder_type=f_type, date=date)
                    # CREATE BUTTON IN LIST ITEM FOR LOAD LAST VERSION
                    if f_type == "asset":
                        model.loadSignal.connect(self.load_last)
                    self.h_slider_zoomView.setValue(40)
                    listItem = QListWidgetItem()
                    self.listWidget_files.addItem(listItem)
                    listItem.setSizeHint(QSize(0, 40))
                    self.listWidget_files.setItemWidget(listItem, model)
                else:
                    model = FileItemShot(path=self._path, asset_type=a_type, text=i, folder_type=f_type, date=date)
                    self.h_slider_zoomView.setValue(140)
                    listItem = QListWidgetItem()
                    self.listWidget_files.addItem(listItem)
                    value = self.h_slider_zoomView.value()
                    listItem.setSizeHint(QSize(value, value / 1.35))
                    self.listWidget_files.setItemWidget(listItem, model)



        if folder_type == "asset":
            self.sorting_btn_clicked(btn="Date")
            self.sorting_btn_clicked(btn="Reverse")



    def listViewChange(self, btn):
        if btn == "grid":
            self.listWidget_files.setFlow(QListView.LeftToRight)
            self.listWidget_files.setProperty("isWrapping", True)
            self.listWidget_files.setResizeMode(QListView.Adjust)
            self.listWidget_files.setLayoutMode(QListView.Batched)
        else:
            self.listWidget_files.setFlow(QListView.TopToBottom)
            self.listWidget_files.setProperty("isWrapping", False)
            self.listWidget_files.setResizeMode(QListView.Adjust)
            self.listWidget_files.setLayoutMode(QListView.Batched)

        return self.sorting_btn_clicked(btn=btn)



    def slider_value(self):
        value = self.h_slider_zoomView.value()
        for i in range(self.listWidget_files.count()):
            self.listWidget_files.item(i).setSizeHint(QSize(value, value/1.2))


    def item_clicked(self):

        item_path = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        item_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).folder_type

        dp = item_path+"/"+item_text+"/out"
        if os.path.exists(dp):
            f = os.listdir(dp)
            if f and os.path.exists(dp+"/"+f[0]):
                self.pb_playHires.setEnabled(True)

        if item_text[-3:] == "hip":
            self.pb_open.setEnabled(True)

        if item_type == "asset":
            self.pb_save.setEnabled(True)


    def play_hires(self):
        item_path = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        item_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).folder_type

        dp = item_path+"/"+item_text+"/out"
        files = os.listdir(dp)

        if os.path.exists(dp):
            for f in files:
                if "DAILIES" in f:
                    subprocess.Popen("X:/app/win/rv/rv7.1.1/bin/rv.exe " + dp + "/" + f)
                    break



    def load_scene(self):
        item_path = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        asset_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).asset_type
        folder_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).folder_type
        item_date = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).date

        if self.cbox_sequence.currentText() == "assetBuilds":
            if not os.path.isfile(item_path+"/"+item_text):
                folder_type = "asset"
                self.pb_new.setText("Add Component")
                self.pb_save.setVisible(True)
                self.pb_open.setVisible(True)
                self.pb_select_shot.setVisible(True)
                self.pb_new.setMinimumSize(120, 25)

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
            self.pb_new.setMinimumSize(120,25)
            if self.cbox_sequence == "assetBuilds":
                self._path = os.path.join(item_path, item_text).replace("\\", "/")
            else:
                self._path = os.path.join(item_path, item_text).replace("\\", "/")
                self._path = os.path.join(self._path, asset_type).replace("\\", "/")
            self._shot = item_text
            return self._shot, self.get_list(path=self._path, folder_type="asset")

        elif folder_type == "file":
            if item_text[-3:] == "hip":
                self._file_path = os.path.join(item_path, item_text).replace("\\", "/")
                self.close()
                hou.hipFile.load(self.file_path)
                try:
                    importLastCamAtStartup()
                except:
                    pass
                return self.setup_scene(item_path)


    def load_last(self, full_path):
        if os.path.isfile(full_path):
            hou.hipFile.load(full_path)
            return self.setup_scene(full_path.rsplit("/", 1)[0])



    # HOUDINI SETUP SCENE
    def setup_scene(self, item_path=None, new=None):

        if item_path:
            path = item_path.replace("\\", "/")
            path = path.split("/")
            assetName = path[-1]
            assetType = path[-2]
            hou.hscript("setenv ASSETNAME = " + assetName)
            hou.hscript("setenv ASSETTYPE = " + assetType)
        try:

            viewer = hou.ui.paneTabOfType(hou.paneTabType.IPRViewer)
            viewer.setAutoSavePath("$SHOT/out/ipr/$SNAPNAME.$HIPNAME.$F4.$SAVENUM.exr")
        except:
            pass
        hou.hscript("setenv PROJECT = " + "/".join([self._storage, self.cbox_project.currentText()]))
        hou.hscript("setenv ASSETBUILDS = " + "/".join([self._storage, self.cbox_project.currentText(),"assetBuilds"]))
        storage = self.pref.load()["storage"]
        cache = "/".join([storage["caches"], self.cbox_project.currentText()])
        hou.hscript("setenv CACHE = " + cache)
        hou.hscript("setenv LIB = " + storage["lib"])
        hou.setFps(24)

        path = "/".join([self._storage, self.cbox_project.currentText(), "assetBuilds/hda"])
        hda = os.environ["HOUDINI_OTLSCAN_PATH"] + ";" + path + "/props;" + path + "/fx;" + path + "/char;"
        os.environ["HOUDINI_OTLSCAN_PATH"] = hda
        #hou.hscript("setenv HOUDINI_OTLSCAN_PATH = " + path +"/".join([self._storage, self.cbox_project.currentText(),"assetBuilds/hda"]))


        # SETUP SCENE IF IS SHOT #
        if self.cbox_sequence.currentText() != "assetBuilds":

            config = projectDict(self.cbox_project.currentText(), dr=self._storage)
            config.getSequences()
            shot_data = config.getAllShotData(seq=self.cbox_sequence.currentText(), shot=self._shot)

            if self.cbox_type.currentText() == "fx":
                ff = int(shot_data["first_frame"]) - int(shot_data["preroll"])
                lf = int(shot_data["last_frame"])
            else:
                ff = int(shot_data["first_frame"])
                lf = int(shot_data["last_frame"])

            print ("FRAMERANGE:", ff, lf)

            hou.hscript("setenv FSTART = " + shot_data["first_frame"])
            hou.hscript("setenv FEND = " + shot_data["last_frame"])

            user = os.environ['COMPUTERNAME'].lower()
            hou.hscript("setenv USER = " + user)
            hou.hscript("setenv START = " + shot_data["first_frame"])
            hou.hscript("setenv END = " + shot_data["last_frame"])

            setGobalFrangeExpr = "tset `({0}-1)/$FPS` `{1}/$FPS`".format(ff, lf)
            hou.hscript(setGobalFrangeExpr)
            hou.playbar.setPlaybackRange(ff, lf)
            hou.hscript("setenv SQ = " + self.cbox_sequence.currentText())
            print"SZAZAZAZA"
            hou.hscript("setenv SHOT = " + "/".join([self._storage, self.cbox_project.currentText(), "sequences",
                                                     self.cbox_sequence.currentText(), self._shot]))
            hou.hscript("setenv SN = " + self._shot)

        # SETUP SCENE IF IS ASSET BUILDS
        else:
            hip = os.environ["HIP"]
            hou.hscript("setenv SHOT = " + hip)
            if item_path:
                path = item_path.replace("\\", "/")
                path = path.split("/")
                if self.pb_new.text() == "Add Component":
                    assetName = path[-2]
                    hou.hscript("setenv SN = " + assetName)
                else:
                    assetName = path[-3]
                    hou.hscript("setenv SN = " + assetName)
                if new:
                    pass
                    #lookdev.main(assetname=assetName)
            else:
                hou.hscript("setenv SN = " + "")
        self.loader_preferences(save=True)
        self.updater.get_assets()
        if self.updater.listWidget.count() > 0:
            self.close()
            self.updater.show()






    def sorting_btn_clicked(self, btn):
        items = self.listWidget_files.count()
        list = []
        for item in range(items):
            i = self.listWidget_files.item(item)
            item = self.listWidget_files.itemWidget(i)
            list.append(item)

        # SORTING LIST
        if btn == "Name":
            list.sort(key=self.by_name)
        elif btn == "Date":
            list.sort(key=self.by_date)
        elif btn == "grid" or btn == "list":
            pass
        else:
            list.reverse()
        self.listWidget_files.clear()

        for i in list:
            ### LIST ITEM MODEL BASE ###
            if i.folder_type == "asset" or i.folder_type == "file":
                if btn == "grid":
                    model = FileItemShot(path=i.path, asset_type=i.asset_type,
                                         text=i.text, folder_type=i.folder_type, date=i.date)
                    self.h_slider_zoomView.setValue(150)
                elif btn == "list":
                    model = ItemDetail(path=i.path, asset_type=i.asset_type,
                                       text=i.text, folder_type=i.folder_type, date=i.date)
                    if i.folder_type == "asset":
                        model.loadSignal.connect(self.load_last)
                    self.h_slider_zoomView.setValue(60)
                else:
                    model = ItemDetail(path=i.path, asset_type=i.asset_type,
                                          text=i.text,folder_type=i.folder_type,date=i.date)
                    if i.folder_type == "asset":
                        model.loadSignal.connect(self.load_last)
                    self.h_slider_zoomView.setValue(60)
            else:
                if btn == "list":
                    model = ItemDetail(path=i.path, asset_type=i.asset_type,
                                       text=i.text, folder_type=i.folder_type, date=i.date)
                    if i.folder_type == "asset":
                        model.loadSignal.connect(self.load_last)
                    self.h_slider_zoomView.setValue(60)
                else:
                    model = FileItemShot(path=i.path, asset_type=i.asset_type,
                                         text=i.text, folder_type=i.folder_type, date=i.date)
                    self.h_slider_zoomView.setValue(150)

            listItem = QListWidgetItem()
            self.listWidget_files.addItem(listItem)
            value = self.h_slider_zoomView.value()
            listItem.setSizeHint(QSize(value, value / 1.2))
            self.listWidget_files.setItemWidget(listItem, model)


    def by_name(self, item):
        return item.text


    def by_date(self, item):
        filename = os.path.join(item.path, item.text)
        #print "STTIME:", os.stat(filename).st_mtime
        return os.stat(filename).st_mtime


    def back_next_btn(self):
        if self._path:
            path = self._path.split("/"+self.cbox_project.currentText()+"/")

            if not "assetBuilds" in path[1]:
                path_keys = path[1].split("/")
                if len(path_keys) == 5:
                    path = self._path.rsplit("/", 1)[0]
                    return self.get_list(path=path, folder_type="asset")
                else:
                    return self.get_list()

            elif "assetBuilds" in path[1]:
                path_keys = path[1].split("/")
                if len(path_keys) > 2:
                    path = self._path.rsplit("/", 1)[0]
                    return self.get_list(path=path, folder_type="asset")
            else:
                return self.get_list()
        else:
            return self.get_list()


    def config_read(self):
        config = '/'.join([self._storage, self.cbox_project.currentText(),
                           self.cbox_sequence.currentText(), self._config_name])
        try:
            file = open(config, "r")
            filedata = file.read()
            filedata = filedata.splitlines()[1:]
            self._config = []
            for item in filedata:
                self._config.append(item.split(","))
        except:
            print("NO CONFIG FILE")


    def loader_preferences(self, save=False):
        if save:
            old_data = self.pref.load()
            storage = old_data["storage"]
            index = [self.cbox_project.currentIndex(),
                     self.cbox_sequence.currentIndex(),
                     self.cbox_type.currentIndex(),
                     self.lb_path.text()]
            data = dict(storage=storage, indexes=index)
            self.pref.save(data)
        else:
            try:
                data = self.pref.load()["indexes"]
                self.cbox_project.setCurrentIndex(data[0])
                self.cbox_sequence.setCurrentIndex(data[1])
                self.cbox_type.setCurrentIndex(data[2])
                if len(data) == 4:
                    splited = data[3].split(self.cbox_sequence.currentText())
                    if splited[-1] == "":
                        f_type = "shot"
                    else:
                        f_type = "asset"
                    #self.get_list(path=data[3], folder_type=f_type)
                self.pb_back.setEnabled(True)
            except:
                pass


    def loader_preferences_UI(self):
        global pref
        pref = LoaderPreferencesUI()
        pref.show()


    # Button "ADD SHOT, ADD ASSET, ADD CMPONENT"
    def pushBtnNewAction(self):
        if self.pb_new.text() == "Add Shot":

            if not "assetBuilds" in self.cbox_sequence.currentText():
                self.addShot.pushButton.clicked.connect(self.updateShot)
            self.addShot.show()
        elif self.pb_new.text() == "Add Asset":
            self.new_asset.show()
        elif self.pb_new.text() == "Add Component":
            self.new_asset.show()
        else:
            pass

    def updateShot(self):
        conf = projectDict(self.cbox_project.currentText())
        conf.addSequence(self.cbox_sequence.currentText())
        conf.addShot(seq=self.cbox_sequence.currentText(),
                     shot_name="sh" + str(self.addShot.lineEdit_shot.text()),
                     first_frame=str(self.addShot.label_ff.text()),
                     last_frame=str(self.addShot.label_lf.text()))
        conf.update_proj()
        self.addShot.close()




    # SAVE SCENE AS NEW
    def save_new_asset(self):
        name = self.new_asset.le_assetName.text()
        user = os.environ['COMPUTERNAME'].lower()
        v_ext = "v001.hip"
        names = ""

        if self.cbox_sequence.currentText() == "assetBuilds":
            # <Add Asset>, <Add Shot>, <Add Component>
            if self.pb_new.text() == "Add Asset":

                path = "/".join([self._storage, self.cbox_project.currentText(),
                                 self.cbox_sequence.currentText(),
                                 self.cbox_type.currentText().lower(), name])

                self.create_asset_folders(path)
                path = path + "/main/lookdev"
                names = [name, "lookdev", user, v_ext]

            else:
                path = self.path + "/" + name
                m = self.path.split(self.cbox_type.currentText()+"/")[1]
                main = m.split("/")[0]
                names = [main, name, user, v_ext]

        else:
            path = "/".join([self._storage, self.cbox_project.currentText(), "sequences",
                             self.cbox_sequence.currentText(), self._shot,
                             self.cbox_type.currentText().lower(), name])

            names = [self._shot, name, user, v_ext]

        file_name = '_'.join(names)

        if not os.path.exists(path):
            os.makedirs(path)
        full_path = os.path.join(path, file_name).replace("\\", "/")
        hou.setFps(24)
        self.close()
        return hou.hipFile.save(full_path), self.new_asset.close(), self.setup_scene(path, new=True)


    def create_asset_folders(self, asset_path):
        folders = ["main", "main/modeling", "main/geo", "main/rig", "main/tex", "main/lookdev", "main/texturing",
                   "main/geo/v001", "main/rig/v001", "main/tex/v001"]

        for i in folders:
            path = os.path.join(asset_path, i).replace("\\", "/")
            if not os.path.exists(path):
                os.makedirs(path)


    # SAVE SCENE TO EXISTING
    def save_scene(self, exists=False):
        item_path = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        asset_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).asset_type
        folder_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).folder_type
        item_date = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).date

        path = os.path.join(item_path, item_text).replace("\\", "/")
        user = os.environ['COMPUTERNAME'].lower()

        try:
            str_version = self.get_last_version(path)
        except:
            str_version = "001"

        if not self._shot:
            if self.cbox_sequence.currentText() == "assetBuilds":
                self._shot = item_path.split("/" +self.cbox_type.currentText()+"/")[1].split("/")[0]

        fileName = "_".join([self._shot, item_text, user, "v"+str_version+".hip"])
        full_path = os.path.join(path, fileName).replace("\\", "/")
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
            if len(f.split(".")) == 2:
                versions.append(int(f.rsplit(".", 1)[0][-3:]))


        versions = sorted(versions)
        return self.pad_zeoro(versions[-1] + 1)


    def pad_zeoro(self, version):
        index_s = str(version)
        zeros = '000'
        zeros = zeros[0:len(zeros) - len(index_s)]
        str_index = '%s%s' % (zeros, index_s)
        return str_index


    def closeEvent(self, *args, **kwargs):
        return self.loader_preferences(save=True), self.close()


    # PUBLIC PROPERTY VARIABLES
    @property
    def file_path(self):
        return self._file_path

    @property
    def path(self):
        return self._path

    @property
    def shot(self):
        return self._shot

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




