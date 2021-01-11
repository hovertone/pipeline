import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math

class Limb_Lock(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x424dd878)

    aOutput = OpenMaya.MObject()
    aOffset = OpenMaya.MObject()
    aHOffset = OpenMaya.MObject()
    aTOffset = OpenMaya.MObject()
    aRadius = OpenMaya.MObject()
    aFootBank = OpenMaya.MObject()
    aTM = OpenMaya.MObject()

    #------------ Functions Block ------------#

    def normalizeWeight(self, radius, value):
        if radius == 0.0:
            radius = 0.001
        if value == 0.0:
            value = 0.001

        Weight = 1.0 - 1.0 / (radius / value)
        return Weight

    def vectorLerp(self, aVec, bVec, weight):
        lVec = (aVec*(1-weight) + bVec*weight).normal()
        return lVec

    # ----------------------------------------#

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data):
        if plug != Limb_Lock.aOutput:
            return OpenMaya.kUnknownParameter

        offset = data.inputValue(self.aOffset).asFloat()
        heelOffset = data.inputValue(self.aHOffset).asFloat()
        toeOffset = data.inputValue(self.aTOffset).asFloat()
        radius = data.inputValue(self.aRadius).asFloat()
        footBank = data.inputValue(self.aFootBank).asBool()
        inMatrix = data.inputValue(self.aTM).asMatrix()

        util = OpenMaya.MScriptUtil()

        # ------------ Create Offset Matrix -------------#

        offsetMatrix = OpenMaya.MMatrix()
        offsetMatrixList = [1, 0, 0, 0,
                            0, 1, 0, 0,
                            0, 0, 1, 0,
                            0, -offset, 0, 1]
        util.createMatrixFromList(offsetMatrixList, offsetMatrix)

        # ------------ Create Heel Matrix -------------#

        heelMatrix = OpenMaya.MMatrix()
        heelMatrixList = [1, 0, 0, 0,
                          0, 1, 0, 0,
                          0, 0, 1, 0,
                          0, -heelOffset, 0, 1]
        util.createMatrixFromList(heelMatrixList, heelMatrix)

        # -------------- Create Toe Matrix --------------#

        toeMatrix = OpenMaya.MMatrix()
        toeMatrixList = [1, 0, 0, 0,
                         0, 1, 0, 0,
                         0, 0, 1, 0,
                         0, 0, toeOffset, 1]
        util.createMatrixFromList(toeMatrixList, toeMatrix)

        # -------------- Create Positions ---------------#

        TM = inMatrix * offsetMatrix
        hTM = heelMatrix * TM
        tTM = toeMatrix * heelMatrix * TM

        hPos = OpenMaya.MVector(hTM(3, 0), hTM(3, 1), hTM(3, 2))
        tPos = OpenMaya.MVector(tTM(3, 0), tTM(3, 1), tTM(3, 2))

        # --------------- Limit Positions ---------------#

        if hPos.y < 0:
            heelPos = OpenMaya.MVector(hPos.x, 0, hPos.z)
        else:
            heelPos = hPos

        if tPos.y < 0:
            toePos = OpenMaya.MVector(tPos.x, 0, tPos.z)
        else:
            toePos = tPos

        # ----------- Compute Matrix Vectors ------------#

        if footBank == True:
            Xo = OpenMaya.MVector(TM(0, 0), TM(0, 1), TM(0, 2))

            Z = (heelPos - toePos).normal()
            Y = (Xo ^ Z).normal()
            X = (Z ^ Y).normal()
        else:
            ND_1 = self.normalizeWeight(radius, heelPos.y)
            ND_2 = self.normalizeWeight(radius, toePos.y)
            weight = (ND_1 + ND_2)/2

            Xo = OpenMaya.MVector(TM(0, 0), TM(0, 1), TM(0, 2))

            #-----------------------------#

            Yup = OpenMaya.MVector(0, 1, 0)

            Z = (heelPos - toePos).normal()

            Xv = Z ^ Yup
            if weight > 0:
                X = self.vectorLerp(Xo, Xv, weight)
            else:
                X = Xo

            Y = (X ^ Z).normal()

        # ------------ Compose Matrix -------------#

        commposeMatrix = OpenMaya.MMatrix()
        commposeMatrixList = [X.x, X.y, X.z, 0,
                              Y.x, Y.y, Y.z, 0,
                              Z.x, Z.y, Z.z, 0,
                              heelPos.x, heelPos.y, heelPos.z, 1]
        util.createMatrixFromList(commposeMatrixList, commposeMatrix)

        # ----------------------------------------------#

        outMatrix = commposeMatrix * offsetMatrix.inverse()

        # ----------------------------------------------#

        OutputTM = data.outputValue(Limb_Lock.aOutput)
        OutputTM.setMMatrix(outMatrix)
        OutputTM.setClean()
        data.setClean(plug)

def creator():
    return OpenMayaMPx.asMPxPtr(Limb_Lock())

def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()

    Limb_Lock.aOutput = mAttr.create('OutputMatrix', 'outM')
    Limb_Lock.addAttribute(Limb_Lock.aOutput)

    Limb_Lock.aOffset = nAttr.create('Offset', 'Offset', OpenMaya.MFnNumericData.kFloat, 0)
    nAttr.setKeyable(True)
    Limb_Lock.addAttribute(Limb_Lock.aOffset)

    Limb_Lock.aHOffset = nAttr.create('HeelOffset', 'HeelOffset', OpenMaya.MFnNumericData.kFloat, 10)
    nAttr.setKeyable(True)
    Limb_Lock.addAttribute(Limb_Lock.aHOffset)

    Limb_Lock.aTOffset = nAttr.create('ToeOffset', 'ToeOffset', OpenMaya.MFnNumericData.kFloat, 20)
    nAttr.setKeyable(True)
    Limb_Lock.addAttribute(Limb_Lock.aTOffset)

    Limb_Lock.aRadius = nAttr.create('Radius', 'Radius', OpenMaya.MFnNumericData.kFloat, 5)
    nAttr.setKeyable(True)
    Limb_Lock.addAttribute(Limb_Lock.aRadius)

    Limb_Lock.aFootBank = nAttr.create("FootBank", "FootBank", OpenMaya.MFnNumericData.kBoolean, 0)
    nAttr.setKeyable(True)
    Limb_Lock.addAttribute(Limb_Lock.aFootBank)

    Limb_Lock.aTM = mAttr.create('InputMatrix', 'InputMatrix')
    Limb_Lock.addAttribute(Limb_Lock.aTM)

    Limb_Lock.attributeAffects(Limb_Lock.aOffset, Limb_Lock.aOutput)
    Limb_Lock.attributeAffects(Limb_Lock.aHOffset, Limb_Lock.aOutput)
    Limb_Lock.attributeAffects(Limb_Lock.aTOffset, Limb_Lock.aOutput)
    Limb_Lock.attributeAffects(Limb_Lock.aRadius, Limb_Lock.aOutput)
    Limb_Lock.attributeAffects(Limb_Lock.aFootBank, Limb_Lock.aOutput)
    Limb_Lock.attributeAffects(Limb_Lock.aTM, Limb_Lock.aOutput)

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "Maxim Vodolazskiy", "1.0", "Any")
    plugin.registerNode("Limb_Lock", Limb_Lock.kPluginNodeId, creator, initialize)

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    plugin.deregisterNode(Limb_Lock.kPluginNodeId)