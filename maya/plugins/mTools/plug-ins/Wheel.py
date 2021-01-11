import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import math

class mWheel(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x5edbd3db)

    mOutput = OpenMaya.MObject()
    mRootNode = OpenMaya.MObject()
    mDirectionNode = OpenMaya.MObject()
    mScaleNode = OpenMaya.MObject()
    mToggle = OpenMaya.MObject()
    mOffset = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        self._initialized = False
        self._lastPosition = OpenMaya.MPoint()
        self._distance = float()

    def compute(self, plug, data):
        if plug != mWheel.mOutput:
            return OpenMaya.kUnknownParameter

        RootNode = OpenMaya.MPoint(data.inputValue(self.mRootNode).asFloatVector())
        DirectionNode = OpenMaya.MPoint(data.inputValue(self.mDirectionNode).asFloatVector())
        ScaleNode = OpenMaya.MPoint(data.inputValue(self.mScaleNode).asFloatVector())
        Toggle = data.inputValue(self.mToggle).asBool()
        Offset = (data.inputValue(self.mOffset).asAngle()).asDegrees()
        Pi = 3.14

        if not self._initialized:
            self._lastPosition = RootNode
            self._lastDot = 1.0
            self._initialized = True

        sRadius = (DirectionNode - ScaleNode).length() / 2

        if Toggle == 1:
            V1 = (DirectionNode - RootNode).normal()
            V2 = (RootNode - self._lastPosition).normal()
            Dot = V1 * V2

            if Dot > 0:
                self._distance += (self._lastPosition - RootNode).length()
            else:
                self._distance -= (self._lastPosition - RootNode).length()

            self._lastPosition = RootNode
            self._lastDot = Dot

            Val = (self._distance * Pi) / (Pi * sRadius) + (Pi * Offset / 180.0)
        else:
            Val = (self._distance * Pi) / (Pi * sRadius) + (Pi * Offset / 180.0)

        OutputVal = data.outputValue(mWheel.mOutput)
        OutputVal.setMAngle(OpenMaya.MAngle(Val))
        OutputVal.setClean()
        data.setClean(plug)

def creator():
    return OpenMayaMPx.asMPxPtr(mWheel())

def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    uAttr = OpenMaya.MFnUnitAttribute()

    mWheel.mOutput = uAttr.create("output", "output", OpenMaya.MFnUnitAttribute.kAngle)
    mWheel.addAttribute(mWheel.mOutput)

    mWheel.mRootNode = nAttr.createPoint("root", "root")
    mWheel.addAttribute(mWheel.mRootNode)

    mWheel.mDirectionNode = nAttr.createPoint("direction", "direction")
    mWheel.addAttribute(mWheel.mDirectionNode)

    mWheel.mScaleNode = nAttr.createPoint("scale", "scale")
    mWheel.addAttribute(mWheel.mScaleNode)

    mWheel.mToggle = nAttr.create("toggle", "toggle", OpenMaya.MFnNumericData.kBoolean, 1)
    nAttr.setKeyable(True)
    mWheel.addAttribute(mWheel.mToggle)

    mWheel.mOffset = uAttr.create("offset", "offset", OpenMaya.MFnUnitAttribute.kAngle, 0)
    uAttr.setKeyable(True)
    mWheel.addAttribute(mWheel.mOffset)

    mWheel.attributeAffects(mWheel.mDirectionNode, mWheel.mOutput)
    mWheel.attributeAffects(mWheel.mRootNode, mWheel.mOutput)
    mWheel.attributeAffects(mWheel.mToggle, mWheel.mOutput)
    mWheel.attributeAffects(mWheel.mOffset, mWheel.mOutput)

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "Maxim Vodolazskiy", "1.0", "Any")
    plugin.registerNode("mWheel", mWheel.kPluginNodeId, creator, initialize)

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    plugin.deregisterNode(mWheel.kPluginNodeId)