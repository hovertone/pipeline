


try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

except:
    from PySide.QtGui import *
    from PySide.QtCore import *


from functools import partial
import sys, os

path = "X:/app/win/Pipeline/p_utils"
sys.path.append(path)


from projectCreateUI import Ui_ProjectCreate
from sq_item import SequenceItem
from shot_item import ShotItem
from csv_parser import projectDict
from houdini_app.Loader.loader_pref import LoaderPrefs



class ProjectCreate(QDialog, Ui_ProjectCreate):
    def __init__(self, parent=None):
        super(ProjectCreate, self).__init__(parent)
        self.setupUi(self)

        self.pb_Sq_add.setEnabled(False)
        self.pb_sq_remove.setEnabled(False)
        self.pb_sq_clear.setEnabled(False)

        self.pb_Shots_add.setEnabled(False)
        self.pb_Shots_remove.setEnabled(False)
        self.pb_Shots_clear.setEnabled(False)

        self.pb_create.setEnabled(False)

        self.listWidgetSq.setAlternatingRowColors(True)
        self.listWidgetShots.setAlternatingRowColors(True)
        self.le_Step.setValidator(QIntValidator())
        self.le_Step.setText("10")

        self.le_root.textChanged.connect(self.project_name)
        self.le_projectName.textChanged.connect(self.project_name)
        self.pb_Sq_add.clicked.connect(self.add_sequence)
        self.pb_Sq_add.setDefault(False)
        self.pb_sq_remove.clicked.connect(self.remove_sq)
        self.pb_sq_clear.clicked.connect(self.clear_sq)
        self.pb_Shots_add.clicked.connect(self.add_shot)
        self.pb_Shots_remove.clicked.connect(self.remove_shot)
        self.pb_Shots_clear.clicked.connect(self.clear_shots)
        self.pb_create.clicked.connect(self.create_project_data)
        self.pb_cancel.clicked.connect(self.close)
        self.listWidgetSq.itemClicked.connect(self.sqClicked)
        self.listWidgetShots.itemClicked.connect(self.shotClicked)

        self.pref = LoaderPrefs()
        self._storage = self.pref.load()["storage"]["projects"]


    def keyPressEvent(self, *args, **kwargs):
        pass



    def project_name(self):
        self.listWidgetSq.clear()
        self.listWidgetShots.clear()
        if len(self.le_projectName.text()) > 1:
            project_root_folders = os.listdir(self.le_root.text())
            self.pb_Sq_add.setEnabled(True)
            self.pb_sq_remove.setEnabled(True)
            self.pb_sq_clear.setEnabled(True)
            self.pb_create.setEnabled(True)
            if self.le_projectName.text() in project_root_folders:
                self.existing_project_dict = projectDict(self.le_projectName.text(), path)
                print '%s project exists' % self.le_projectName.text()
                #print self.existing_project_dict
                self.fill_with_existing()
        else:
            self.pb_Sq_add.setEnabled(False)
            self.pb_sq_remove.setEnabled(False)
            self.pb_sq_clear.setEnabled(False)
            self.pb_create.setEnabled(False)

    def fill_with_existing(self):
        self.listWidgetSq.clear()
        data = self.existing_project_dict.getDict()

        seqs = data.keys()
        for seq in seqs:
            shots_data = data[seq]

            model = SequenceItem(name = seq, data = shots_data)
            listItem = QListWidgetItem()
            self.listWidgetSq.addItem(listItem)
            listItem.setSizeHint(QSize(0, 55))
            self.listWidgetSq.setItemWidget(listItem, model)

    def add_sequence(self):
        print "ADD SQ CLICKED"
        ######################
        index = self.listWidgetSq.count() + 1
        model = SequenceItem(index=index)
        listItem = QListWidgetItem()
        self.listWidgetSq.addItem(listItem)
        listItem.setSizeHint(QSize(0, 55))
        self.listWidgetSq.setItemWidget(listItem, model)











    def add_shot(self):
        print "ADD SHOT CLICKED"
        ######################
        if self.listWidgetSq.currentItem():
            if self.listWidgetShots.count() > 0:
                last = range(self.listWidgetShots.count())[-1]
                sh = self.listWidgetShots.itemWidget(self.listWidgetShots.item(last)).data["name"]
                lst_shot = int(sh) + int(self.le_Step.text())
            else:
                lst_shot = int(self.le_Step.text())

            print "LAST SHOT", lst_shot
            model = ShotItem(index=lst_shot)
            listItem = QListWidgetItem()
            self.listWidgetShots.addItem(listItem)
            listItem.setSizeHint(QSize(0, 55))
            self.listWidgetShots.setItemWidget(listItem, model)
            self.shotClicked()





    def remove_sq(self):
        print "REMOVE SQ CLICKED"
        ######################
        if self.listWidgetSq.currentItem():
            self.listWidgetSq.takeItem(self.listWidgetSq.row(self.listWidgetSq.currentItem()))
            self.listWidgetShots.clear()


    def remove_shot(self):
        print "REMOVE SHOT CLICKED"
        ######################
        if self.listWidgetShots.currentItem():
            self.listWidgetShots.takeItem(self.listWidgetShots.row(self.listWidgetShots.currentItem()))
            self.shotClicked()


    def clear_sq(self):
        self.listWidgetSq.clear()
        self.listWidgetShots.clear()



    def clear_shots(self):
        self.listWidgetShots.clear()
        self.shotClicked()



    def sqClicked(self):
        print "SQ ITEM CLICKED"
        ######################

        self.pb_Shots_add.setEnabled(True)
        self.pb_Shots_remove.setEnabled(True)
        self.pb_Shots_clear.setEnabled(True)

        shots = self.listWidgetSq.itemWidget(self.listWidgetSq.currentItem()).shots
        if shots:
            self.listWidgetShots.clear()
            for shot in shots:
                model = ShotItem(data=shot)

                model.le_shot.textChanged.connect(self.check_shot_name)
                model.le_frame_start.textChanged.connect(self.shotClicked)
                model.le_frame_end.textChanged.connect(self.shotClicked)
                model.le_preroll.textChanged.connect(self.shotClicked)

                listItem = QListWidgetItem()
                self.listWidgetShots.addItem(listItem)
                listItem.setSizeHint(QSize(0, 55))
                self.listWidgetShots.setItemWidget(listItem, model)
            self.shotClicked()
        else:
            self.listWidgetShots.clear()


    def check_shot_name(self, text):
        print "SHOT LE CHANGE", text
        if text == "":
            self.pb_create.setEnabled(False)
        else:
            self.pb_create.setEnabled(True)



    def shotClicked(self):
        print "SHOT ITEM CLICKED"
        ######################
        count = self.listWidgetShots.count()
        shots = []
        for i in range(count):
            item = self.listWidgetShots.item(i)
            shot = self.listWidgetShots.itemWidget(item).data
            shots.append(shot)
        self.listWidgetSq.itemWidget(self.listWidgetSq.currentItem()).set_shots(shots)



    def create_project_data(self):
        if self.listWidgetSq.count() > 0:
            sq_data = []

            for sq in range(self.listWidgetSq.count()):
                sq_name = self.listWidgetSq.itemWidget(self.listWidgetSq.item(sq)).name
                if len(sq_name) > 2:
                    sq_shots = self.listWidgetSq.itemWidget(self.listWidgetSq.item(sq)).shots
                    print "NOT SORTED", sq_shots
                    if sq_shots:
                        new_list = sorted(sq_shots, key=lambda k: k['name'])
                        print "SORTED", new_list
                        sq = dict(sequence=sq_name, shots=new_list)
                        sq_data.append(sq)


            project_data = dict(project_path=self.le_root.text(),
                                project_name=self.le_projectName.text(),
                                data=sq_data)

            # PRINT DATA #
            print "PROJECT PATH: ", project_data["project_path"]
            print "PROJECT NAME: ", project_data["project_name"]
            for i in project_data["data"]:
                print "SEQUENCE NAME: ", i["sequence"]
                print "SHOTS: ", i["shots"]


            p_d = projectDict(project_data["project_name"], dr=self.le_root.text())
            for d in project_data["data"]:
                p_d.addSequence(d["sequence"])

                for shot in d["shots"]:
                    print "SHOTS DATA", shot
                    shot_name = "sh" + str(shot["name"])
                    p_d.addShot(seq=d["sequence"], shot_name=shot_name, first_frame=shot["first_frame"],
                                last_frame=shot["last_frame"], preroll=shot["preroll"])

            p_d.update_proj()
            self.close()

            #self.create_root(project_data["project_path"], project_data["project_name"])
            #self.create_project_csv(project_data)
            #self.create_folders(project_data)
            #self.close()


    def create_root(self, path, project_name):
        print "CREATE ROOT", path
        if os.path.exists(path):
            p_path = os.path.join(path, project_name)
            if not os.path.exists(p_path):
                return os.mkdir(p_path)




    def create_project_csv(self, project_data):
        path = "/".join([project_data["project_path"], project_data["project_name"], "project_config.csv"])

        data_lines = []

        # if os.path.isfile(path):
        #     fh = open(path, 'r')
        #     filedata = fh.read()
        #     old_data = filedata.split('\n')
        #     for d in old_data:
        #         if d == "":
        #             pass
        #         else:
        #             x = d + "\n"
        #             data_lines.append(x)

        fh = open(path, "w")
        for d in project_data["data"]:
            sq = "seq " + d["sequence"] + "\n"
            data_lines.append(sq)
            for shot in d["shots"]:
                shot_name = "sh"+str(shot["shot"])
                line = ",".join([shot_name, shot["first_frame"], shot["last_frame"], shot["preroll"] + "\n"])
                data_lines.append(line)

        # LAST EMPTY LINE FIX
        if '\n' in data_lines[-1]:
            data_lines[-1] = data_lines[-1].strip('\n')

        fh.writelines(data_lines)
        fh.close()




    def create_folders(self, project_data):
        rootFolders = ['assetBuilds',
        'assetBuilds/art',
        'assetBuilds/art/concept',
        'assetBuilds/art/src',
        'assetBuilds/art/in',
        'assetBuilds/art/out',
        'assetBuilds/footages',
        'assetBuilds/fx',
        'assetBuilds/hdri',
        'assetBuilds/char',
        'assetBuilds/props',
        'assetBuilds/env',
        'assetBuilds/hda',
        'in',
        'out',
        'dailies',
        'edit',
        'edit/src',
        'edit/sound',
        'edit/prProj',
        'preproduction',
        'preproduction/storyboard',
        'preproduction/script',
        'preproduction/prProj',
        'preproduction/previz',
        'ref']
        shotFolders = [ 'animation',
        'src',
        'track',
        'art',
        'cache',
        'cache/anim',
        'cache/anim/!cachename',
        'cache/fx',
        'cache/fx/!fxName',
        'cache/fx/!cacheName/v001',
        'cache/cam',
        'comp',
        'fx',
        'light',
        'render',
        'render/!layerName',
        'render/!layerName/v001',
        'out']

        ###############################################

        drive = project_data["project_path"]
        project = project_data["project_name"]
        projectPath = os.path.join(drive, project)



        for rf in rootFolders:
            folder = '/'.join([projectPath, rf])
            #print path
            if not os.path.exists(folder): os.makedirs(folder)

        for d in project_data["data"]:
            for shot in d["shots"]:
                for f in shotFolders:
                    folder = '/'.join([projectPath, 'sequences', d["sequence"], "sh"+shot["shot"], f])
                    #print folder
                    if not os.path.exists(folder): os.makedirs(folder)



if __name__ == '__main__':

    app = QApplication([])
    w=ProjectCreate()
    w.show()
    sys.exit(app.exec_())


