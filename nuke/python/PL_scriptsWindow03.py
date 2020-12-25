import math
import nuke
import os, sys
import glob

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import PySide.QtGui as QtGuiWidgets
from myWidgets import *

from PL_writesCreate import makePrecomp

from uis.scriptsWindow04_UI import Ui_Form

import LH
import nukescripts
import deleteFilesFromWrite
import rerenderMissingFrames
import scripts
import mirrorNodes
import W_scaleTree
import split_layers
import batchrenamer
import deepDefocusSlicer
import Points3DToTracker
import ExportAnimationFromEXR
import toolsets_loader

class scriptsWindow(QtGui.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(scriptsWindow, self).__init__(parent)
        self.setupUi(self)


# class scriptsWindow(QtGui.QWidget):
#     def __init__(self):
#         super(scriptsWindow, self).__init__()
        self.drive = 'P:'

        length = 4
        width = length * 200
        height = length * 100
        offset = QtCore.QPoint(width * 0.5, height * 0.5)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # self.masterLayout = QtGuiWidgets.QVBoxLayout(self)
        # self.masterLayout.setAlignment(QtCore.Qt.AlignLeft)
        # self.setLayout(self.masterLayout)

        self.button_width = 100 #width / length /100

        buttons = [self.flopflop, self.autocrop, self.viewerToRGBA, self.deleteWriteFiles, self.rerenderMissingFrames, self.lineupHorizontally, self.lineupVertically, self.toggleViewerInputs,
                  self.mirrorNodes, self.w_scaletree, self.glezin, self.batchRenamer, self.deepDefocusSlicer, self.normalize, self.copyTrackingDataToRoto, self.cameraFromExr, self.toolsetLoaderCreate]
        for b in buttons:
            print b.property('name')
            b.clicked.connect(self.executeScript, )

        # # DAILY BUTTON
        # self.buttonsLayout = QtGuiWidgets.QHBoxLayout()
        # buttondDaily = ScriptButtonWithGif(name = 'Dailies', script = 'import PL_dailiesMaker\nreload(PL_dailiesMaker)\nPL_dailiesMaker.makeDailyFromRead()', gifname = None, button_width = self.button_width)
        # buttondDaily.setMinimumWidth(130)
        # buttondDaily.setMaximumWidth(130)
        # buttondDaily.clicked.connect(self.executeScript, )
        # self.buttonsLayout.addWidget(buttondDaily)
        #
        # # CREATE HIRES WRITE
        # buttonCreateHires = ScriptButtonWithGif(name = 'Create Hires Write', script = 'import PL_writesCreate\nreload(PL_writesCreate)\nPL_writesCreate.createHiresWrite()', gifname = None, button_width = self.button_width)
        # buttonCreateHires.setMinimumWidth(130)
        # buttonCreateHires.setMaximumWidth(130)
        # buttonCreateHires.clicked.connect(self.executeScript, )
        # self.buttonsLayout.addWidget(buttonCreateHires)
        #
        # # CAMERA IMPORT
        # buttonImportCamera = ScriptButtonWithGif(name = 'Import Camera', script = 'import PL_cameraImporter\nreload(PL_cameraImporter)\nPL_cameraImporter.importCam()', gifname = None,  button_width = self.button_width)
        # buttonImportCamera.setMinimumWidth(130)
        # buttonImportCamera.setMaximumWidth(130)
        # buttonImportCamera.clicked.connect(self.executeScript, )
        # self.buttonsLayout.addWidget(buttonImportCamera)
        #
        # # ADDING FIRST LINE OF BUTTONS AND PRECOMP LAYOUT TO A MASTER LAYOUT
        # self.masterLayout.addLayout(self.buttonsLayout)

        pos = QtGui.QCursor.pos()
        self.adjustSize()
        self.move(pos.x() - self.width()/2, pos.y() - self.height()/2)

        # make sure the widgets closes when it loses focus
        self.installEventFilter(self)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def executeScript(self):
        # try:
        #     exec(self.sender().script)
        # except:
        #     print 'ERROR!'
        #help(self.sender())
        if QtGui.qApp.mouseButtons() & QtCore.Qt.RightButton:
            nuke.message('left click')
            self.close()
            self.destroy()
        else:
            exec (self.sender().property('script'))
            self.close()
            self.destroy()

    def keyPressEvent(self, e):
        #nuke.message('keyPressEvent')
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
            self.destroy()

    def keyReleaseEvent(self, e):
        pass

    def eventFilter(self, object, event):
        if event.type() in [QtCore.QEvent.WindowDeactivate, QtCore.QEvent.FocusOut]:
            self.close()
            self.destroy()
            return True

if __name__ == '__main__':

    app = QApplication([])
    w=scriptsWindow()
    w.show()
    sys.exit(app.exec_())
