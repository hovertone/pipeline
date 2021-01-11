import MUI.MaxUI as mui
reload (mui)
import PySide2.QtGui as qg
import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
import pymel.core as pm

class LimbPoint(qw.QDialog):

    def __init__(self):
        qw.QDialog.__init__(self)

        '''--------Window--------'''

        mui.Window(W=self, Titel="Limb Point", Width=135, Height=185)

        mui.GroupeBox(W=self, Name="Offset", Pos=[5, 5], Width=125, Height=93)

        mui.Label(W=self, Text="Offset X:", Pos=[15, 23])
        self.OffsetX = mui.Spinner(W=self, Pos=[65, 20], Width=55, Height=20, Range="(-999999, 999999)", Value=0)

        mui.Label(W=self, Text="Offset Y:", Pos=[15, 47])
        self.OffsetY = mui.Spinner(W=self, Pos=[65, 45], Width=55, Height=20, Range="(-999999, 999999)", Value=0)

        mui.Label(W=self, Text="Offset Z:", Pos=[15, 73])
        self.OffsetZ = mui.Spinner(W=self, Pos=[65, 70], Width=55, Height=20, Range="(-999999, 999999)", Value=0)

        mui.GroupeBox(W=self, Name="Flip", Pos=[5, 98], Width=125, Height=50)

        self.FlipX = mui.CheckBox(W=self, Name="X", Pos=[15, 118])
        self.FlipY = mui.CheckBox(W=self, Name="Y", Pos=[55, 118], State=True)
        self.FlipZ = mui.CheckBox(W=self, Name="Z", Pos=[95, 118])

        self.CreateBTN = mui.Button(W=self, Name="Create", Pos=[5, 155], Width=125, Height=25)

        self.CreateBTN.clicked.connect(self.CreatePoint)

    def CreatePoint(self):
        sel = pm.ls(sl=1)

        Bone1 = sel[0]
        Bone2 = sel[1]
        Bone3 = sel[2]

        XOffset = 45

        PointMatrixNode = pm.createNode("Point3Matrix")
        DecomposeNode = pm.createNode("decomposeMatrix")
        Locator = pm.spaceLocator(p=(0, 0, 0))

        pm.connectAttr(Bone1.worldMatrix[0], PointMatrixNode.Matrix1)
        pm.connectAttr(Bone2.worldMatrix[0], PointMatrixNode.Matrix2)
        pm.connectAttr(Bone3.worldMatrix[0], PointMatrixNode.Matrix3)
        pm.connectAttr(PointMatrixNode.OutputMatrix, DecomposeNode.inputMatrix)
        pm.connectAttr(DecomposeNode.outputTranslate, Locator.translate)
        pm.connectAttr(DecomposeNode.outputRotate, Locator.rotate)

        pm.setAttr(PointMatrixNode.OffsetX, self.OffsetX.value())
        pm.setAttr(PointMatrixNode.OffsetY, self.OffsetY.value())
        pm.setAttr(PointMatrixNode.OffsetZ, self.OffsetZ.value())

        pm.setAttr(PointMatrixNode.FlipX, self.FlipX.isChecked())
        pm.setAttr(PointMatrixNode.FlipY, self.FlipY.isChecked())
        pm.setAttr(PointMatrixNode.FlipZ, self.FlipZ.isChecked())

dialog = LimbPoint()
dialog.show()