import MUI.MaxUI as mui
reload (mui)
import PySide2.QtGui as qg
import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
import maya.cmds as cmds

class QSSet(qw.QDialog):

    def __init__(self):
        qw.QDialog.__init__(self)

        '''-------- Window --------'''

        mui.Window(W=self, Titel="Selection Set", Width=315, Height=95)

        '''-------- UI --------'''

        mui.Label(W=self, Pos=[10, 10], Text="Enter Quick Select Set name:")
        self.SetName = mui.TextBox(W=self, Text="Set", Pos=[10, 30], Width=295, Height=20)

        self.QSBTN = mui.Button(W=self, Name="Quick Set", Pos=[10, 60], Width=95, Height=25)
        self.SSBTN = mui.Button(W=self, Name="Selection Set", Pos=[110, 60], Width=95, Height=25)
        self.CancelBTN = mui.Button(W=self, Name="Cancel", Pos=[210, 60], Width=95, Height=25)

        '''--------------------'''

        self.QSBTN.clicked.connect(self.QSS)
        self.SSBTN.clicked.connect(self.SS)
        self.CancelBTN.clicked.connect(self.Close)

    def QSS(self):
        Name = self.SetName.text()

        obj = cmds.ls(sl=1)
        cmds.select(obj)
        cmds.sets(name=Name, text="gCharacterSet")

        cmds.select(clear=True)
        self.close()

    def SS(self):
        Name = self.SetName.text()

        obj = cmds.ls(sl=1)
        cmds.select(obj)
        cmds.sets(name=Name)

        cmds.select(clear=True)
        self.close()

    def Close(self):
        cmds.select(clear=True)
        self.close()

QSSet_dialog = QSSet()
QSSet_dialog.show()