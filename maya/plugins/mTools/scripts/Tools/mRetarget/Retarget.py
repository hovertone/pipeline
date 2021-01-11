import MUI.MaxUI as mui
reload (mui)
import PySide2.QtGui as qg
import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os
import sys
import ConfigParser


def SetControl(Side, BTNL, BTNR, Bone, Index , LArray, RArray):

    if Side == "L":
        if Bone != None and RArray[Index] == None:
            BTNL.setStyleSheet("QPushButton{background-color: rgba(200,200,0,255);}")
            BTNL.setToolTip(Bone)
            LArray[Index] = Bone
        else:
            if RArray[Index] != None:
                BTNL.setStyleSheet("QPushButton{background-color: rgba(0,200,0,255);}")
                BTNR.setStyleSheet("QPushButton{background-color: rgba(0,200,0,255);}")
                BTNL.setToolTip(Bone)
                LArray[Index] = Bone
    else:
        if Bone != None and LArray[Index] == None:
            BTNR.setStyleSheet("QPushButton{background-color: rgba(200,200,0,255);}")
            BTNR.setToolTip(Bone)
            RArray[Index] = Bone
        else:
            if LArray[Index] != None:
                BTNR.setStyleSheet("QPushButton{background-color: rgba(0,200,0,255);}")
                BTNL.setStyleSheet("QPushButton{background-color: rgba(0,200,0,255);}")
                BTNR.setToolTip(Bone)
                RArray[Index] = Bone

def RemoveControl(Side, BTNL, BTNR, Index, LArray, RArray):
    if Side == "L":
        LArray[Index] = None
        BTNL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        if RArray[Index] != None:
            BTNR.setStyleSheet("QPushButton{background-color: rgba(255,255,0,255);}")
    else:
        RArray[Index] = None
        BTNR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        if LArray[Index] != None:
            BTNL.setStyleSheet("QPushButton{background-color: rgba(255,255,0,255);}")

def GetName():
    try:
        Sel = cmds.ls(sl=True)[0]
        Bone = Sel.split("|")[-1]
    except:
        Bone = None

    return Bone

