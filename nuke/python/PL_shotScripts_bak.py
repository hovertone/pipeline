import math
import nuke
import os, sys
import glob

import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
import PySide.QtGui as QtGuiWidgets
from myWidgets import *
from functools import partial
from PL_writesCreate import makePrecomp

class shotScripts(QtGui.QWidget):
    def __init__(self):
        super(shotScripts, self).__init__()
        self.drive = 'P:'

        length = 4
        width = length * 200
        height = length * 100
        offset = QtCore.QPoint(width * 0.5, height * 0.5)

        #self.setMinimumSize(width, height)
        #self.setMaximumSize(width, height)

        #point = QtGui.QCursor.pos()
        #self.move(point)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.masterLayout = QtGuiWidgets.QVBoxLayout(self)
        self.masterLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(self.masterLayout)

        self.button_width = 100 #width / length /100

        # DAILY BUTTON
        self.buttonsLayout = QtGuiWidgets.QHBoxLayout()
        buttondDaily = ScriptButtonWithGif(name = 'Dailies', script = 'import PL_dailiesMaker\nreload(PL_dailiesMaker)\nPL_dailiesMaker.masterDaily()', gifname = None, button_width = self.button_width)
        buttondDaily.setMinimumWidth(130)
        buttondDaily.setMaximumWidth(130)
        buttondDaily.clicked.connect(self.executeScript, )
        self.buttonsLayout.addWidget(buttondDaily)

        # CREATE HIRES WRITE
        buttonCreateHires = ScriptButtonWithGif(name = 'Create Hires Write', script = 'import PL_writesCreate\nreload(PL_writesCreate)\nPL_writesCreate.createHiresWrite()', gifname = None, button_width = self.button_width)
        buttonCreateHires.setMinimumWidth(130)
        buttonCreateHires.setMaximumWidth(130)
        buttonCreateHires.clicked.connect(self.executeScript, )
        self.buttonsLayout.addWidget(buttonCreateHires)

        # CAMERA IMPORT
        buttonImportCamera = ScriptButtonWithGif(name = 'Import Camera', script = 'import PL_cameraImporter\nreload(PL_cameraImporter)\nPL_cameraImporter.importCam()', gifname = None,  button_width = self.button_width)
        buttonImportCamera.setMinimumWidth(130)
        buttonImportCamera.setMaximumWidth(130)
        buttonImportCamera.clicked.connect(self.executeScript, )
        self.buttonsLayout.addWidget(buttonImportCamera)

        # PRECOMP GROUP
        self.precompFrame = QtGui.QGroupBox('PRECOMP')
        # self.precompLayout = QtGuiWidgets.QVBoxLayout()
        # self.precompLayout.setAlignment(QtCore.Qt.AlignLeft)

        # LINE EDIT FOR PRECOMP
        self.precompLayout = QtGuiWidgets.QHBoxLayout()
        self.lineEdit = QtGuiWidgets.QLineEdit()
        self.lineEditForm = QtGuiWidgets.QFormLayout()
        self.lineEditForm.addRow('NAME', self.lineEdit)
        self.precompLayout.addLayout(self.lineEditForm)
        self.precompFrame.setLayout(self.precompLayout)

        self.combobox = QtGuiWidgets.QComboBox()
        self.combobox.addItems(['.exr', '.exr Alpha', '.exr All', '.jpg', '.png Alpha'])
        self.precompLayout.addWidget(self.combobox)

        self.switch_check = QtGuiWidgets.QCheckBox()
        self.switch_check.setText('Switch')
        self.switch_check.setToolTip('Make a write with a switch, read node and the backdrop')
        self.precompLayout.addWidget(self.switch_check)

        self.precompCreateButton = ScriptButtonWithGif('Create', None, None, 150)
        #self.precompCreateButton = QtGuiWidgets.QPushButton('PTSHHH!')
        i = 20
        self.precompCreateButton.setMaximumHeight(i)
        self.precompCreateButton.setMinimumHeight(i)
        self.precompCreateButton.clicked.connect(self.createPrecomp, )
        self.precompLayout.addWidget(self.precompCreateButton)

        # RENAME SCRIPT WITH MY NAME
        self.buttons2Layout = QtGuiWidgets.QHBoxLayout()
        renameScriptButton = ScriptButtonWithGif(name='Rename Script',
                                           script='import PL_scripts\nreload(PL_scripts)\nPL_scripts.renameScriptWithMyName()',
                                           gifname=None, button_width=self.button_width)
        renameScriptButton.setMinimumWidth(130)
        renameScriptButton.setMaximumWidth(130)
        renameScriptButton.clicked.connect(self.executeScript, )
        self.buttons2Layout.addWidget(renameScriptButton)

        # ADDING FIRST LINE OF BUTTONS AND PRECOMP LAYOUT TO A MASTER LAYOUT
        self.masterLayout.addLayout(self.buttonsLayout)
        #self.masterLayout.addLayout(self.precompLayout)
        self.masterLayout.addWidget(self.precompFrame)
        self.masterLayout.addLayout(self.buttons2Layout)
        nuke.tprint('hehehheehehe')

        pos = QtGui.QCursor.pos()
        self.adjustSize()
        self.move(pos.x() - self.width()/2, pos.y() - self.height()/2)

        # make sure the widgets closes when it loses focus
        self.installEventFilter(self)

    def createPrecomp(self):
        precompName = self.lineEdit.text()
        precompType = self.combobox.currentText()
        makePrecomp(precompName, precompType, self.switch_check.isChecked())
        self.close()

    def executeScript(self):
        exec (self.sender().script)
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
