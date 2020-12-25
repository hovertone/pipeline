# -*- coding: utf-8 -*-


try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os, sys
import nuke
import nukescripts
import json
from functools import partial
from houdini_app.AssetsLoader.ui.AssetsLib_v002_UIs import Ui_AssetsLib
from uis.toolsets_create_03_UIs import toolset_create_ui
from houdini_app.AssetsLoader.lib_item import AssetItem

path = "O:/compToolsets"

class toolsetCreate(QDialog, toolset_create_ui):
    def __init__(self, parent=None):
        super(toolsetCreate, self).__init__(parent)
        # if nuke.selectedNodes() == []:
        #     nuke.message('Select nodes, man!')
        #     return
        self.setupUi(self)

        self.PATH = "O:/compToolsets"

        # MENU FOLDERS
        menu_folders = [i for i in os.listdir(self.PATH) if '.' not in i]
        menu_folders.insert(0, 'root')
        self.cb_menuSection.addItems(menu_folders)

        # CONNECTS
        self.cb_menuSection.currentIndexChanged.connect(self.get_list)
        self.le_name.textChanged.connect(self.name_changed)
        self.pb_ok.clicked.connect(self.create_toolset)
        self.pb_cancel.clicked.connect(self.close)


    def get_list(self):
        #print 'get_list'
        pass

    def create_toolset(self):
        if self.le_name.text() == '':
            # nuke.message('Toolset has to be named. Fill name field.')
            # return
            t = QMessageBox(self)
            t.setText('Toolset has to be named. Fill name field.')
            t.show()
        else:
            section = self.cb_menuSection.currentText()
            name = self.le_name.text()
            description = self.pte_description.toPlainText()

            if '/' in name:
                folder, name = name.split('/')
                os.makedirs(os.path.join(self.PATH, folder).replace('\\', '/'))
            else:
                folder = section

            toolset_path = os.path.join(self.PATH, folder, name)
            try:
                nuke.nodeCopy(toolset_path + '.nk')
            except RuntimeError:
                t = QMessageBox(self)
                t.setText('Select some nodes please')
                t.show()
                return

            # THUMBNAIL PART
            clipboard = QApplication.clipboard()
            mimeData = clipboard.mimeData()
            if mimeData.hasImage():
                print 'saved with screenshot'
                i = clipboard.image()
                p = QPixmap(i)
                p.save(toolset_path + '.png', "png")
            else:
                print 'saved WITHOUT screenshot'

            #DESCRIPTION
            data = dict()
            with open(os.path.join(self.PATH, 'descriptions.json')) as json_file:
                data = json.load(json_file)
            data['%s_%s' % (folder, name)] = description

            with open(os.path.join(self.PATH, 'descriptions.json'), 'w') as write_file:
                json.dump(data, write_file)

            self.close()

    def getDescription(self, k):
        data = dict()
        with open(os.path.join(self.PATH, 'descriptions.json')) as json_file:
            data = json.load(json_file)
        if k in data.keys():
            return data[k]
        else:
            raise ValueError('There is no description with %s toolset' % k)

    def name_changed(self):
        if '/' in self.le_name.text():
            #print 'slash condition'
            self.cb_menuSection.setCurrentIndex(0)

        if self.cb_menuSection.currentIndex() != 0:
            section = self.cb_menuSection.currentText()
            path = os.path.join(self.PATH, section)
            toolsets = [i.strip('.nk') for i in os.listdir(path) if '.nk' in i]
            #print '%s' % toolsets
            if self.le_name.text() in toolsets:
                self.le_name.setStyleSheet("color: rgb(255, 201, 0);")
                self.le_name.setToolTip('Name is already in use. The toolset will be overriden.')
                self.pte_description.setPlainText(self.getDescription('%s_%s' % (section, self.le_name.text())))
            else:
                self.le_name.setStyleSheet("color: rgb(122, 122, 122);")
                self.le_name.setToolTip('English text only. This name is not in use.')

class AssetsLoader(QDialog, Ui_AssetsLib):
    def __init__(self, parent=None):
        super(AssetsLoader, self).__init__(parent)
        self.setupUi(self)
        #AssetsLoader.setObjectName("Toolset Browser")
        self.hSlider_zoom.setValue(200)
        self.path = path

        self.cbox_category.clear()
        toolsetFolders = [i for i in os.listdir(self.path) if '.' not in i and '_tech' not in i]
        print toolsetFolders
        for i, f in enumerate(toolsetFolders[::-1]):
            print i, f
            print self.cbox_category.insertItem(0, f)

        self.cbox_category.currentIndexChanged.connect(self.get_list)
        self.hSlider_zoom.valueChanged.connect(self.slider_value)
        self.le_search.textChanged.connect(self.search_action)

        self.get_list()


    def get_list(self):
        self.listWidget_lib.clear()
        path = os.path.join(self.path, self.cbox_category.currentText()).replace("\\", "/")
        list = os.listdir(path)
        files = []

        for l in list:
            if l[-2:] == "nk":
                files.append(l)

        for f in files:
            model = AssetItem(path=path, text=f, type=self.cbox_category.currentText())
            model.pb_load.clicked.connect(partial(self.itemAction, model.lb_text.text()))
            listItem = QListWidgetItem()
            self.listWidget_lib.addItem(listItem)
            listItem.setSizeHint(QSize(self.hSlider_zoom.value(), self.hSlider_zoom.value()))
            self.listWidget_lib.setItemWidget(listItem, model)


    def itemAction(self, text):
        print text
        #net_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
        #parent = net_editor.pwd()
        nuke.loadToolset("%s/%s/%s.nk" % (self.path, self.cbox_category.currentText(), text))


    def slider_value(self):
        value = self.hSlider_zoom.value()
        for i in range(self.listWidget_lib.count()):
            self.listWidget_lib.item(i).setSizeHint(QSize(value, value))


    def search_action(self):
        text = self.le_search.text()
        self.get_list()
        if len(text) > 0:
            if self.listWidget_lib.count() > 0:
                for i in range(self.listWidget_lib.count()):
                    if text in self.listWidget_lib.itemWidget(self.listWidget_lib.item(i)).text:
                        pass
                    else:
                        self.listWidget_lib.takeItem(self.listWidget_lib.row(self.listWidget_lib.item(i)))
        else:
            self.get_list()

# def addToolset():
#     if nuke.selectedNodes() == []:
#         nuke.message('No nodes has been selected.')
#         return


if __name__ == '__main__':

    app = QApplication([])
    w=toolsetCreate()
    w.show()
    sys.exit(app.exec_())
