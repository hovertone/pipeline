import os
import MUI.MaxUI as mui
reload (mui)
import PySide2.QtGui as qg
import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
import maya.cmds as cmds
import ConfigParser

class CharSet(qw.QDialog):

    def __init__(self):
        qw.QDialog.__init__(self)

        '''-------- Window --------'''

        mui.Window(W=self, Titel="Chracter Set", Width=215, Height=95)

        '''-------- UI --------'''

        mui.Label(W=self, Pos=[10, 10], Text="Name:")

        self.globalPath = os.environ.get('PLARIUM_MAYA_VERSION_TOOLS', '').replace("/", "\\")
        self.INIPath = self.globalPath + "\mTools\scripts\Tools\mRetarget\CharacterSet.ini"

        Config = ConfigParser.ConfigParser()
        Config.read(self.INIPath)
        CharName = Config.get("Char", "Name")

        self.SetName = mui.TextBox(W=self, Text=CharName, Pos=[10, 30], Width=195, Height=20)

        self.CreateBTN = mui.Button(W=self, Name="Create", Pos=[10, 60], Width=95, Height=25)
        self.CancelBTN = mui.Button(W=self, Name="Cancel", Pos=[110, 60], Width=95, Height=25)

        '''--------------------'''

        self.CreateBTN.clicked.connect(self.CreateCharacter)
        self.CancelBTN.clicked.connect(self.Close)

    def WrightINI(self):
        Config = ConfigParser.ConfigParser()
        Config.read(self.INIPath)
        File = open(self.INIPath, "w")
        Config.set("Char", "Name", self.SetName.text())
        Config.write(File)
        File.close()

    def CreateCharacter(self):
        Name = self.SetName.text()

        cmds.character(name=Name)

        cmds.select(clear=True)
        self.WrightINI()
        self.close()

    def Close(self):
        cmds.select(clear=True)
        self.close()

ChracterSet_dialog = CharSet()
ChracterSet_dialog.show()