class MRetarget(qw.QDialog):

    def __init__(self):
        qw.QDialog.__init__(self)

        '''-------- Window --------'''

        mui.Window(W=self, Titel="mRetarget", Width=325, Height=330)

        '''-------- Top Menu --------'''

        self.FileBTN = mui.Button(W=self, Name="File", Pos=[0,0], Width=83, Height=20)
        self.IKFKBTN = mui.Button(W=self, Name="IK | FK", Pos=[83, 0], Width=82, Height=20)
        self.ToolsBTN = mui.Button(W=self, Name="Tools", Pos=[165,0], Width=82, Height=20)

        self.FileMenu = qw.QMenu()
        self.MISaveFile = self.FileMenu.addAction("Save Map File")
        self.MIOpenFile = self.FileMenu.addAction("Open Map File")
        self.SepReset = self.FileMenu.addSeparator()
        self.MIReset = self.FileMenu.addAction("Reset Map")
        self.FileBTN.setMenu(self.FileMenu)

        self.IKFKMenu = qw.QMenu()
        self.ArmsMenu = self.IKFKMenu.addMenu("Arms")
        self.ArmsFK = qw.QAction("FK", self.ArmsMenu, checkable=True, checked=True)
        self.ArmsMenu.addAction(self.ArmsFK)
        self.ArmsIK = qw.QAction("IK", self.ArmsMenu, checkable=True)
        self.ArmsMenu.addAction(self.ArmsIK)
        self.LegsMenu = self.IKFKMenu.addMenu("Legs")
        self.LegsFK = qw.QAction("FK", self.LegsMenu, checkable=True)
        self.LegsMenu.addAction(self.LegsFK)
        self.LegsIK = qw.QAction("IK", self.LegsMenu, checkable=True, checked=True)
        self.LegsMenu.addAction(self.LegsIK)
        self.IKFKBTN.setMenu(self.IKFKMenu)

        self.ToolsMenu = qw.QMenu()
        self.ToolsMenu.tearOffEnabled = 1
        self.ToolsMenu.setTearOffEnabled(1)
        self.ToolsMenu.setWindowTitle("Tools")

        '''self.Sep = qw.QWidgetAction(self)
        self.label = qw.QLabel(self)
        self.label.setFixedHeight(0)
        self.Sep.setDefaultWidget(self.label)
        self.ToolsMenu.addAction(self.Sep)'''

        self.CharSetup = self.ToolsMenu.addAction("Setup Chracter")
        self.CharReset = self.ToolsMenu.addAction("Reset Chracter")

        self.SepChar = self.ToolsMenu.addSeparator()
        self.SepChar.setText("Character")

        self.Connect = self.ToolsMenu.addAction("Char Connect")
        self.CharDis = self.ToolsMenu.addAction("Char Disconnect")
        self.Bake = self.ToolsMenu.addAction("Char Bake")

        self.SepProb = self.ToolsMenu.addSeparator()
        self.SepProb.setText("Control")

        self.PConnect = self.ToolsMenu.addAction("Control Connect")
        self.PDis = self.ToolsMenu.addAction("Control Disconnect")
        self.PBake = self.ToolsMenu.addAction("Control Bake")

        self.SepTool = self.ToolsMenu.addSeparator()
        self.SepTool.setText("Tools")

        self.MILimbPoint = self.ToolsMenu.addAction("Limb Point")
        self.MILimbPointDialog = self.ToolsMenu.addAction("Limb Point Dialog")

        self.ToolsMenu.addSeparator()

        self.CharacterSetMenu = self.ToolsMenu.addAction("Character Set")
        self.SelectionSetMenu = self.ToolsMenu.addAction("Selection Set")

        self.ToolsMenu.addSeparator()

        self.FBXBatch = self.ToolsMenu.addAction("FBX Batch")
        self.ToolsBTN.setMenu(self.ToolsMenu)

        '''-------- Left Sceleton --------'''

        mui.Label(W=self, Text="From", Pos=[20, 30])

        self.BTNLHead = mui.Button(W=self, Pos=[70, 25], Width=25, Height=30)  # Head
        self.BTNLNeck = mui.Button(W=self, Pos=[75, 55], Width=15, Height=15)  # Neck
        self.BTNLChest = mui.Button(W=self, Pos=[60, 85], Width=45, Height=40)  # Chest
        self.BTNLPelvis = mui.Button(W=self, Pos=[60, 150], Width=45, Height=20)  # Pelvis

        self.BTNLClavicleR = mui.Button(W=self, Pos=[40, 70], Width=43, Height=15)  # Clavicle R
        self.BTNLUpperArmR = mui.Button(W=self, Pos=[40, 85], Width=15, Height=45)  # UpperArm R
        self.BTNLLowerArmR = mui.Button(W=self, Pos=[40, 130], Width=15, Height=40)  # LowerArm R
        self.BTNLHandR = mui.Button(W=self, Pos=[40, 170], Width=15, Height=20)  # Hand R

        self.BTNLClavicleL = mui.Button(W=self, Pos=[83, 70], Width=42, Height=15)  # Clavicle L
        self.BTNLUpperArmL = mui.Button(W=self, Pos=[110, 85], Width=15, Height=45)  # UpperArm L
        self.BTNLLowerArmL = mui.Button(W=self, Pos=[110, 130], Width=15, Height=40)  # LowerArm L
        self.BTNLHandL = mui.Button(W=self, Pos=[110, 170], Width=15, Height=20)  # Hand L

        self.BTNLThingR = mui.Button(W=self, Pos=[60, 170], Width=20, Height=65)  # Thing R
        self.BTNLCalfR = mui.Button(W=self, Pos=[60, 235], Width=20, Height=70)  # Calf R
        self.BTNLFootR = mui.Button(W=self, Pos=[55, 305], Width=25, Height=15)  # Foot R
        self.BTNLToeR = mui.Button(W=self, Pos=[40, 305], Width=15, Height=15)  # Toe R

        self.BTNLThingL = mui.Button(W=self, Pos=[85, 170], Width=20, Height=65)  # Thing L
        self.BTNLCalfL = mui.Button(W=self, Pos=[85, 235], Width=20, Height=70)  # Calf L
        self.BTNLFootL = mui.Button(W=self, Pos=[85, 305], Width=25, Height=15)  # Foot L
        self.BTNLToeL = mui.Button(W=self, Pos=[110, 305], Width=15, Height=15)  # Toe L

        self.BTNLArmPointR = mui.Button(W=self, Pos=[20, 120], Width=15, Height=15)  # Arm Point R
        self.BTNLArmPointL = mui.Button(W=self, Pos=[130, 120], Width=15, Height=15)  # Arm Point L
        self.BTNLLegPointR = mui.Button(W=self, Pos=[40, 225], Width=15, Height=15)  # Leg Point R
        self.BTNLLegPointL = mui.Button(W=self, Pos=[110, 225], Width=15, Height=15)  # Leg Point L

        '''-------- Right Sceleton --------'''

        mui.Label(W=self, Text="To", Pos=[185, 30])

        self.BTNRHead = mui.Button(W=self, Pos=[230, 25], Width=25, Height=30)  # Head
        self.BTNRNeck = mui.Button(W=self, Pos=[235, 55], Width=15, Height=15)  # Neck
        self.BTNRChest = mui.Button(W=self, Pos=[220, 85], Width=45, Height=40)  # Chest
        self.BTNRPelvis = mui.Button(W=self, Pos=[220, 150], Width=45, Height=20)  # Pelvis

        self.BTNRClavicleR = mui.Button(W=self, Pos=[200, 70], Width=43, Height=15)  # Clavicle R
        self.BTNRUpperArmR = mui.Button(W=self, Pos=[200, 85], Width=15, Height=45)  # UpperArm R
        self.BTNRLowerArmR = mui.Button(W=self, Pos=[200, 130], Width=15, Height=40)  # LowerArm R
        self.BTNRHandR = mui.Button(W=self, Pos=[200, 170], Width=15, Height=20)  # Hand R

        self.BTNRClavicleL = mui.Button(W=self, Pos=[243, 70], Width=42, Height=15)  # Clavicle L
        self.BTNRUpperArmL = mui.Button(W=self, Pos=[270, 85], Width=15, Height=45)  # UpperArm L
        self.BTNRLowerArmL = mui.Button(W=self, Pos=[270, 130], Width=15, Height=40)  # LowerArm L
        self.BTNRHandL = mui.Button(W=self, Pos=[270, 170], Width=15, Height=20)  # Hand L

        self.BTNRThingR = mui.Button(W=self, Pos=[220, 170], Width=20, Height=65)  # Thing R
        self.BTNRCalfR = mui.Button(W=self, Pos=[220, 235], Width=20, Height=70)  # Calf R
        self.BTNRFootR = mui.Button(W=self, Pos=[215, 305], Width=25, Height=15)  # Foot R
        self.BTNRToeR = mui.Button(W=self, Pos=[200, 305], Width=15, Height=15)  # Toe R

        self.BTNRThingL = mui.Button(W=self, Pos=[245, 170], Width=20, Height=65)  # Thing L
        self.BTNRCalfL = mui.Button(W=self, Pos=[245, 235], Width=20, Height=70)  # Calf L
        self.BTNRFootL = mui.Button(W=self, Pos=[245, 305], Width=25, Height=15)  # Foot L
        self.BTNRToeL = mui.Button(W=self, Pos=[270, 305], Width=15, Height=15)  # Toe L

        self.BTNRArmPointR = mui.Button(W=self, Pos=[180, 120], Width=15, Height=15)  # Arm Point R
        self.BTNRArmPointL = mui.Button(W=self, Pos=[290, 120], Width=15, Height=15)  # Arm Point L
        self.BTNRLegPointR = mui.Button(W=self, Pos=[200, 225], Width=15, Height=15)  # Leg Point R
        self.BTNRLegPointL = mui.Button(W=self, Pos=[270, 225], Width=15, Height=15)  # Leg Point L

        '''------------- Button Connects -------------'''

        self.MISaveFile.triggered.connect(self.SaveFile)
        self.MIOpenFile.triggered.connect(self.OpenFile)
        self.MIReset.triggered.connect(self.ResetFile)

        self.ArmsFK.triggered.connect(self.SetArmsFK)
        self.ArmsIK.triggered.connect(self.SetArmsIK)

        self.LegsFK.triggered.connect(self.SetLegsFK)
        self.LegsIK.triggered.connect(self.SetLegsIK)

        self.CharSetup.triggered.connect(self.CharacterSetup)
        self.CharReset.triggered.connect(self.CharacterReset)

        self.Bake.triggered.connect(self.BakeAll)
        self.Connect.triggered.connect(self.ConnectAll)
        self.CharDis.triggered.connect(self.DisconnectChar)

        self.PBake.triggered.connect(self.ProbBake)
        self.PConnect.triggered.connect(self.ProbConnect)
        self.PDis.triggered.connect(self.DisconnectProb)

        self.MILimbPoint.triggered.connect(self.LimbPoint)
        self.MILimbPointDialog.triggered.connect(self.LimbPointDialod)
        self.CharacterSetMenu.triggered.connect(self.CharacterSet)
        self.SelectionSetMenu.triggered.connect(self.SelectionSet)
        self.FBXBatch.triggered.connect(self.BatchFBX)

        '''-------------------------------------------'''

        self.BTNLHead.clicked.connect(self.LSSetHead)
        self.BTNRHead.clicked.connect(self.RSSetHead)

        self.BTNLHead.rightClick.connect(self.LSSetHead_RC)
        self.BTNRHead.rightClick.connect(self.RSSetHead_RC)

        self.BTNLNeck.clicked.connect(self.LSSetNeck)
        self.BTNRNeck.clicked.connect(self.RSSetNeck)

        self.BTNLNeck.rightClick.connect(self.LSSetNeck_RC)
        self.BTNRNeck.rightClick.connect(self.RSSetNeck_RC)

        self.BTNLChest.clicked.connect(self.LSSetChest)
        self.BTNRChest.clicked.connect(self.RSSetChest)

        self.BTNLChest.rightClick.connect(self.LSSetChest_RC)
        self.BTNRChest.rightClick.connect(self.RSSetChest_RC)

        self.BTNLPelvis.clicked.connect(self.LSSetPelvis)
        self.BTNRPelvis.clicked.connect(self.RSSetPelvis)

        self.BTNLPelvis.rightClick.connect(self.LSSetPelvis_RC)
        self.BTNRPelvis.rightClick.connect(self.RSSetPelvis_RC)

        '''-------------------------------------------'''

        self.BTNLClavicleR.clicked.connect(self.LSSetClavicleR)
        self.BTNRClavicleR.clicked.connect(self.RSSetClavicleR)

        self.BTNLClavicleR.rightClick.connect(self.LSSetClavicleR_RC)
        self.BTNRClavicleR.rightClick.connect(self.RSSetClavicleR_RC)

        self.BTNLUpperArmR.clicked.connect(self.LSSetUpperArmR)
        self.BTNRUpperArmR.clicked.connect(self.RSSetUpperArmR)

        self.BTNLUpperArmR.rightClick.connect(self.LSSetUpperArmR_RC)
        self.BTNRUpperArmR.rightClick.connect(self.RSSetUpperArmR_RC)

        self.BTNLLowerArmR.clicked.connect(self.LSSetLowerArmR)
        self.BTNRLowerArmR.clicked.connect(self.RSSetLowerArmR)

        self.BTNLLowerArmR.rightClick.connect(self.LSSetLowerArmR_RC)
        self.BTNRLowerArmR.rightClick.connect(self.RSSetLowerArmR_RC)

        self.BTNLHandR.clicked.connect(self.LSSetHandR)
        self.BTNRHandR.clicked.connect(self.RSSetHandR)

        self.BTNLHandR.rightClick.connect(self.LSSetHandR_RC)
        self.BTNRHandR.rightClick.connect(self.RSSetHandR_RC)

        '''-------------------------------------------'''

        self.BTNLClavicleL.clicked.connect(self.LSSetClavicleL)
        self.BTNRClavicleL.clicked.connect(self.RSSetClavicleL)

        self.BTNLClavicleL.rightClick.connect(self.LSSetClavicleL_RC)
        self.BTNRClavicleL.rightClick.connect(self.RSSetClavicleL_RC)

        self.BTNLUpperArmL.clicked.connect(self.LSSetUpperArmL)
        self.BTNRUpperArmL.clicked.connect(self.RSSetUpperArmL)

        self.BTNLUpperArmL.rightClick.connect(self.LSSetUpperArmL_RC)
        self.BTNRUpperArmL.rightClick.connect(self.RSSetUpperArmL_RC)

        self.BTNLLowerArmL.clicked.connect(self.LSSetLowerArmL)
        self.BTNRLowerArmL.clicked.connect(self.RSSetLowerArmL)

        self.BTNLLowerArmL.rightClick.connect(self.LSSetLowerArmL_RC)
        self.BTNRLowerArmL.rightClick.connect(self.RSSetLowerArmL_RC)

        self.BTNLHandL.clicked.connect(self.LSSetHandL)
        self.BTNRHandL.clicked.connect(self.RSSetHandL)

        self.BTNLHandL.rightClick.connect(self.LSSetHandL_RC)
        self.BTNRHandL.rightClick.connect(self.RSSetHandL_RC)

        '''-------------------------------------------'''

        self.BTNLThingR.clicked.connect(self.LSSetThingR)
        self.BTNRThingR.clicked.connect(self.RSSetThingR)

        self.BTNLThingR.rightClick.connect(self.LSSetThingR_RC)
        self.BTNRThingR.rightClick.connect(self.RSSetThingR_RC)

        self.BTNLCalfR.clicked.connect(self.LSSetCalfR)
        self.BTNRCalfR.clicked.connect(self.RSSetCalfR)

        self.BTNLCalfR.rightClick.connect(self.LSSetCalfR_RC)
        self.BTNRCalfR.rightClick.connect(self.RSSetCalfR_RC)

        self.BTNLFootR.clicked.connect(self.LSSetFootR)
        self.BTNRFootR.clicked.connect(self.RSSetFootR)

        self.BTNLFootR.rightClick.connect(self.LSSetFootR_RC)
        self.BTNRFootR.rightClick.connect(self.RSSetFootR_RC)

        self.BTNLToeR.clicked.connect(self.LSSetToeR)
        self.BTNRToeR.clicked.connect(self.RSSetToeR)

        self.BTNLToeR.rightClick.connect(self.LSSetToeR_RC)
        self.BTNRToeR.rightClick.connect(self.RSSetToeR_RC)

        '''-------------------------------------------'''

        self.BTNLThingL.clicked.connect(self.LSSetThingL)
        self.BTNRThingL.clicked.connect(self.RSSetThingL)

        self.BTNLThingL.rightClick.connect(self.LSSetThingL_RC)
        self.BTNRThingL.rightClick.connect(self.RSSetThingL_RC)

        self.BTNLCalfL.clicked.connect(self.LSSetCalfL)
        self.BTNRCalfL.clicked.connect(self.RSSetCalfL)

        self.BTNLCalfL.rightClick.connect(self.LSSetCalfL_RC)
        self.BTNRCalfL.rightClick.connect(self.RSSetCalfL_RC)

        self.BTNLFootL.clicked.connect(self.LSSetFootL)
        self.BTNRFootL.clicked.connect(self.RSSetFootL)

        self.BTNLFootL.rightClick.connect(self.LSSetFootL_RC)
        self.BTNRFootL.rightClick.connect(self.RSSetFootL_RC)

        self.BTNLToeL.clicked.connect(self.LSSetToeL)
        self.BTNRToeL.clicked.connect(self.RSSetToeL)

        self.BTNLToeL.rightClick.connect(self.LSSetToeL_RC)
        self.BTNRToeL.rightClick.connect(self.RSSetToeL_RC)

        '''-------------------------------------------'''

        self.BTNLArmPointR.clicked.connect(self.LSSetArmPointR)
        self.BTNRArmPointR.clicked.connect(self.RSSetArmPointR)

        self.BTNLArmPointR.rightClick.connect(self.LSSetArmPointR_RC)
        self.BTNRArmPointR.rightClick.connect(self.RSSetArmPointR_RC)

        self.BTNLArmPointL.clicked.connect(self.LSSetArmPointL)
        self.BTNRArmPointL.clicked.connect(self.RSSetArmPointL)

        self.BTNLArmPointL.rightClick.connect(self.LSSetArmPointL_RC)
        self.BTNRArmPointL.rightClick.connect(self.RSSetArmPointL_RC)

        self.BTNLLegPointR.clicked.connect(self.LSSetLegPointR)
        self.BTNRLegPointR.clicked.connect(self.RSSetLegPointR)

        self.BTNLLegPointR.rightClick.connect(self.LSSetLegPointR_RC)
        self.BTNRLegPointR.rightClick.connect(self.RSSetLegPointR_RC)

        self.BTNLLegPointL.clicked.connect(self.LSSetLegPointL)
        self.BTNRLegPointL.clicked.connect(self.RSSetLegPointL)

        self.BTNLLegPointL.rightClick.connect(self.LSSetLegPointL_RC)
        self.BTNRLegPointL.rightClick.connect(self.RSSetLegPointL_RC)

        '''-------- Variable --------'''

        self.LSArray = [None] * 24
        self.RSArray = [None] * 24

    '''--------------------------------'''

    def RunFile(self, Path):
        thePath = (os.path.dirname(os.path.abspath(__file__)) + "\\" + Path)

        file = os.path.basename(thePath)
        dir = os.path.dirname(thePath)

        toks = file.split('.')
        modname = toks[0]

        if (os.path.exists(dir)):

            paths = sys.path
            pathfound = 0
            for path in paths:
                if (dir == path):
                    pathfound = 1

            if not pathfound:
                sys.path.append(dir)

        exec ('import ' + modname) in globals()

        exec ('reload( ' + modname + ' )') in globals()

    def SetTollTip(self):
        self.BTNLHead.setToolTip(str(self.LSArray[0]))
        self.BTNLNeck.setToolTip(str(self.LSArray[1]))
        self.BTNLChest.setToolTip(str(self.LSArray[2]))
        self.BTNLPelvis.setToolTip(str(self.LSArray[3]))
        self.BTNLClavicleR.setToolTip(str(self.LSArray[4]))
        self.BTNLUpperArmR.setToolTip(str(self.LSArray[5]))
        self.BTNLLowerArmR.setToolTip(str(self.LSArray[6]))
        self.BTNLHandR.setToolTip(str(self.LSArray[7]))
        self.BTNLClavicleL.setToolTip(str(self.LSArray[8]))
        self.BTNLUpperArmL.setToolTip(str(self.LSArray[9]))
        self.BTNLLowerArmL.setToolTip(str(self.LSArray[10]))
        self.BTNLHandL.setToolTip(str(self.LSArray[11]))
        self.BTNLThingR.setToolTip(str(self.LSArray[12]))
        self.BTNLCalfR.setToolTip(str(self.LSArray[13]))
        self.BTNLFootR.setToolTip(str(self.LSArray[14]))
        self.BTNLToeR.setToolTip(str(self.LSArray[15]))
        self.BTNLThingL.setToolTip(str(self.LSArray[16]))
        self.BTNLCalfL.setToolTip(str(self.LSArray[17]))
        self.BTNLFootL.setToolTip(str(self.LSArray[18]))
        self.BTNLToeL.setToolTip(str(self.LSArray[19]))
        self.BTNLArmPointR.setToolTip(str(self.LSArray[20]))
        self.BTNLArmPointL.setToolTip(str(self.LSArray[21]))
        self.BTNLLegPointR.setToolTip(str(self.LSArray[22]))
        self.BTNLLegPointL.setToolTip(str(self.LSArray[23]))

        self.BTNRHead.setToolTip(str(self.RSArray[0]))
        self.BTNRNeck.setToolTip(str(self.RSArray[1]))
        self.BTNRChest.setToolTip(str(self.RSArray[2]))
        self.BTNRPelvis.setToolTip(str(self.RSArray[3]))
        self.BTNRClavicleR.setToolTip(str(self.RSArray[4]))
        self.BTNRUpperArmR.setToolTip(str(self.RSArray[5]))
        self.BTNRLowerArmR.setToolTip(str(self.RSArray[6]))
        self.BTNRHandR.setToolTip(str(self.RSArray[7]))
        self.BTNRClavicleL.setToolTip(str(self.RSArray[8]))
        self.BTNRUpperArmL.setToolTip(str(self.RSArray[9]))
        self.BTNRLowerArmL.setToolTip(str(self.RSArray[10]))
        self.BTNRHandL.setToolTip(str(self.RSArray[11]))
        self.BTNRThingR.setToolTip(str(self.RSArray[12]))
        self.BTNRCalfR.setToolTip(str(self.RSArray[13]))
        self.BTNRFootR.setToolTip(str(self.RSArray[14]))
        self.BTNRToeR.setToolTip(str(self.RSArray[15]))
        self.BTNRThingL.setToolTip(str(self.RSArray[16]))
        self.BTNRCalfL.setToolTip(str(self.RSArray[17]))
        self.BTNRFootL.setToolTip(str(self.RSArray[18]))
        self.BTNRToeL.setToolTip(str(self.RSArray[19]))
        self.BTNRArmPointR.setToolTip(str(self.RSArray[20]))
        self.BTNRArmPointL.setToolTip(str(self.RSArray[21]))
        self.BTNRLegPointR.setToolTip(str(self.RSArray[22]))
        self.BTNRLegPointL.setToolTip(str(self.RSArray[23]))

    def showEvent(self, event):
        self.SetTollTip()

    def paintEvent(self, event):
        Paint = qg.QPainter()
        Paint.begin(self)

        Paint.setPen(qg.QPen(qg.QColor(0, 0, 0, 0)))
        Paint.setBrush(qg.QColor(93, 93, 93))

        Paint.drawRect(0, 0, 325, 20)
        Paint.drawRect(70, 125, 25, 25)
        Paint.drawRect(230, 125, 25, 25)
        Paint.drawRect(160, 25, 5, 295)

        Paint.end()

    '''--------------------------------'''

    def CharacterSetup(self):

        sel = pm.ls(sl=True, l=True)[0]

        '''--- create root ---'''

        rootNode = pm.ls(sl=True)[0]

        ctrlGroup = rootNode + "_ctl"
        cmds.group(n=ctrlGroup, em=True)

        locName = rootNode + "_origin"
        cmds.spaceLocator(n=locName)

        cmds.setAttr(locName + ".localScaleX", 30)
        cmds.setAttr(locName + ".localScaleY", 30)
        cmds.setAttr(locName + ".localScaleZ", 30)

        DecomposeNode = pm.createNode("decomposeMatrix")
        pm.connectAttr(locName + ".worldMatrix[0]", DecomposeNode.inputMatrix)
        pm.connectAttr(DecomposeNode.outputTranslate, rootNode.translate)
        pm.connectAttr(DecomposeNode.outputRotate, rootNode.rotate)
        pm.connectAttr(DecomposeNode.outputScale, rootNode.scale)

        '''--- all childs ---'''

        charNodes = cmds.listRelatives(str(sel), ad=True, f=True)
        cmds.cutKey(charNodes, s=True)

        '''--- reset rotations ---'''

        for i in range(len(charNodes)):
            node = charNodes[i]

            cmds.setAttr(str(node) + ".rotateX", 0)
            cmds.setAttr(str(node) + ".rotateY", 0)
            cmds.setAttr(str(node) + ".rotateZ", 0)

        '''--- hip trasformations ---'''

        cHip = str(charNodes[33])
        cmds.setAttr(cHip + ".rotateX", -90)
        cmds.setAttr(cHip + ".translateX", 0)
        cmds.setAttr(cHip + ".translateZ", 0)

        '''--- left leg trasformations ---'''

        cLeftUpLeg = str(charNodes[32])
        cmds.setAttr(cLeftUpLeg + ".rotateZ", -3)

        cLeftLeg = str(charNodes[31])
        cmds.setAttr(cLeftLeg + ".rotateZ", 6)

        cLeftFoot = str(charNodes[30])
        cmds.setAttr(cLeftFoot + ".rotateZ", -3)

        '''--- left leg offset ---'''

        name = rootNode + "_left_Leg_OP"
        cmds.spaceLocator(n=name)

        cmds.parent(name, cHip)

        ll_pos = cmds.getAttr(cLeftUpLeg + ".translate")[0]
        ll_ros = cmds.getAttr(cLeftUpLeg + ".rotate")[0]

        cmds.setAttr(name + ".translateX", ll_pos[0])
        cmds.setAttr(name + ".translateY", ll_pos[1])
        cmds.setAttr(name + ".translateZ", ll_pos[2])

        cmds.setAttr(name + ".rotateX", ll_ros[0])
        cmds.setAttr(name + ".rotateY", ll_ros[1])
        cmds.setAttr(name + ".rotateZ", ll_ros[2])

        cmds.setAttr(name + ".localScaleX", 5)
        cmds.setAttr(name + ".localScaleY", 5)
        cmds.setAttr(name + ".localScaleZ", 5)

        cmds.pointConstraint(name, cLeftUpLeg)

        '''--- left leg limb point ---'''

        name = rootNode + "_left_Leg_LP"

        PointMatrixNode = pm.createNode("Point3Matrix")
        DecomposeNode = pm.createNode("decomposeMatrix")
        cmds.spaceLocator(n=name)

        pm.connectAttr(cLeftUpLeg + ".worldMatrix[0]", PointMatrixNode.Matrix1)
        pm.connectAttr(cLeftLeg + ".worldMatrix[0]", PointMatrixNode.Matrix2)
        pm.connectAttr(cLeftFoot + ".worldMatrix[0]", PointMatrixNode.Matrix3)
        pm.connectAttr(PointMatrixNode.OutputMatrix, DecomposeNode.inputMatrix)
        pm.connectAttr(DecomposeNode.outputTranslate, name + ".translate")
        pm.connectAttr(DecomposeNode.outputRotate, name + ".rotate")

        pm.setAttr(PointMatrixNode.OffsetX, -30)
        pm.setAttr(PointMatrixNode.OffsetY, 0)
        pm.setAttr(PointMatrixNode.OffsetZ, 0)

        pm.setAttr(PointMatrixNode.FlipX, False)
        pm.setAttr(PointMatrixNode.FlipY, True)
        pm.setAttr(PointMatrixNode.FlipZ, False)

        cmds.setAttr(name + ".localScaleX", 5)
        cmds.setAttr(name + ".localScaleY", 5)
        cmds.setAttr(name + ".localScaleZ", 5)

        cmds.parent(name, ctrlGroup)

        '''--- right leg trasformations ---'''

        cRightUpLeg = str(charNodes[27])
        cmds.setAttr(cRightUpLeg + ".rotateZ", -3)

        cRightLeg = str(charNodes[26])
        cmds.setAttr(cRightLeg + ".rotateZ", 6)

        cRightFoot = str(charNodes[25])
        cmds.setAttr(cRightFoot + ".rotateZ", -3)

        '''--- right leg offset ---'''

        name = rootNode + "_right_Leg_OP"
        cmds.spaceLocator(n=name)

        cmds.parent(name, cHip)

        rl_pos = cmds.getAttr(cRightUpLeg + ".translate")[0]
        rl_ros = cmds.getAttr(cRightUpLeg + ".rotate")[0]

        cmds.setAttr(name + ".translateX", rl_pos[0])
        cmds.setAttr(name + ".translateY", rl_pos[1])
        cmds.setAttr(name + ".translateZ", rl_pos[2])

        cmds.setAttr(name + ".rotateX", rl_ros[0])
        cmds.setAttr(name + ".rotateY", rl_ros[1])
        cmds.setAttr(name + ".rotateZ", rl_ros[2])

        cmds.setAttr(name + ".localScaleX", 5)
        cmds.setAttr(name + ".localScaleY", 5)
        cmds.setAttr(name + ".localScaleZ", 5)

        cmds.pointConstraint(name, cRightUpLeg)

        '''--- left leg limb point ---'''

        name = rootNode + "_right_Leg_LP"

        PointMatrixNode = pm.createNode("Point3Matrix")
        DecomposeNode = pm.createNode("decomposeMatrix")
        cmds.spaceLocator(n=name)

        pm.connectAttr(cRightUpLeg + ".worldMatrix[0]", PointMatrixNode.Matrix1)
        pm.connectAttr(cRightLeg + ".worldMatrix[0]", PointMatrixNode.Matrix2)
        pm.connectAttr(cRightFoot + ".worldMatrix[0]", PointMatrixNode.Matrix3)
        pm.connectAttr(PointMatrixNode.OutputMatrix, DecomposeNode.inputMatrix)
        pm.connectAttr(DecomposeNode.outputTranslate, name + ".translate")
        pm.connectAttr(DecomposeNode.outputRotate, name + ".rotate")

        pm.setAttr(PointMatrixNode.OffsetX, -30)
        pm.setAttr(PointMatrixNode.OffsetY, 0)
        pm.setAttr(PointMatrixNode.OffsetZ, 0)

        pm.setAttr(PointMatrixNode.FlipX, False)
        pm.setAttr(PointMatrixNode.FlipY, True)
        pm.setAttr(PointMatrixNode.FlipZ, False)

        cmds.setAttr(name + ".localScaleX", 5)
        cmds.setAttr(name + ".localScaleY", 5)
        cmds.setAttr(name + ".localScaleZ", 5)

        cmds.parent(name, ctrlGroup)

        '''--- left arm trasformations ---'''

        cLeftArm = str(charNodes[17])
        cmds.setAttr(cLeftArm + ".rotateZ", 3)

        cLeftForeArm = str(charNodes[16])
        cmds.setAttr(cLeftForeArm + ".rotateZ", -6)

        cLeftHand = str(charNodes[15])
        cmds.setAttr(cLeftHand + ".rotateZ", 3)

        '''--- right arm trasformations ---'''

        cRightArm = str(charNodes[9])
        cmds.setAttr(cRightArm + ".rotateZ", 3)

        cRightForeArm = str(charNodes[8])
        cmds.setAttr(cRightForeArm + ".rotateZ", -6)

        cRightHand = str(charNodes[7])
        cmds.setAttr(cRightHand + ".rotateZ", 3)

        '''--- limb lock setup ---'''

        '''--- create floor plane ---'''

        FP = pm.ls("Floor_Plane")

        if len(FP) < 1:
            cmds.polyPlane(n="Floor_Plane", w=500, h=500, sx=1, sy=1)

        '''--- left leg setup ---'''

        mainName = rootNode + "_left_Main_LL"

        leftFootPos = cmds.xform(cLeftFoot, q=True, t=True, ws=True)

        cmds.spaceLocator(n=mainName)
        cmds.setAttr(mainName + ".translate", leftFootPos[0], leftFootPos[1], leftFootPos[2])
        cmds.setAttr(mainName + ".localScale", 5, 5, 5)
        cmds.parentConstraint(cLeftFoot, mainName, mo=True)

        contactName = rootNode + "_left_Contact_LL"

        cmds.spaceLocator(n=contactName)
        cmds.setAttr(contactName + ".translate", leftFootPos[0], 0, leftFootPos[2])
        cmds.setAttr(contactName + ".localScale", 5, 5, 5)

        LimbLockNode = pm.createNode("Limb_Lock")
        DecomposeNode = pm.createNode("decomposeMatrix")
        pm.connectAttr(mainName + ".worldMatrix[0]", LimbLockNode.InputMatrix)
        pm.connectAttr("Floor_Plane.translateY", LimbLockNode.Offset)
        pm.connectAttr(LimbLockNode.OutputMatrix, DecomposeNode.inputMatrix)
        pm.connectAttr(DecomposeNode.outputTranslate, contactName + ".translate")
        pm.connectAttr(DecomposeNode.outputRotate, contactName + ".rotate")

        cmds.parent(mainName, ctrlGroup)
        cmds.parent(contactName, ctrlGroup)

        '''--- left leg setup ---'''

        mainName = rootNode + "_right_Main_LL"

        rightFootPos = cmds.xform(cRightFoot, q=True, t=True, ws=True)

        cmds.spaceLocator(n=mainName)
        cmds.setAttr(mainName + ".translate", rightFootPos[0], rightFootPos[1], rightFootPos[2])
        cmds.setAttr(mainName + ".localScale", 5, 5, 5)
        cmds.parentConstraint(cRightFoot, mainName, mo=True)

        contactName = rootNode + "_right_Contact_LL"

        cmds.spaceLocator(n=contactName)
        cmds.setAttr(contactName + ".translate", rightFootPos[0], 0, rightFootPos[2])
        cmds.setAttr(contactName + ".localScale", 5, 5, 5)

        LimbLockNode = pm.createNode("Limb_Lock")
        DecomposeNode = pm.createNode("decomposeMatrix")
        pm.connectAttr(mainName + ".worldMatrix[0]", LimbLockNode.InputMatrix)
        pm.connectAttr("Floor_Plane.translateY", LimbLockNode.Offset)
        pm.connectAttr(LimbLockNode.OutputMatrix, DecomposeNode.inputMatrix)
        pm.connectAttr(DecomposeNode.outputTranslate, contactName + ".translate")
        pm.connectAttr(DecomposeNode.outputRotate, contactName + ".rotate")

        cmds.parent(mainName, ctrlGroup)
        cmds.parent(contactName, ctrlGroup)

        '''--- parent to root group ---'''

        RG = pm.ls("Mocap")

        if len(RG) < 1:
            cmds.group(em=True, name="Mocap")

        cmds.parent(rootNode.name(), "Mocap")
        cmds.parent(ctrlGroup, "Mocap")
        cmds.parent(locName, "Mocap")
        cmds.parent("Floor_Plane", "Mocap")


    def CharacterReset(self):
        sel = pm.ls(sl=True, l=True)[0]

        '''--- all chields ---'''

        charNodes = cmds.listRelatives(str(sel), ad=True, f=True)
        cmds.cutKey(charNodes, s=True)

        '''--- reset rotations ---'''

        for i in range(len(charNodes)):
            node = charNodes[i]

            cmds.setAttr(str(node) + ".rotateX", 0)
            cmds.setAttr(str(node) + ".rotateY", 0)
            cmds.setAttr(str(node) + ".rotateZ", 0)

        '''--- hip trasformations ---'''

        cHip = str(charNodes[33])
        cmds.setAttr(cHip + ".rotateX", -90)
        cmds.setAttr(cHip + ".translateX", 0)
        cmds.setAttr(cHip + ".translateZ", 0)

        '''--- left leg trasformations ---'''

        cLeftUpLeg = str(charNodes[32])
        cmds.setAttr(cLeftUpLeg + ".rotateZ", -3)

        cLeftLeg = str(charNodes[31])
        cmds.setAttr(cLeftLeg + ".rotateZ", 6)

        cLeftFoot = str(charNodes[30])
        cmds.setAttr(cLeftFoot + ".rotateZ", -3)

        '''--- right leg trasformations ---'''

        cRightUpLeg = str(charNodes[27])
        cmds.setAttr(cRightUpLeg + ".rotateZ", -3)

        cRightLeg = str(charNodes[26])
        cmds.setAttr(cRightLeg + ".rotateZ", 6)

        cRightFoot = str(charNodes[25])
        cmds.setAttr(cRightFoot + ".rotateZ", -3)

        '''--- left arm trasformations ---'''

        cLeftArm = str(charNodes[17])
        cmds.setAttr(cLeftArm + ".rotateZ", 3)

        cLeftForeArm = str(charNodes[16])
        cmds.setAttr(cLeftForeArm + ".rotateZ", -6)

        cLeftHand = str(charNodes[15])
        cmds.setAttr(cLeftHand + ".rotateZ", 3)

        '''--- right arm trasformations ---'''

        cRightArm = str(charNodes[9])
        cmds.setAttr(cRightArm + ".rotateZ", 3)

        cRightForeArm = str(charNodes[8])
        cmds.setAttr(cRightForeArm + ".rotateZ", -6)

        cRightHand = str(charNodes[7])
        cmds.setAttr(cRightHand + ".rotateZ", 3)

    '''--------------------------------'''

    def ParentCon(self, objA, objB, MO=True):
        cmds.parentConstraint(objA, objB, mo=MO)

    def OrientCon(self, objA, objB, MO=True):
        cmds.orientConstraint(objA, objB, mo=MO)

    def PointCon(self, objA, objB, MO=False):
        cmds.pointConstraint(objA, objB, mo=MO)

    def ConnectAll(self):

        cmds.select(self.RSArray)
        cmds.delete(cn=True)
        cmds.select(clear=True)

        Master = self.LSArray
        Slave = self.RSArray

        "Head"
        if Master[0] != None:
            self.OrientCon(Master[0], Slave[0])

        "Neck"
        if Master[1] != None:
            self.OrientCon(Master[1], Slave[1])

        "Chest"
        if Master[2] != None:
            self.ParentCon(Master[2], Slave[2])

        "Pelvis"
        if Master[3] != None:
            self.ParentCon(Master[3], Slave[3])

        "ClavicleR"
        if Master[4] != None:
            self.OrientCon(Master[4], Slave[4])

        "UpperArmR"
        if Master[5] != None:
            if self.ArmsFK.isChecked() == True:
                self.OrientCon(Master[5], Slave[5])

        "LowerArmR"
        if Master[6] != None:
            if self.ArmsFK.isChecked() == True:
                self.OrientCon(Master[6], Slave[6])

        "HandR"
        if Master[7] != None:
            if self.ArmsFK.isChecked() == True:
                self.OrientCon(Master[7], Slave[7])
            else:
                self.ParentCon(Master[7], Slave[7])

        "ClavicleL"
        if Master[8] != None:
            self.OrientCon(Master[8], Slave[8])

        "UpperArmL"
        if Master[9] != None:
            if self.ArmsFK.isChecked() == True:
                self.OrientCon(Master[9], Slave[9])

        "LowerArmL"
        if Master[10] != None:
            if self.ArmsFK.isChecked() == True:
                self.OrientCon(Master[10], Slave[10])

        "HandL"
        if Master[11] != None:
            if self.ArmsFK.isChecked() == True:
                self.OrientCon(Master[11], Slave[11])
            else:
                self.ParentCon(Master[11], Slave[11])

        "ThingR"
        if Master[12] != None:
            if self.LegsFK.isChecked() == True:
                self.OrientCon(Master[12], Slave[12])

        "CalfR"
        if Master[13] != None:
            if self.LegsFK.isChecked() == True:
                self.OrientCon(Master[13], Slave[13])

        "FootR"
        if Master[14] != None:
            if self.LegsFK.isChecked() == True:
                self.OrientCon(Master[14], Slave[14])
            else:
                self.ParentCon(Master[14], Slave[14])

        "ToeR"
        if Master[15] != None:
            if self.LegsFK.isChecked() == True:
                self.OrientCon(Master[15], Slave[15])

        "ThingL"
        if Master[16] != None:
            if self.LegsFK.isChecked() == True:
                self.OrientCon(Master[16], Slave[16])

        "CalfL"
        if Master[17] != None:
            if self.LegsFK.isChecked() == True:
                self.OrientCon(Master[17], Slave[17])

        "FootL"
        if Master[18] != None:
            if self.LegsFK.isChecked() == True:
                self.OrientCon(Master[18], Slave[18])
            else:
                self.ParentCon(Master[18], Slave[18])

        "ToeL"
        if Master[19] != None:
            if self.LegsFK.isChecked() == True:
                self.OrientCon(Master[19], Slave[19])

        "ArmPointR"
        if Master[20] != None:
            if self.ArmsIK.isChecked() == True:
                self.PointCon(Master[20], Slave[20])

        "ArmPointL"
        if Master[21] != None:
            if self.ArmsIK.isChecked() == True:
                self.PointCon(Master[21], Slave[21])

        "LegPointR"
        if Master[22] != None:
            if self.LegsIK.isChecked() == True:
                self.PointCon(Master[22], Slave[22])

        "LegPointL"
        if Master[23] != None:
            if self.LegsIK.isChecked() == True:
                self.PointCon(Master[23], Slave[23])

    def BakeAll(self):
        Master = self.LSArray
        Slave = self.RSArray

        theStart = int(cmds.playbackOptions(query=True, animationStartTime=True))
        theEnd = int(cmds.playbackOptions(query=True, animationEndTime=True))

        cmds.currentTime(theStart)

        cmds.bakeSimulation(Slave, at=['tx', 'ty', 'tz', 'rx', 'ry', 'rz'], t=(theStart, theEnd))

        cmds.select(self.RSArray)
        cmds.delete(cn=True)
        cmds.select(clear=True)

    def DisconnectChar(self):
        Slave = self.RSArray
        cmds.select(Slave)
        cmds.delete(cn=True)
        cmds.select(clear=True)


        for i in range(len(Slave)):
            if Slave[i] != None:
                try:
                    cmds.setAttr(Slave[i] + ".translateX", 0)
                except:
                    pass

                try:
                    cmds.setAttr(Slave[i] + ".translateY", 0)
                except:
                    pass

                try:
                    cmds.setAttr(Slave[i] + ".translateZ", 0)
                except:
                    pass

                try:
                    cmds.setAttr(Slave[i] + ".rotateX", 0)
                except:
                    pass

                try:
                    cmds.setAttr(Slave[i] + ".rotateY", 0)
                except:
                    pass

                try:
                    cmds.setAttr(Slave[i] + ".rotateZ", 0)
                except:
                    pass

    '''--------------------------------'''

    def ProbConnect(self):
        Selection = cmds.ls(sl=True)

        Node_1 = Selection[0]
        Node_2 = Selection[1]

        self.ParentCon(Node_1, Node_2)

    def ProbBake(self):
        Selection = cmds.ls(sl=True)

        theStart = int(cmds.playbackOptions(query=True, animationStartTime=True))
        theEnd = int(cmds.playbackOptions(query=True, animationEndTime=True))

        cmds.currentTime(theStart)

        cmds.bakeSimulation(Selection, at=['tx', 'ty', 'tz', 'rx', 'ry', 'rz'], t=(theStart, theEnd))

        cmds.select(Selection)
        cmds.delete(cn=True)
        cmds.select(clear=True)

    def DisconnectProb(self):
        Selection = cmds.ls(sl=True)

        cmds.select(Selection)
        cmds.delete(cn=True)
        #cmds.select(clear=True)

    '''--------------------------------'''

    def SaveFile(self):
        Config = ConfigParser.ConfigParser()

        multipleFilters = "MRetarget Map (*.mmap);; All Files (*.*)"
        fileName = str((cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=1))[0])
        cfgfile = open(fileName, "w")

        Config.add_section("Data")
        Config.set("Data", "LS", str(self.LSArray))
        Config.set("Data", "RS", str(self.RSArray))
        Config.write(cfgfile)
        cfgfile.close()

    def OpenFile(self):
        Config = ConfigParser.ConfigParser()

        multipleFilters = "MRetarget Map (*.mmap);; All Files (*.*)"
        theFile = str((cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=1, fileMode=1))[0])

        Config.read(theFile)
        exec("self.LSArray = " + Config.get("Data", "LS"))
        exec ("self.RSArray = " + Config.get("Data", "RS"))

        if self.LSArray[0] != None:
            SetControl("L", self.BTNLHead, self.BTNRHead, self.LSArray[0], 0, self.LSArray, self.RSArray)
        if self.RSArray[0] != None:
            SetControl("R", self.BTNLHead, self.BTNRHead, self.RSArray[0], 0, self.LSArray, self.RSArray)

        if self.LSArray[1] != None:
            SetControl("L", self.BTNLNeck, self.BTNRNeck, self.LSArray[1], 1, self.LSArray, self.RSArray)
        if self.RSArray[1] != None:
            SetControl("R", self.BTNLNeck, self.BTNRNeck, self.RSArray[1], 1, self.LSArray, self.RSArray)

        if self.LSArray[2] != None:
            SetControl("L", self.BTNLChest, self.BTNRChest, self.LSArray[2], 2, self.LSArray, self.RSArray)
        if self.RSArray[2] != None:
            SetControl("R", self.BTNLChest, self.BTNRChest, self.RSArray[2], 2, self.LSArray, self.RSArray)

        if self.LSArray[3] != None:
            SetControl("L", self.BTNLPelvis, self.BTNRPelvis, self.LSArray[3], 3, self.LSArray, self.RSArray)
        if self.RSArray[3] != None:
            SetControl("R", self.BTNLPelvis, self.BTNRPelvis, self.RSArray[3], 3, self.LSArray, self.RSArray)

        '''------------------------------------------------------------------------------------------------'''

        if self.LSArray[4] != None:
            SetControl("L", self.BTNLClavicleR, self.BTNRClavicleR, self.LSArray[4], 4, self.LSArray, self.RSArray)
        if self.RSArray[4] != None:
            SetControl("R", self.BTNLClavicleR, self.BTNRClavicleR, self.RSArray[4], 4, self.LSArray, self.RSArray)

        if self.LSArray[5] != None:
            SetControl("L", self.BTNLUpperArmR, self.BTNRUpperArmR, self.LSArray[5], 5, self.LSArray, self.RSArray)
        if self.RSArray[5] != None:
            SetControl("R", self.BTNLUpperArmR, self.BTNRUpperArmR, self.RSArray[5], 5, self.LSArray, self.RSArray)

        if self.LSArray[6] != None:
            SetControl("L", self.BTNLLowerArmR, self.BTNRLowerArmR, self.LSArray[6], 6, self.LSArray, self.RSArray)
        if self.RSArray[6] != None:
            SetControl("R", self.BTNLLowerArmR, self.BTNRLowerArmR, self.RSArray[6], 6, self.LSArray, self.RSArray)

        if self.LSArray[7] != None:
            SetControl("L", self.BTNLHandR, self.BTNRHandR, self.LSArray[7], 7, self.LSArray, self.RSArray)
        if self.RSArray[7] != None:
            SetControl("R", self.BTNLHandR, self.BTNRHandR, self.RSArray[7], 7, self.LSArray, self.RSArray)

        '''------------------------------------------------------------------------------------------------'''

        if self.LSArray[8] != None:
            SetControl("L", self.BTNLClavicleL, self.BTNRClavicleL, self.LSArray[8], 8, self.LSArray, self.RSArray)
        if self.RSArray[8] != None:
            SetControl("R", self.BTNLClavicleL, self.BTNRClavicleL, self.RSArray[8], 8, self.LSArray, self.RSArray)

        if self.LSArray[9] != None:
            SetControl("L", self.BTNLUpperArmL, self.BTNRUpperArmL, self.LSArray[9], 9, self.LSArray, self.RSArray)
        if self.RSArray[9] != None:
            SetControl("R", self.BTNLUpperArmL, self.BTNRUpperArmL, self.RSArray[9], 9, self.LSArray, self.RSArray)

        if self.LSArray[10] != None:
            SetControl("L", self.BTNLLowerArmL, self.BTNRLowerArmL, self.LSArray[10], 10, self.LSArray, self.RSArray)
        if self.RSArray[10] != None:
            SetControl("R", self.BTNLLowerArmL, self.BTNRLowerArmL, self.RSArray[10], 10, self.LSArray, self.RSArray)

        if self.LSArray[11] != None:
            SetControl("L", self.BTNLHandL, self.BTNRHandL, self.LSArray[11], 11, self.LSArray, self.RSArray)
        if self.RSArray[11] != None:
            SetControl("R", self.BTNLHandL, self.BTNRHandL, self.RSArray[11], 11, self.LSArray, self.RSArray)

        '''------------------------------------------------------------------------------------------------'''

        if self.LSArray[12] != None:
            SetControl("L", self.BTNLThingR, self.BTNRThingR, self.LSArray[12], 12, self.LSArray, self.RSArray)
        if self.RSArray[12] != None:
            SetControl("R", self.BTNLThingR, self.BTNRThingR, self.RSArray[12], 12, self.LSArray, self.RSArray)

        if self.LSArray[13] != None:
            SetControl("L", self.BTNLCalfR, self.BTNRCalfR, self.LSArray[13], 13, self.LSArray, self.RSArray)
        if self.RSArray[13] != None:
            SetControl("R", self.BTNLCalfR, self.BTNRCalfR, self.RSArray[13], 13, self.LSArray, self.RSArray)

        if self.LSArray[14] != None:
            SetControl("L", self.BTNLFootR, self.BTNRFootR, self.LSArray[14], 14, self.LSArray, self.RSArray)
        if self.RSArray[14] != None:
            SetControl("R", self.BTNLFootR, self.BTNRFootR, self.RSArray[14], 14, self.LSArray, self.RSArray)

        if self.LSArray[15] != None:
            SetControl("L", self.BTNLToeR, self.BTNRToeR, self.LSArray[15], 15, self.LSArray, self.RSArray)
        if self.RSArray[15] != None:
            SetControl("R", self.BTNLToeR, self.BTNRToeR, self.RSArray[15], 15, self.LSArray, self.RSArray)

        '''------------------------------------------------------------------------------------------------'''

        if self.LSArray[16] != None:
            SetControl("L", self.BTNLThingL, self.BTNRThingL, self.LSArray[16], 16, self.LSArray, self.RSArray)
        if self.RSArray[16] != None:
            SetControl("R", self.BTNLThingL, self.BTNRThingL, self.RSArray[16], 16, self.LSArray, self.RSArray)

        if self.LSArray[17] != None:
            SetControl("L", self.BTNLCalfL, self.BTNRCalfL, self.LSArray[17], 17, self.LSArray, self.RSArray)
        if self.RSArray[17] != None:
            SetControl("R", self.BTNLCalfL, self.BTNRCalfL, self.RSArray[17], 17, self.LSArray, self.RSArray)

        if self.LSArray[18] != None:
            SetControl("L", self.BTNLFootL, self.BTNRFootL, self.LSArray[18], 18, self.LSArray, self.RSArray)
        if self.RSArray[18] != None:
            SetControl("R", self.BTNLFootL, self.BTNRFootL, self.RSArray[18], 18, self.LSArray, self.RSArray)

        if self.LSArray[19] != None:
            SetControl("L", self.BTNLToeL, self.BTNRToeL, self.LSArray[19], 19, self.LSArray, self.RSArray)
        if self.RSArray[19] != None:
            SetControl("R", self.BTNLToeL, self.BTNRToeL, self.RSArray[19], 19, self.LSArray, self.RSArray)

        '''------------------------------------------------------------------------------------------------'''

        if self.LSArray[20] != None:
            SetControl("L", self.BTNLArmPointR, self.BTNRArmPointR, self.LSArray[20], 20, self.LSArray, self.RSArray)
        if self.RSArray[20] != None:
            SetControl("R", self.BTNLArmPointR, self.BTNRArmPointR, self.RSArray[20], 20, self.LSArray, self.RSArray)

        if self.LSArray[21] != None:
            SetControl("L", self.BTNLArmPointL, self.BTNRArmPointL, self.LSArray[21], 21, self.LSArray, self.RSArray)
        if self.RSArray[21] != None:
            SetControl("R", self.BTNLArmPointL, self.BTNRArmPointL, self.RSArray[21], 21, self.LSArray, self.RSArray)

        if self.LSArray[22] != None:
            SetControl("L", self.BTNLLegPointR, self.BTNRLegPointR, self.LSArray[22], 22, self.LSArray, self.RSArray)
        if self.RSArray[22] != None:
            SetControl("R", self.BTNLLegPointR, self.BTNRLegPointR, self.RSArray[22], 22, self.LSArray, self.RSArray)

        if self.LSArray[23] != None:
            SetControl("L", self.BTNLLegPointL, self.BTNRLegPointL, self.LSArray[23], 23, self.LSArray, self.RSArray)
        if self.RSArray[23] != None:
            SetControl("R", self.BTNLLegPointL, self.BTNRLegPointL, self.RSArray[23], 23, self.LSArray, self.RSArray)

        self.SetTollTip()

    def ResetFile(self):
        self.LSArray = [None] * 24
        self.RSArray = [None] * 24

        self.BTNLHead.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRHead.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLHead.setToolTip("None")
        self.BTNRHead.setToolTip("None")

        self.BTNLNeck.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRNeck.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLNeck.setToolTip("None")
        self.BTNRNeck.setToolTip("None")

        self.BTNLChest.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRChest.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLChest.setToolTip("None")
        self.BTNRChest.setToolTip("None")

        self.BTNLPelvis.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRPelvis.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLPelvis.setToolTip("None")
        self.BTNRPelvis.setToolTip("None")

        '''-------------------------------------------'''

        self.BTNLClavicleR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRClavicleR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLClavicleR.setToolTip("None")
        self.BTNRClavicleR.setToolTip("None")

        self.BTNLUpperArmR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRUpperArmR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLUpperArmR.setToolTip("None")
        self.BTNRUpperArmR.setToolTip("None")

        self.BTNLLowerArmR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRLowerArmR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLLowerArmR.setToolTip("None")
        self.BTNRLowerArmR.setToolTip("None")

        self.BTNLHandR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRHandR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLHandR.setToolTip("None")
        self.BTNRHandR.setToolTip("None")

        '''-------------------------------------------'''

        self.BTNLClavicleL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRClavicleL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLClavicleL.setToolTip("None")
        self.BTNRClavicleL.setToolTip("None")

        self.BTNLUpperArmL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRUpperArmL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLUpperArmL.setToolTip("None")
        self.BTNRUpperArmL.setToolTip("None")

        self.BTNLLowerArmL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRLowerArmL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLLowerArmL.setToolTip("None")
        self.BTNRLowerArmL.setToolTip("None")

        self.BTNLHandL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRHandL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLHandL.setToolTip("None")
        self.BTNRHandL.setToolTip("None")

        '''-------------------------------------------'''

        self.BTNLThingR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRThingR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLThingR.setToolTip("None")
        self.BTNRThingR.setToolTip("None")

        self.BTNLCalfR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRCalfR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLCalfR.setToolTip("None")
        self.BTNRCalfR.setToolTip("None")

        self.BTNLFootR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRFootR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLFootR.setToolTip("None")
        self.BTNRFootR.setToolTip("None")

        self.BTNLToeR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRToeR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLToeR.setToolTip("None")
        self.BTNRToeR.setToolTip("None")

        '''-------------------------------------------'''

        self.BTNLThingL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRThingL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLThingL.setToolTip("None")
        self.BTNRThingL.setToolTip("None")

        self.BTNLCalfL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRCalfL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLCalfL.setToolTip("None")
        self.BTNRCalfL.setToolTip("None")

        self.BTNLFootL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRFootL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLFootL.setToolTip("None")
        self.BTNRFootL.setToolTip("None")

        self.BTNLToeL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRToeL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLToeL.setToolTip("None")
        self.BTNRToeL.setToolTip("None")

        '''-------------------------------------------'''

        self.BTNLArmPointR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRArmPointR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLArmPointR.setToolTip("None")
        self.BTNRArmPointR.setToolTip("None")

        self.BTNLArmPointL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRArmPointL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLArmPointL.setToolTip("None")
        self.BTNRArmPointL.setToolTip("None")

        self.BTNLLegPointR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRLegPointR.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLLegPointR.setToolTip("None")
        self.BTNRLegPointR.setToolTip("None")

        self.BTNLLegPointL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")
        self.BTNRLegPointL.setStyleSheet("QPushButton{background-color: rgba(93,93,93,255);}")

        self.BTNLLegPointL.setToolTip("None")
        self.BTNRLegPointL.setToolTip("None")

    def BatchFBX(self):
        self.RunFile("mBatch.py")

    def LimbPointDialod(self):
        self.RunFile("LimbPoint.py")

    def LimbPoint(self):
        sel = pm.ls(sl=1)

        Bone1 = sel[0]
        Bone2 = sel[1]
        Bone3 = sel[2]

        PointMatrixNode = pm.createNode("Point3Matrix")
        DecomposeNode = pm.createNode("decomposeMatrix")
        Locator = pm.spaceLocator(p=(0, 0, 0))

        pm.connectAttr(Bone1.worldMatrix[0], PointMatrixNode.Matrix1)
        pm.connectAttr(Bone2.worldMatrix[0], PointMatrixNode.Matrix2)
        pm.connectAttr(Bone3.worldMatrix[0], PointMatrixNode.Matrix3)
        pm.connectAttr(PointMatrixNode.OutputMatrix, DecomposeNode.inputMatrix)
        pm.connectAttr(DecomposeNode.outputTranslate, Locator.translate)
        pm.connectAttr(DecomposeNode.outputRotate, Locator.rotate)

        pm.setAttr(PointMatrixNode.OffsetX, 0)
        pm.setAttr(PointMatrixNode.OffsetY, 0)
        pm.setAttr(PointMatrixNode.OffsetZ, 0)

        pm.setAttr(PointMatrixNode.FlipX, False)
        pm.setAttr(PointMatrixNode.FlipY, True)
        pm.setAttr(PointMatrixNode.FlipZ, False)

    def CharacterSet(self):
        cmds.select(self.RSArray)
        self.RunFile("CharacterSet.py")

    def SelectionSet(self):
        cmds.select(self.RSArray)
        self.RunFile("SelectionSet.py")

    def SetArmsFK(self):
        if self.ArmsFK.isChecked() == True:
            self.ArmsIK.setChecked(False)
        else:
            self.ArmsIK.setChecked(True)

    def SetArmsIK(self):
        if self.ArmsIK.isChecked() == True:
            self.ArmsFK.setChecked(False)
        else:
            self.ArmsFK.setChecked(True)

    def SetLegsFK(self):
        if self.LegsFK.isChecked() == True:
            self.LegsIK.setChecked(False)
        else:
            self.LegsIK.setChecked(True)

    def SetLegsIK(self):
        if self.LegsIK.isChecked() == True:
            self.LegsFK.setChecked(False)
        else:
            self.LegsFK.setChecked(True)

    '''--------------------------------'''

    def LSSetHead(self):
        SetControl("L", self.BTNLHead, self.BTNRHead, GetName(), 0, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetHead(self):
        SetControl("R", self.BTNLHead, self.BTNRHead, GetName(), 0, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetHead_RC(self):
        RemoveControl("L", self.BTNLHead, self.BTNRHead, 0, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetHead_RC(self):
        RemoveControl("R", self.BTNLHead, self.BTNRHead, 0, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetNeck(self):
        SetControl("L", self.BTNLNeck, self.BTNRNeck, GetName(), 1, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetNeck(self):
        SetControl("R", self.BTNLNeck, self.BTNRNeck, GetName(), 1, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetNeck_RC(self):
        RemoveControl("L", self.BTNLNeck, self.BTNRNeck, 1, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetNeck_RC(self):
        RemoveControl("R", self.BTNLNeck, self.BTNRNeck, 1, self.LSArray, self.RSArray)
        self.SetTollTip()
    '''--------------------------------'''

    def LSSetChest(self):
        SetControl("L", self.BTNLChest, self.BTNRChest, GetName(), 2, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetChest(self):
        SetControl("R", self.BTNLChest, self.BTNRChest, GetName(), 2, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetChest_RC(self):
        RemoveControl("L", self.BTNLChest, self.BTNRChest, 2, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetChest_RC(self):
        RemoveControl("R", self.BTNLChest, self.BTNRChest, 2, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetPelvis(self):
        SetControl("L", self.BTNLPelvis, self.BTNRPelvis, GetName(), 3, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetPelvis(self):
        SetControl("R", self.BTNLPelvis, self.BTNRPelvis, GetName(), 3, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetPelvis_RC(self):
        RemoveControl("L", self.BTNLPelvis, self.BTNRPelvis, 3, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetPelvis_RC(self):
        RemoveControl("R", self.BTNLPelvis, self.BTNRPelvis, 3, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetClavicleR(self):
        SetControl("L", self.BTNLClavicleR, self.BTNRClavicleR, GetName(), 4, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetClavicleR(self):
        SetControl("R", self.BTNLClavicleR, self.BTNRClavicleR, GetName(), 4, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetClavicleR_RC(self):
        RemoveControl("L", self.BTNLClavicleR, self.BTNRClavicleR, 4, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetClavicleR_RC(self):
        RemoveControl("R", self.BTNLClavicleR, self.BTNRClavicleR, 4, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetUpperArmR(self):
        SetControl("L", self.BTNLUpperArmR, self.BTNRUpperArmR, GetName(), 5, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetUpperArmR(self):
        SetControl("R", self.BTNLUpperArmR, self.BTNRUpperArmR, GetName(), 5, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetUpperArmR_RC(self):
        RemoveControl("L", self.BTNLUpperArmR, self.BTNRUpperArmR, 5, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetUpperArmR_RC(self):
        RemoveControl("R", self.BTNLUpperArmR, self.BTNRUpperArmR, 5, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetLowerArmR(self):
        SetControl("L", self.BTNLLowerArmR, self.BTNRLowerArmR, GetName(), 6, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetLowerArmR(self):
        SetControl("R", self.BTNLLowerArmR, self.BTNRLowerArmR, GetName(), 6, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetLowerArmR_RC(self):
        RemoveControl("L", self.BTNLLowerArmR, self.BTNRLowerArmR, 6, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetLowerArmR_RC(self):
        RemoveControl("R", self.BTNLLowerArmR, self.BTNRLowerArmR, 6, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetHandR(self):
        SetControl("L", self.BTNLHandR, self.BTNRHandR, GetName(), 7, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetHandR(self):
        SetControl("R", self.BTNLHandR, self.BTNRHandR, GetName(), 7, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetHandR_RC(self):
        RemoveControl("L", self.BTNLHandR, self.BTNRHandR, 7, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetHandR_RC(self):
        RemoveControl("R", self.BTNLHandR, self.BTNRHandR, 7, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetClavicleL(self):
        SetControl("L", self.BTNLClavicleL, self.BTNRClavicleL, GetName(), 8, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetClavicleL(self):
        SetControl("R", self.BTNLClavicleL, self.BTNRClavicleL, GetName(), 8, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetClavicleL_RC(self):
        RemoveControl("L", self.BTNLClavicleL, self.BTNRClavicleL, 8, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetClavicleL_RC(self):
       RemoveControl("R", self.BTNLClavicleL, self.BTNRClavicleL, 8, self.LSArray, self.RSArray)
       self.SetTollTip()

    '''--------------------------------'''

    def LSSetUpperArmL(self):
        SetControl("L", self.BTNLUpperArmL, self.BTNRUpperArmL, GetName(), 9, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetUpperArmL(self):
        SetControl("R", self.BTNLUpperArmL, self.BTNRUpperArmL, GetName(), 9, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetUpperArmL_RC(self):
        RemoveControl("L", self.BTNLUpperArmL, self.BTNRUpperArmL, 9, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetUpperArmL_RC(self):
        RemoveControl("R", self.BTNLUpperArmL, self.BTNRUpperArmL, 9, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetLowerArmL(self):
        SetControl("L", self.BTNLLowerArmL, self.BTNRLowerArmL, GetName(), 10, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetLowerArmL(self):
        SetControl("R", self.BTNLLowerArmL, self.BTNRLowerArmL, GetName(), 10, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetLowerArmL_RC(self):
        RemoveControl("L", self.BTNLLowerArmL, self.BTNRLowerArmL, 10, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetLowerArmL_RC(self):
        RemoveControl("R", self.BTNLLowerArmL, self.BTNRLowerArmL, 10, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetHandL(self):
        SetControl("L", self.BTNLHandL, self.BTNRHandL, GetName(), 11, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetHandL(self):
        SetControl("R", self.BTNLHandL, self.BTNRHandL, GetName(), 11, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetHandL_RC(self):
        RemoveControl("L", self.BTNLHandL, self.BTNRHandL, 11, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetHandL_RC(self):
        RemoveControl("R", self.BTNLHandL, self.BTNRHandL, 11, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetThingR(self):
        SetControl("L", self.BTNLThingR, self.BTNRThingR, GetName(), 12, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetThingR(self):
        SetControl("R", self.BTNLThingR, self.BTNRThingR, GetName(), 12, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetThingR_RC(self):
        RemoveControl("L", self.BTNLThingR, self.BTNRThingR, 12, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetThingR_RC(self):
        RemoveControl("R", self.BTNLThingR, self.BTNRThingR, 12, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetCalfR(self):
        SetControl("L", self.BTNLCalfR, self.BTNRCalfR, GetName(), 13, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetCalfR(self):
        SetControl("R", self.BTNLCalfR, self.BTNRCalfR, GetName(), 13, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetCalfR_RC(self):
        RemoveControl("L", self.BTNLCalfR, self.BTNRCalfR, 13, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetCalfR_RC(self):
        RemoveControl("R", self.BTNLCalfR, self.BTNRCalfR, 13, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetFootR(self):
        SetControl("L", self.BTNLFootR, self.BTNRFootR, GetName(), 14, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetFootR(self):
        SetControl("R", self.BTNLFootR, self.BTNRFootR, GetName(), 14, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetFootR_RC(self):
        RemoveControl("L", self.BTNLFootR, self.BTNRFootR, 14, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetFootR_RC(self):
        RemoveControl("R", self.BTNLFootR, self.BTNRFootR, 14, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetToeR(self):
        SetControl("L", self.BTNLToeR, self.BTNRToeR, GetName(), 15, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetToeR(self):
        SetControl("R", self.BTNLToeR, self.BTNRToeR, GetName(), 15, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetToeR_RC(self):
        RemoveControl("L", self.BTNLToeR, self.BTNRToeR, 15, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetToeR_RC(self):
        RemoveControl("R", self.BTNLToeR, self.BTNRToeR, 15, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetThingL(self):
        SetControl("L", self.BTNLThingL, self.BTNRThingL, GetName(), 16, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetThingL(self):
        SetControl("R", self.BTNLThingL, self.BTNRThingL, GetName(), 16, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetThingL_RC(self):
        RemoveControl("L", self.BTNLThingL, self.BTNRThingL, 16, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetThingL_RC(self):
        RemoveControl("R", self.BTNLThingL, self.BTNRThingL, 16, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetCalfL(self):
        SetControl("L", self.BTNLCalfL, self.BTNRCalfL, GetName(), 17, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetCalfL(self):
        SetControl("R", self.BTNLCalfL, self.BTNRCalfL, GetName(), 17, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetCalfL_RC(self):
        RemoveControl("L", self.BTNLCalfL, self.BTNRCalfL, 17, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetCalfL_RC(self):
        RemoveControl("R", self.BTNLCalfL, self.BTNRCalfL, 17, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetFootL(self):
        SetControl("L", self.BTNLFootL, self.BTNRFootL, GetName(), 18, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetFootL(self):
        SetControl("R", self.BTNLFootL, self.BTNRFootL, GetName(), 18, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetFootL_RC(self):
        RemoveControl("L", self.BTNLFootL, self.BTNRFootL, 18, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetFootL_RC(self):
        RemoveControl("R", self.BTNLFootL, self.BTNRFootL, 18, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetToeL(self):
        SetControl("L", self.BTNLToeL, self.BTNRToeL, GetName(), 19, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetToeL(self):
        SetControl("R", self.BTNLToeL, self.BTNRToeL, GetName(), 19, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetToeL_RC(self):
        RemoveControl("L", self.BTNLToeL, self.BTNRToeL, 19, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetToeL_RC(self):
        RemoveControl("R", self.BTNLToeL, self.BTNRToeL, 19, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetArmPointR(self):
        SetControl("L", self.BTNLArmPointR, self.BTNRArmPointR, GetName(), 20, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetArmPointR(self):
        SetControl("R", self.BTNLArmPointR, self.BTNRArmPointR, GetName(), 20, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetArmPointR_RC(self):
        RemoveControl("L", self.BTNLArmPointR, self.BTNRArmPointR, 20, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetArmPointR_RC(self):
        RemoveControl("R", self.BTNLArmPointR, self.BTNRArmPointR, 20, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetArmPointL(self):
        SetControl("L", self.BTNLArmPointL, self.BTNRArmPointL, GetName(), 21, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetArmPointL(self):
        SetControl("R", self.BTNLArmPointL, self.BTNRArmPointL, GetName(), 21, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetArmPointL_RC(self):
        RemoveControl("L", self.BTNLArmPointL, self.BTNRArmPointL, 21, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetArmPointL_RC(self):
        RemoveControl("R", self.BTNLArmPointL, self.BTNRArmPointL, 21, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetLegPointR(self):
        SetControl("L", self.BTNLLegPointR, self.BTNRLegPointR, GetName(), 22, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetLegPointR(self):
        SetControl("R", self.BTNLLegPointR, self.BTNRLegPointR, GetName(), 22, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetLegPointR_RC(self):
        RemoveControl("L", self.BTNLLegPointR, self.BTNRLegPointR, 22, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetLegPointR_RC(self):
        RemoveControl("R", self.BTNLLegPointR, self.BTNRLegPointR, 22, self.LSArray, self.RSArray)
        self.SetTollTip()

    '''--------------------------------'''

    def LSSetLegPointL(self):
        SetControl("L", self.BTNLLegPointL, self.BTNRLegPointL, GetName(), 23, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetLegPointL(self):
        SetControl("R", self.BTNLLegPointL, self.BTNRLegPointL, GetName(), 23, self.LSArray, self.RSArray)
        self.SetTollTip()

    def LSSetLegPointL_RC(self):
        RemoveControl("L", self.BTNLLegPointL, self.BTNRLegPointL, 23, self.LSArray, self.RSArray)
        self.SetTollTip()

    def RSSetLegPointL_RC(self):
        RemoveControl("R", self.BTNLLegPointL, self.BTNRLegPointL, 23, self.LSArray, self.RSArray)
        self.SetTollTip()


mRetargetCore = MRetarget()
mRetargetCore.show()