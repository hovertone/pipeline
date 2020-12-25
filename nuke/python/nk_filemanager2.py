
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os, sys, time, nuke, re
from houdini_app.Loader.filemanager_v3 import Filemanager
from p_utils.csv_parser_bak import projectDict
from PL_shotsInitiation import attachStringAttr, attachTab
from PL_scripts import get_last_version, getPipelineAttrs



class NukeManager(Filemanager):
    def __init__(self, parent=None):
        super(NukeManager, self).__init__(parent)

        result = getPipelineAttrs()
        if result and result[1] != '':
            try:
                drive, project, seq, shot, assetName, version = getPipelineAttrs()

                project_i = [self.cbox_project.itemText(i) for i in range(self.cbox_project.count())].index(project)
                self.cbox_project.setCurrentIndex(project_i)

                seq_i = [self.cbox_sequence.itemText(i) for i in range(self.cbox_sequence.count())].index(seq)
                self.cbox_sequence.setCurrentIndex(seq_i)

                shot_i = [self.cbox_shot.itemText(i) for i in range(self.cbox_shot.count())].index(shot)
                self.cbox_shot.setCurrentIndex(shot_i)

                self.cbox_type.setCurrentIndex(4)
            except Exception as e:
                print('ERROR :: %s' % e)
        else:
            self.loader_preferences(save=False)
            # self.cbox_project.setCurrentIndex(4)
            # self.cbox_sequence.setCurrentIndex(2)
            # self.cbox_shot.setCurrentIndex(0)

        self.cbox_type.setCurrentIndex(4)



    def item_clicked(self):
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        item_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).folder_type
        if item_text[-2:] == "nk":
            print 'item click :: .nk'
            self.pb_open.setEnabled(True)

        if item_type == "asset":
            print 'item click :: asset'
            self.pb_save.setEnabled(True)



    def load_scene(self, item):
        item_path = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        asset_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).asset_type
        folder_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).folder_type
        item_date = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).date

        #nuke.tprint('%s\n%s\n%s\n%s' % (item_path, item_text, item_type, item_date))

        if folder_type == "asset":
            print 'load_scene :: folder type :: asset'
            self.pb_back.setEnabled(True)
            self._path = os.path.join(item_path, item_text).replace("\\", "/")
            return self.get_list(path=self._path, folder_type="asset")

        elif folder_type == "shot":
            print 'load_scene :: folder type :: shot'
            self.h_slider_zoomView.setValue(50)
            self.slider_value()
            self.pb_back.setEnabled(True)
            if self.cbox_sequence == "assetBuilds":
                self._path = os.path.join(item_path, item_text).replace("\\", "/")
            else:
                self._path = os.path.join(item_path, item_text).replace("\\", "/")
                self._path = os.path.join(self._path, asset_type).replace("\\", "/")
            self._shot = item_text
            return self._shot, self.get_list(path=self._path, folder_type="asset")

        elif folder_type == "file":
            if item_text[-2:] == "nk":
                print 'load_scene :: folder type :: file nk'
                self.loader_preferences(save=True)

                self._file_path = os.path.join(item_path, item_text).replace("\\", "/")
                self.close()

                nuke.scriptOpen(self._file_path)
                nuke.tprint('setup_scene %s' % os.path.split(item_path)[-1])
                self.setup_scene() # os.path.split(item_path)[-1]
                user = os.environ['COMPUTERNAME'].lower()

                modifiers = QApplication.keyboardModifiers()
                if user not in self._file_path and modifiers == Qt.ShiftModifier:
                    print 'load_scene :: SHIFT'
                    # checks if scripts is named by another person. If so - ask window will pop up
                    splitted = item_text.split('_')
                    splitted[-2] = user
                    curVer = splitted[-1]
                    match = re.match(r'v(\d*)', curVer)
                    newVer = get_last_version(path = item_path, filter = user)
                    replaced = curVer.replace(match.group(1), str(newVer+1).zfill(3))
                    splitted[-1] = replaced
                    self._file_path = os.path.join(item_path, '_'.join(splitted)).replace("\\", "/")
                    nuke.scriptSaveAs(self._file_path)
                    print 'Script renamed to %s' % self._file_path

    def load_last(self, full_path):
        item_path = full_path.rsplit("/", 1)[0]
        item_text = full_path.rsplit("/", 1)[1]
        print "LOAD LAST", full_path
        print 'SISI'
        if os.path.isfile(full_path):
            if full_path[-2:] == "nk":
                self.loader_preferences(save=True)
                self._file_path = os.path.join(item_path, item_text).replace("\\", "/")
                self.close()
                nuke.scriptOpen(os.path.join(item_path, item_text).replace('\\', '/'))
                nuke.tprint('setup_scene %s' % os.path.split(item_path)[-1])
                self.setup_scene()  # os.path.split(item_path)[-1]

                user = os.environ['COMPUTERNAME'].lower()

                modifiers = QApplication.keyboardModifiers()
                if user not in self._file_path and modifiers == Qt.ShiftModifier:
                    # checks if scripts is named by another person. If so - ask window will pop up
                    splitted = item_text.split('_')
                    splitted[-2] = user
                    curVer = splitted[-1]
                    match = re.match(r'v(\d*)', curVer)
                    newVer = get_last_version(path=item_path, filter=user)
                    replaced = curVer.replace(match.group(1), str(newVer + 1).zfill(3))
                    splitted[-1] = replaced
                    self._file_path = os.path.join(item_path, '_'.join(splitted)).replace("\\", "/")
                    nuke.scriptSaveAs(self._file_path)
                    print 'Script renamed to %s' % self._file_path
                    # nuke.tprint(self._file_path)



    # SAVE SCENE AS NEW
    def save_new_asset(self):
        self.listWidget_files.clearSelection()
        #print "ENTER EVENT TO NEW ASSET"
        name = self.new_asset.le_assetName.text()
        user = os.environ['COMPUTERNAME'].lower()
        v_ext = "v001.nk"



        if self.cbox_sequence.currentText() == "assetBuilds":
            file_name = '_'.join([name, user, v_ext])
            path = "/".join([self._storage,
                             self.cbox_project.currentText(),
                             self.cbox_sequence.currentText(),
                             self.cbox_type.currentText().lower(),
                             name])
        else:
            file_name = '_'.join([self.cbox_sequence.currentText(), self.cbox_shot.currentText(), name, user, v_ext])
            massPath = [self._storage, self.cbox_project.currentText(), "sequences",
                        self.cbox_sequence.currentText(), self.cbox_shot.currentText(),
                        self.cbox_type.currentText().lower(), name]
            print "MASS PATH: ", massPath
            path = "/".join(massPath)

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                "PATH CREATE ERROR"

        if not os.path.exists(path+'/precomp'):
            os.makedirs(path+'/precomp')

        full_path = os.path.join(path, file_name).replace("\\", "/")
        #nuke.tprint(full_path)

        self.setup_scene() #self.new_asset.le_assetName.text()
        nuke.scriptSaveAs(full_path)
        self.new_asset.close()
        self.close()

    # SAVE SCENE TO EXISTING
    def save_scene(self, exists=False):
        item_path = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).path
        item_text = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        item_type = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).type
        item_date = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).date

        #nuke.tprint('%s\n%s\n%s\n%s' % (item_path, item_text, item_type, item_date))

        path = os.path.join(item_path, item_text)
        user = os.environ['COMPUTERNAME'].lower()
        version = get_last_version(path)
        fileName = "_".join([self.cbox_sequence.currentText(), self.cbox_shot.currentText(), item_text, user, "v"+str(version+1).zfill(3)+".nk"])

        full_path = os.path.join(path, fileName).replace("\\", "/")
        nuke.root()['assetName'].setValue(item_text)
        self.setup_scene()
        nuke.scriptSaveAs(full_path)
        self.close()

    def setup_scene(self):
        project_settings = {}

        project = self.cbox_project.currentText()
        seq = self.cbox_sequence.currentText()
        shot = self._shot
        nuke.tprint(self.listWidget_files.currentItem()) #shot asset file
        if self.listWidget_files.itemWidget(self.listWidget_files.currentItem()) and self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).folder_type == 'asset':
            # if folder type is selected
            nuke.tprint('folder selected. Text is %s' % str(self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text))
            assetName = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text
        elif self.listWidget_files.itemWidget(self.listWidget_files.currentItem()) and '.nk' in self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text:
            # script opened via double clicking
            nuke.tprint('double click')
            assetName = self.listWidget_files.itemWidget(self.listWidget_files.currentItem()).text.split('_')[2]
        else:
            nuke.tprint('nothing is selected')
            assetName = self.new_asset.le_assetName.text()
        #nuke.tprint('setup_scene: assetname %s' % assetName)

        drive = self._storage
        root = nuke.root()
        pd = projectDict(project)

        first_frame = pd.getSpecificShotData(seq, shot, 'first_frame')
        last_frame = pd.getSpecificShotData(seq, shot, 'last_frame')

        # print '%s %s %s %s' % (seq, shot, first_frame, last_frame)

        # Cleaning the nodes except Viewers
        # for i in [e for e in nuke.allNodes() if e.Class() != 'Viewer']:
        #     nuke.delete(i)

        # SHOT STUFF
        root['lock_range'].setValue(True)
        root['fps'].setValue(24)
        root['format'].setValue('PL 3k')
        root['first_frame'].setValue(int(first_frame))
        root['last_frame'].setValue(int(last_frame))

        root['colorManagement'].setValue('OCIO')
        root['OCIO_config'].setValue('custom')
        root['customOCIOConfigPath'].setValue('X:/app/win/Pipeline/nuke/lib/aces_1.0.3/config.ocio')

        # PIPELINE STUFF
        attachTab(nuke.root(), 'PIPELINE')
        attachStringAttr('project', project, enabled=False)
        attachStringAttr('seq', seq, enabled=False)
        attachStringAttr('shot', shot, enabled=False)
        if assetName:
            #nuke.tprint('setting assetName to %s' % assetName)
            attachStringAttr('assetName', assetName, enabled=False)
        else:
            nuke.message('No assetName was found. This is an error of some kind')

        nuke.tprint('%s -- %s -- %s -- %s' % (project, seq, shot, assetName))

        #PL_writesCreate.createHiresWrite()
        #PL_writesCreate.createPreviewWrite()

        #pathToSave = '%s/%s/sequences/%s/%s/comp/%s/%s_%s_%s_%s_v001.nk' % (drive, project, seq, shot, assetName, seq, shot, assetName, os.environ['COMPUTERNAME'].lower())
        #dirName = os.path.dirname(pathToSave)
        #nuke.message(pathToSave)

    # def get_last_version(self, path, filter = None):
    #     if filter:
    #         list = [i for i in os.listdir(path) if filter in i]
    #     else:
    #         list = os.listdir(path)
    #
    #     if len(list) == 0:
    #         #no saves found
    #         return 0
    #     files = []
    #     versions = []
    #
    #     for f in list:
    #         ff = os.path.join(path, f).replace("\\", "/")
    #         #nuke.tprint(ff)
    #         if os.path.isfile(ff):
    #             files.append(f)
    #
    #     for f in files:
    #         if "~" in f or '.autosave' in f:
    #             pass
    #         else:
    #             match = re.match(r'(\w*)_(\w*)_v(\d*)', f)
    #             versions.append(int(match.group(3)))
    #
    #     versions = sorted(versions)
    #     #nuke.message(str(versions))
    #     return versions[-1] #integer type



if __name__ == '__main__':

    app = QApplication([])
    w=MayaManager()
    w.show()
    sys.exit(app.exec_())


