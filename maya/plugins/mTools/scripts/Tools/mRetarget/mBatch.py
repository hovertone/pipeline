import os
import glob
import maya.cmds as cmds
import maya.mel as mel
import MUI.MaxUI as mui
reload(mui)
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import ConfigParser

class mBatch(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        self.globalPath = os.environ.get('PLARIUM_MAYA_VERSION_TOOLS', '').replace("/", "\\")
        self.INIPath = self.globalPath + "\mTools\scripts\Tools\mRetarget\mBatch.ini"

        '''-------- Window --------'''

        mui.Window(W=self, Titel="FBX Batch", Width=270, Height=140)

        '''---------- UI ----------'''

        Config = ConfigParser.ConfigParser()
        Config.read(self.INIPath)
        RawPathString = Config.get("Raw", "Path")
        ClearPathString = Config.get("Clear", "Path")

        mui.GroupeBox(W=self, Name="Raw Folder", Pos=[5, 5], Height=60, Width=260)
        self.RawFolderBTN = mui.Button(W=self, Pos=[10, 20], Height=20, Width=30, IPath=self.globalPath + "\mTools\scripts\Tools\mRetarget\Images\Open_Folder_20px.png")
        self.RawFolderTB = mui.TextBox(W=self, Pos=[40, 20], Height=20, Width=220, Text=RawPathString)
        self.MultiFolder = mui.CheckBox(W=self, Pos=[10,45], Name="Use Folder Structure", State=False,)

        mui.GroupeBox(W=self, Name="Clear Folder", Pos=[5, 65], Height=40, Width=260)
        self.ClearFolderBTN = mui.Button(W=self, Pos=[10, 80], Height=20, Width=30, IPath=self.globalPath + "\mTools\scripts\Tools\mRetarget\Images\Open_Folder_20px.png")
        self.ClearFolderTB = mui.TextBox(W=self, Pos=[40, 80], Height=20, Width=220, Text=ClearPathString)

        self.RunBTN = mui.Button(W=self, Pos=[5, 110], Height=25, Width=260, Name="Run")

        '''------------- Button Connects -------------'''

        self.RawFolderBTN.clicked.connect(self.OpenRawFolder)
        self.ClearFolderBTN.clicked.connect(self.OpenClearFolder)
        self.RunBTN.clicked.connect(self.RunBatch)

        '''-------------------------------------------'''

    def OpenRawFolder(self):
        Config = ConfigParser.ConfigParser()
        Config.read(self.INIPath)
        RawPathString = Config.get("Raw", "Path")

        Folder = str(cmds.fileDialog2(dir=RawPathString, dialogStyle=1, fileMode=3)[0])
        self.RawFolderTB.setText(Folder)

        self.WriteINI()

    def OpenClearFolder(self):
        Config = ConfigParser.ConfigParser()
        Config.read(self.INIPath)
        ClearPathString = Config.get("Clear", "Path")

        Folder = str(cmds.fileDialog2(dir=ClearPathString, dialogStyle=1, fileMode=3)[0])
        self.ClearFolderTB.setText(Folder)

        self.WriteINI()

    def makeDir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def ClearAll(self):

        cmds.select(deselect=True)
        Joints = cmds.ls(type="joint", l=True)

        '''---Get Time---'''

        theStart = int(cmds.playbackOptions(query=True, animationStartTime=True))
        theEnd = int(cmds.playbackOptions(query=True, animationEndTime=True))

        cmds.playbackOptions(animationStartTime=theStart, min=theStart, animationEndTime=theEnd, max=theEnd)

        cmds.currentTime(theStart)

        '''---Bake All---'''

        for i in range(len(Joints)):
            cmds.bakeResults(Joints[i] + ".translateX", t=(theStart, theEnd))
            cmds.bakeResults(Joints[i] + ".translateY", t=(theStart, theEnd))
            cmds.bakeResults(Joints[i] + ".translateZ", t=(theStart, theEnd))

            cmds.bakeResults(Joints[i] + ".rotateX", t=(theStart, theEnd))
            cmds.bakeResults(Joints[i] + ".rotateY", t=(theStart, theEnd))
            cmds.bakeResults(Joints[i] + ".rotateZ", t=(theStart, theEnd))

        '''---Create Roots---'''

        '''--- Probs ---'''

        index = 0

        for i in range(len(Joints)):
            nName = Joints[i]
            namePath = nName.split("|")

            if namePath[len(namePath) - 1].find("root") != -1:

                filterPath = namePath[1].split(":")[0]

                index += 1
                pName = cmds.rename(nName, "root_" + str(index))

                rootName = "Blade_" + filterPath
                rootJoint = cmds.joint(n=rootName, p=(0, 0, 0))

                cmds.parent(pName, rootJoint)

                cmds.select(deselect=True)

        '''--- Characters ---'''

        characters = cmds.ls( 'Hips', l = True)

        for i in range(len(characters)):
            namePath = characters[i].split("|")

            rootName = "Blade_" + namePath[1]

            rootJoint = cmds.joint(n=rootName, p=(0, 0, 0))
            cmds.parent(characters[i], rootJoint)

            charNodes = cmds.listRelatives(rootJoint, ad=True, f=True)

            for j in range(len(charNodes)):
                charJoint = charNodes[j]
                splitJointName = charJoint.split("|")

                charJointName = namePath[1] + "_" + splitJointName[len(splitJointName) - 1]
                cmds.rename(charJoint, charJointName)

            cmds.select(deselect=True)

        '''---Delete Locators and Gabidge---'''

        Locators = cmds.ls(type="locator")

        for i in range(len(Locators)):
            try:
                PL = cmds.listRelatives(Locators[i], p=True)
                cmds.delete(PL)
            except:
                pass

        #cmds.createDisplayLayer(name="FBX_Clean")

    def RunBatch(self):
        RootPath = self.RawFolderTB.text()
        DestinationPath = self.ClearFolderTB.text()

        if self.MultiFolder.isChecked() == True:

            RootFolderName = os.path.basename(RootPath)
            DestinationFolder = DestinationPath + "\\" + RootFolderName

            self.makeDir(DestinationFolder)

            for folderName in os.listdir(RootPath):
                RDir = RootPath + "\\" + folderName
                RawFBX = glob.glob(RDir + "\\" + "*.fbx")

                DDir = DestinationFolder + "\\" + folderName
                self.makeDir(DDir)

                for file in RawFBX:
                    cmds.file(new=True, f=True)

                    cmds.file(file, i=True, type="FBX", importTimeRange="override")

                    CharArray = cmds.ls(["Hips*", "root*"], tr=True)
                    cmds.select(CharArray, r=True)

                    cmds.currentUnit(t="film")
                    self.ClearAll()

                    Name = os.path.basename(file).rsplit(".", 1)[0]

                    fileName = (DDir + "\\" + Name).replace("\\", "/")
                    mel.eval('FBXExport -f "' + fileName + '"')
        else:
            RawFBX = glob.glob(RootPath + "\\" + "*.fbx")

            for file in RawFBX:
                cmds.file(new=True, f=True)

                cmds.file(file, i=True, type="FBX", importTimeRange="override")

                CharArray = cmds.ls(["Hips*", "root*"], tr=True)
                cmds.select(CharArray, r=True)

                cmds.currentUnit(t="film")
                self.ClearAll()

                Name = os.path.basename(file).rsplit(".", 1)[0]

                fileName = (DestinationPath + "\\" + Name).replace("\\", "/")
                mel.eval('FBXExport -f "' + fileName + '"')

    def WriteINI(self):
        Config = ConfigParser.ConfigParser()
        Config.read(self.INIPath)
        File = open(self.INIPath, "w")
        Config.set("Raw", "Path", self.RawFolderTB.text())
        Config.set("Clear", "Path", self.ClearFolderTB.text())
        Config.write(File)
        File.close()

    def closeEvent(self, event):
        self.WriteINI()

mBatch_Dialog = mBatch()
mBatch_Dialog.show()