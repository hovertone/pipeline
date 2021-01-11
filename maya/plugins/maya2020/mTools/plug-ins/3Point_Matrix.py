import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math

class Point3_Matrix(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x12365478)

    mOutput = OpenMaya.MObject()
    OffsetX = OpenMaya.MObject()
    OffsetY = OpenMaya.MObject()
    OffsetZ = OpenMaya.MObject()
    aX = OpenMaya.MObject()
    aY = OpenMaya.MObject()
    aZ = OpenMaya.MObject()
    aTM1 = OpenMaya.MObject()
    aTM2 = OpenMaya.MObject()
    aTM3 = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data):
        if plug != Point3_Matrix.mOutput:
            return OpenMaya.kUnknownParameter

        XOffset = data.inputValue(self.OffsetX).asFloat()
        YOffset = data.inputValue(self.OffsetY).asFloat()
        ZOffset = data.inputValue(self.OffsetZ).asFloat()

        XBool = data.inputValue(self.aX).asBool()
        YBool = data.inputValue(self.aY).asBool()
        ZBool = data.inputValue(self.aZ).asBool()

        TM1 = data.inputValue(self.aTM1).asMatrix()
        TM2 = data.inputValue(self.aTM2).asMatrix()
        TM3 = data.inputValue(self.aTM3).asMatrix()

        MT1 = OpenMaya.MTransformationMatrix(TM1)
        MT2 = OpenMaya.MTransformationMatrix(TM2)
        MT3 = OpenMaya.MTransformationMatrix(TM3)

        V1 = MT1.translation(OpenMaya.MSpace.kWorld)
        V2 = MT2.translation(OpenMaya.MSpace.kWorld)
        V3 = MT3.translation(OpenMaya.MSpace.kWorld)

        ITM = OpenMaya.MTransformationMatrix(TM3*TM1.inverse())
        Pos = ITM.translation(OpenMaya.MSpace.kWorld)

        if XBool == 1:
            if Pos.x >= 0:
                AxisX = -1
            else:
                AxisX = 1
        else:
            AxisX = 1

        if YBool == 1:
            if Pos.y >= 0:
                AxisY = -1
            else:
                AxisY = 1
        else:
            AxisY = 1

        if ZBool == 1:
            if Pos.z >= 0:
                AxisZ = -1
            else:
                AxisZ = 1
        else:
            AxisZ = 1

        B1_Length = (V1 - V2).length()
        B2_Length = (V2 - V3).length()

        Dir1 = (V3 - V1).normal()
        Dir2 = (V1 - V3).normal()

        Avarenge = ((Dir1 * B1_Length + V1) + (Dir2 * B2_Length + V3)) / 2

        Row1 = (V2 - Avarenge).normal()*AxisX*AxisY*AxisZ
        Row2 = ((V2 - V1) ^ (V3 - V1)).normal()*AxisX*AxisY*AxisZ
        Row3 = (Row1 ^ Row2).normal()*AxisX*AxisY*AxisZ

        util = OpenMaya.MScriptUtil()

        newMatrix = OpenMaya.MMatrix()
        NmatrixList = [Row1[0], Row1[1], Row1[2], 0, Row2[0], Row2[1], Row2[2], 0, Row3[0], Row3[1], Row3[2], 0, V2[0], V2[1], V2[2], 1]
        util.createMatrixFromList(NmatrixList, newMatrix)

        zeroMatrix = OpenMaya.MMatrix()
        ZmatrixList = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, XOffset, YOffset, ZOffset, 1]
        util.createMatrixFromList(ZmatrixList, zeroMatrix)

        OutputTM = data.outputValue(Point3_Matrix.mOutput)
        OutputTM.setMMatrix(zeroMatrix*newMatrix)
        OutputTM.setClean()
        data.setClean(plug)

def creator():
    return OpenMayaMPx.asMPxPtr(Point3_Matrix())

def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    Point3_Matrix.mOutput = mAttr.create('OutputMatrix', 'outM')
    Point3_Matrix.addAttribute(Point3_Matrix.mOutput)

    Point3_Matrix.OffsetX = nAttr.create('OffsetX', 'OffsetX', OpenMaya.MFnNumericData.kFloat, 0)
    nAttr.setKeyable(True)
    Point3_Matrix.addAttribute(Point3_Matrix.OffsetX)

    Point3_Matrix.OffsetY = nAttr.create('OffsetY', 'OffsetY', OpenMaya.MFnNumericData.kFloat, 0)
    nAttr.setKeyable(True)
    Point3_Matrix.addAttribute(Point3_Matrix.OffsetY)

    Point3_Matrix.OffsetZ = nAttr.create('OffsetZ', 'OffsetZ', OpenMaya.MFnNumericData.kFloat, 0)
    nAttr.setKeyable(True)
    Point3_Matrix.addAttribute(Point3_Matrix.OffsetZ)

    Point3_Matrix.aX = nAttr.create("FlipX", "FlipX", OpenMaya.MFnNumericData.kBoolean, 0)
    nAttr.setKeyable(True)
    Point3_Matrix.addAttribute(Point3_Matrix.aX)

    Point3_Matrix.aY = nAttr.create("FlipY", "FlipY", OpenMaya.MFnNumericData.kBoolean, 1)
    nAttr.setKeyable(True)
    Point3_Matrix.addAttribute(Point3_Matrix.aY)

    Point3_Matrix.aZ = nAttr.create("FlipZ", "FlipZ", OpenMaya.MFnNumericData.kBoolean, 0)
    nAttr.setKeyable(True)
    Point3_Matrix.addAttribute(Point3_Matrix.aZ)

    Point3_Matrix.aTM1 = mAttr.create('Matrix1', 'M1')
    Point3_Matrix.addAttribute(Point3_Matrix.aTM1)

    Point3_Matrix.aTM2 = mAttr.create('Matrix2', 'M2')
    Point3_Matrix.addAttribute(Point3_Matrix.aTM2)

    Point3_Matrix.aTM3 = mAttr.create('Matrix3', 'M3')
    Point3_Matrix.addAttribute(Point3_Matrix.aTM3)

    Point3_Matrix.attributeAffects(Point3_Matrix.OffsetX, Point3_Matrix.mOutput)
    Point3_Matrix.attributeAffects(Point3_Matrix.OffsetY, Point3_Matrix.mOutput)
    Point3_Matrix.attributeAffects(Point3_Matrix.OffsetZ, Point3_Matrix.mOutput)
    Point3_Matrix.attributeAffects(Point3_Matrix.aX, Point3_Matrix.mOutput)
    Point3_Matrix.attributeAffects(Point3_Matrix.aY, Point3_Matrix.mOutput)
    Point3_Matrix.attributeAffects(Point3_Matrix.aZ, Point3_Matrix.mOutput)
    Point3_Matrix.attributeAffects(Point3_Matrix.aTM1, Point3_Matrix.mOutput)
    Point3_Matrix.attributeAffects(Point3_Matrix.aTM2, Point3_Matrix.mOutput)
    Point3_Matrix.attributeAffects(Point3_Matrix.aTM3, Point3_Matrix.mOutput)

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "Maxim Vodolazskiy", "1.0", "Any")
    plugin.registerNode("Point3Matrix", Point3_Matrix.kPluginNodeId, creator, initialize)

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    plugin.deregisterNode(Point3_Matrix.kPluginNodeId)