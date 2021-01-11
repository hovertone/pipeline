import maya.cmds as cmds
import pymel.core as pm

sel = pm.ls(sl=True, l=True)[0]

'''--- create root ---'''

rootNode = pm.ls(sl=True)[0]

cLocator = cmds.CreateLocator(p=(0, 0, 0))
locName = rootName + "_origin"
oLocator = cmds.rename(cLocator, locName)

cmds.setAttr(oLocator + ".localScaleX", 30)
cmds.setAttr(oLocator + ".localScaleY", 30)
cmds.setAttr(oLocator + ".localScaleZ", 30)

cmds.parent(str(rootNode), oLocator)

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

'''--- left leg limb point ---'''

PointMatrixNode = pm.createNode("Point3Matrix")
DecomposeNode = pm.createNode("decomposeMatrix")
cmds.spaceLocator(n="left_Leg_LP")

pm.connectAttr(cLeftUpLeg + ".worldMatrix[0]", PointMatrixNode.Matrix1)
pm.connectAttr(cLeftLeg + ".worldMatrix[0]", PointMatrixNode.Matrix2)
pm.connectAttr(cLeftFoot + ".worldMatrix[0]", PointMatrixNode.Matrix3)
pm.connectAttr(PointMatrixNode.OutputMatrix, DecomposeNode.inputMatrix)
pm.connectAttr(DecomposeNode.outputTranslate, "left_Leg_LP.translate")
pm.connectAttr(DecomposeNode.outputRotate, "left_Leg_LP.rotate")

pm.setAttr(PointMatrixNode.OffsetX, -30)
pm.setAttr(PointMatrixNode.OffsetY, 0)
pm.setAttr(PointMatrixNode.OffsetZ, 0)

pm.setAttr(PointMatrixNode.FlipX, False)
pm.setAttr(PointMatrixNode.FlipY, True)
pm.setAttr(PointMatrixNode.FlipZ, False)

cmds.setAttr("left_Leg_LP.localScaleX", 5)
cmds.setAttr("left_Leg_LP.localScaleY", 5)
cmds.setAttr("left_Leg_LP.localScaleZ", 5)


cmds.parent("left_Leg_LP", oLocator)

'''--- right leg trasformations ---'''

cRightUpLeg = str(charNodes[27])
cmds.setAttr(cRightUpLeg + ".rotateZ", -3)

cRightLeg = str(charNodes[26])
cmds.setAttr(cRightLeg + ".rotateZ", 6)

cRightFoot = str(charNodes[25])
cmds.setAttr(cRightFoot + ".rotateZ", -3)

'''--- left leg limb point ---'''

PointMatrixNode = pm.createNode("Point3Matrix")
DecomposeNode = pm.createNode("decomposeMatrix")
cmds.spaceLocator(n="right_Leg_LP")

pm.connectAttr(cRightUpLeg + ".worldMatrix[0]", PointMatrixNode.Matrix1)
pm.connectAttr(cRightLeg + ".worldMatrix[0]", PointMatrixNode.Matrix2)
pm.connectAttr(cRightFoot + ".worldMatrix[0]", PointMatrixNode.Matrix3)
pm.connectAttr(PointMatrixNode.OutputMatrix, DecomposeNode.inputMatrix)
pm.connectAttr(DecomposeNode.outputTranslate, "right_Leg_LP.translate")
pm.connectAttr(DecomposeNode.outputRotate, "right_Leg_LP.rotate")

pm.setAttr(PointMatrixNode.OffsetX, -30)
pm.setAttr(PointMatrixNode.OffsetY, 0)
pm.setAttr(PointMatrixNode.OffsetZ, 0)

pm.setAttr(PointMatrixNode.FlipX, False)
pm.setAttr(PointMatrixNode.FlipY, True)
pm.setAttr(PointMatrixNode.FlipZ, False)

cmds.setAttr("right_Leg_LP.localScaleX", 5)
cmds.setAttr("right_Leg_LP.localScaleY", 5)
cmds.setAttr("right_Leg_LP.localScaleZ", 5)

cmds.parent("right_Leg_LP", oLocator)

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
    nodeFP = cmds.polyPlane(n="Floor_Plane", w=500, h=500, sx=1, sy=1)

'''--- left leg setup ---'''

leftFootPos = cmds.xform(cLeftFoot, q=True, t=True, ws=True)

LM_LL_locator = cmds.spaceLocator(n="left_Main_LL")
cmds.setAttr("left_Main_LL.translate", leftFootPos[0], leftFootPos[1], leftFootPos[2])
cmds.setAttr("left_Main_LL.localScale", 5, 5, 5)
cmds.parentConstraint(cLeftFoot, "left_Main_LL", mo=True)

LC_LL_locator = cmds.spaceLocator(n="left_Contact_LL")
cmds.setAttr("left_Contact_LL.translate", leftFootPos[0], 0, leftFootPos[2])
cmds.setAttr("left_Contact_LL.localScale", 5, 5, 5)

LimbLockNode = pm.createNode("Limb_Lock")
DecomposeNode = pm.createNode("decomposeMatrix")
pm.connectAttr("left_Main_LL.worldMatrix[0]", LimbLockNode.InputMatrix)
pm.connectAttr("Floor_Plane.translateY", LimbLockNode.Offset)
pm.connectAttr(LimbLockNode.OutputMatrix, DecomposeNode.inputMatrix)
pm.connectAttr(DecomposeNode.outputTranslate, "left_Contact_LL.translate")
pm.connectAttr(DecomposeNode.outputRotate, "left_Contact_LL.rotate")

cmds.parent(LM_LL_locator, oLocator)
cmds.parent(LC_LL_locator, oLocator)

'''--- left leg setup ---'''

rightFootPos = cmds.xform(cRightFoot, q=True, t=True, ws=True)

RM_LL_locator = cmds.spaceLocator(n="right_Main_LL")
cmds.setAttr("right_Main_LL.translate", rightFootPos[0], rightFootPos[1], rightFootPos[2])
cmds.setAttr("right_Main_LL.localScale", 5, 5, 5)
cmds.parentConstraint(cRightFoot, "right_Main_LL", mo=True)

RC_LL_locator = cmds.spaceLocator(n="right_Contact_LL")
cmds.setAttr("right_Contact_LL.translate", rightFootPos[0], 0, rightFootPos[2])
cmds.setAttr("right_Contact_LL.localScale", 5, 5, 5)

LimbLockNode = pm.createNode("Limb_Lock")
DecomposeNode = pm.createNode("decomposeMatrix")
pm.connectAttr("right_Main_LL.worldMatrix[0]", LimbLockNode.InputMatrix)
pm.connectAttr("Floor_Plane.translateY", LimbLockNode.Offset)
pm.connectAttr(LimbLockNode.OutputMatrix, DecomposeNode.inputMatrix)
pm.connectAttr(DecomposeNode.outputTranslate, "right_Contact_LL.translate")
pm.connectAttr(DecomposeNode.outputRotate, "right_Contact_LL.rotate")

cmds.parent(RM_LL_locator, oLocator)
cmds.parent(RC_LL_locator, oLocator)
