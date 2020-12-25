import math
import nuke
import os, sys
import glob
import socket
import re

from p_utils.csv_parser_bak import projectDict
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import PySide.QtGui as QtGuiWidgets

class LayerButton(QtGuiWidgets.QPushButton):
    def __init__(self, name, button_width, parent=None):
        super(LayerButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.setText(name)
        self.setMinimumWidth(button_width / 2)
        self.regular_color = "background-color:#282828; font: 13px"
        self.orange_color = "background-color:#C26828; font: 13px"
        self.green_color = "background-color: #1EB028; font: 13px"
        self.setStyleSheet(self.regular_color)

    def enterEvent(self, event):
        if not self.styleSheet() == self.green_color:
            self.setStyleSheet(self.orange_color)

    def leaveEvent(self, event):
        if not self.styleSheet() == self.green_color:
            self.setStyleSheet(self.regular_color)


class ShotButton(LayerButton):
    def __init__(self, name, project, seq, button_width, parent=None):
        super(ShotButton, self).__init__(name, button_width, parent)
        self.project = project
        self.seq = seq

class LineEdit(QtGuiWidgets.QLineEdit):
    def __init__(self, parent, layer_list):
        super(LineEdit, self).__init__(parent)
        self.parent = parent
        layer = [i for i in layer_list]
        self.completerList = []
        self.completer = QtGuiWidgets.QCompleter(layer, self)
        self.completer.setCompletionMode(QtGuiWidgets.QCompleter.InlineCompletion)
        self.setCompleter(self.completer)
        self.completer.activated.connect(self.returnPressed)

class Label(QtGuiWidgets.QLabel):
    def __init__(self, label):
        super(Label, self).__init__()
        #self.


class shotOpener(QtGuiWidgets.QWidget):
    def __init__(self):
        super(shotOpener, self).__init__()
        self.drive = 'P:'

        #av = nuke.activeViewer().node()
        #vn = av.input(nuke.activeViewer().activeInput())

        #layer = list(set([c.split('.')[0] for c in vn.channels()]))
        #layer.sort()

        length = 4
        width = length * 200
        height = length * 100
        offset = QtCore.QPoint(width * 0.5, height * 0.5)
        #self.setMinimumSize(width, height)
        #self.setMaximumSize(width, height)

        point = QtGui.QCursor.pos() - offset
        self.move(point)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        i = 10
        #self.setContentsMargins(i, i, i, i)

        self.masterLayout = QtGuiWidgets.QVBoxLayout(self)
        self.masterLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(self.masterLayout)

        self.button_width = width / length /100
        #self.fillShotsPartFromProject('rnd')

        self.users = ['sashok', 'jenya', 'alex', 'andr', 'gleb', 'kolya', 'marik', 'paul', 'pc-097', 'vavs']
        #self.fillShotsPartFromProject('Arena')
        self.fillShotsPartFromProject('Raid')

    def fillShotsPartFromProject(self, project):
        self.projectFrame = QtGui.QGroupBox(project)
        self.projectLayout= QtGuiWidgets.QVBoxLayout()
        self.projectLayout.setAlignment(QtCore.Qt.AlignLeft)

        self.d = projectDict(project)
        for seq in sorted(self.d.getSequences()):
            if 'previz' in seq:
                break
            self.seqFrame = QtGui.QGroupBox(seq)
            self.seqLayout = QtGuiWidgets.QGridLayout()
            self.row, self.column = 0, 0
            for i, shot in enumerate(self.d.getShots(seq)):
                button = ShotButton(shot, project, seq, 0)
                button.setMinimumWidth(130)
                button.setMaximumWidth(130)
                button.clicked.connect(self.openShotScript, )
                self.seqLayout.addWidget(button, self.row, self.column)
                self.seqLayout.setAlignment(QtCore.Qt.AlignLeft)
                if (i+1)%5 == 0:
                    self.row += 1
                    self.column = 0
                else:
                    self.column += 1

            self.seqFrame.setLayout(self.seqLayout)
            self.projectLayout.addWidget(self.seqFrame)

        self.projectFrame.setLayout(self.projectLayout)
        self.masterLayout.addWidget(self.projectFrame)

        self.installEventFilter(self)

    def keyPressEvent(self, e):
        #nuke.message('keyPressEvent')
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def keyReleaseEvent(self, e):
        pass

    def listUsersAndSaves(self, search_dir):
        files = filter(os.path.isfile, glob.glob(search_dir + "*"))
        onlyNKfiles = [i for i in files if '~' not in i and '.autosave' not in i and '.nk' in i]
        usersAndVersions = dict()
        for u in self.users:
            userFiles = []
            files = filter(os.path.isfile, glob.glob(search_dir + "*%s*.nk" % u))
            if files != []:
                files.sort(key=lambda x: os.path.getmtime(x))
                #nuke.message(str(files[-1]))
                usersAndVersions[u] = files[-1]

        return usersAndVersions

    def openShotScript(self):
        #nuke.message(self.sender().project + self.sender().text())
        self.shot = self.sender().text()
        self.project = self.sender().project
        self.seq = self.sender().seq
        os.environ["SHOT"] = '%s/%s/sequences/%s/%s' % (self.drive, self.project, self.seq, self.shot)
        os.environ["SN"] = self.shot
        user = socket.gethostname()

        search_dir = '%s/%s/sequences/%s/%s/comp/' % (self.drive, self.project, self.seq, self.shot)
        files = filter(os.path.isfile, glob.glob(search_dir + "*"))
        onlyNKfiles = [i for i in files if '~' not in i and '.autosave' not in i and '.nk' in i]
        onlyNKfiles.sort(key=lambda x: os.path.getmtime(x))

        usersAndSaves = self.listUsersAndSaves(search_dir)
        keys = usersAndSaves.keys()
        if len(keys) == 1:
            #if only one user saves exists
            wantedUser = keys[0]
            nuke.scriptOpen(usersAndSaves[keys[0]])
        else:
            # multiuser saves exist
            p = nuke.Panel('Which user save you want to open?')
            for i, k in enumerate(keys):
                p.addButton(k)
            ret = p.show()
            wantedUser = keys[ret]

            nuke.scriptOpen(usersAndSaves[wantedUser])

        if wantedUser != user:
            curPath = usersAndSaves[wantedUser]
            if user not in keys:
                ver = 1
            else:
                files = filter(os.path.isfile, glob.glob(search_dir + "*"))
                userNKs = [i for i in files if '~' not in i and '.autosave' not in i and '.nk' in i and user in i]
                userNKs.sort()
                lastSave = os.path.split(userNKs[-1])[-1]

                res = re.match(r'(\w*)_(\w*)_v(\d*)', lastSave)
                ver = int(res.group(3)) + 1
            #nuke.message(str(ver))
            newPath = curPath.replace(wantedUser, user)
            newPath = newPath[:newPath.index('_v')] + '_v%s.nk' % str(ver).zfill(3)
            nuke.scriptSaveAs(newPath)
        # if user in onlyNKfiles[-1]:
        #     # last saved .nk file contains current user name
        #     print 'last save is ours save'
        # else:
        #     # last save has a different from our current user name
        #     # ask which user name we wan't to open
        #     print self.listUsersFromSave(search_dir)

        #nuke.message(onlyNKfiles[-1])

        #nuke.scriptOpen(onlyNKfiles[-1])
        #nuke.root()['fps'].setValue(24)
        #print 'SUCCESS. Opening %s %s' % (seq, shot)
        self.close()

    def clicked(self):
        nuke.message(self.sender().text())
        self.close()


    def line_enter(self):
        nuke.activeViewer().node()['channels'].setValue(self.input.text())
        self.close()

    def eventFilter(self, object, event):
        if event.type() in [QtCore.QEvent.WindowDeactivate, QtCore.QEvent.FocusOut]:
            self.close()
            return True

if __name__ == '__main__':

    app = QtGui.QApplication([])
    w=shotOpener()
    w.show()
    sys.exit(app.exec_())

