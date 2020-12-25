"""
Shifter's Component guide class.
"""

from functools import partial

import maya.cmds as cmds
# pyMel
import pymel.core as pm
from pymel.core import datatypes

# mgear
import mgear

from mgear.core import string

from mgear.core import dag, vector, transform, applyop, attribute, icon

from mgear.shifter import guide, guide_manager
from . import chain_guide_initializer

import main_settings_ui as msui

from mgear.vendor.Qt import QtWidgets, QtCore

##########################################################
# COMPONENT GUIDE
##########################################################


class ComponentGuide(guide.Main):
    """Main class for component guide creation.

    This class handles all the parameters and objectDefs creation.
    It also know how to parse its own hierachy of object to retrieve position
    and transform.
    Finally it also now how to export itself as xml_node.

    Attributes:
        paramNames (list): List of parameter name cause it's actually important
            to keep them sorted.
        paramDefs (dic): Dictionary of parameter definition.
        values (dic): Dictionary of options values.
        valid (bool): We will check a few things and make sure the guide we are
            loading is up to date.
            If parameters or object are missing a warning message will be
                display and the guide should be updated.
        tra (dic): dictionary of global transform
        atra (list): list of global transform
        pos (dic): dictionary of global postion
        apos (list): list of global position
        prim (dic): dictionary of primitive
        blades (dic): dictionary of blades
        size (float): Size reference of the component. Default = .1
        save_transform (list): Transform of object name in this list will
            be saved
        save_primitive (list): Primitive of object name in this list will
            be saved
        save_blade (list): Normal and BiNormal of object will be saved
        minmax (dic): Define the min and max object for multi location objects

    """
    compType = "component"  # Component type
    compName = "component"  # Component default name
    compSide = "C"
    compIndex = 0  # Component default index

    description = ""  # Description of the component

    connectors = []
    compatible = []
    ctl_grp = ""

    # ====================================================
    # Init method.
    def __init__(self):

        # Parameters names, definition and values.
        # List of parameter name cause it's actually important to keep
        # them sorted.
        self.paramNames = []
        # Dictionary of parameter definition.
        self.paramDefs = {}
        # Dictionary of options values.
        self.values = {}

        # We will check a few things and make sure the guide we are loading is
        # up to date.
        # If parameters or object are missing a warning message will be display
        # and the guide should be updated.
        self.valid = True

        self.root = None
        self.id = None

        # parent component identification
        self.parentComponent = None
        self.parentLocalName = None

        # direct child components
        self.child_components = []

        # List and dictionary used during the creation of the component
        self.tra = {}  # dictionary of global transform
        self.atra = []  # list of global transform
        self.pos = {}  # dictionary of global postion
        self.apos = []  # list of global position
        self.prim = {}  # dictionary of primitive
        self.blades = {}
        self.size = .1
        # self.root_size = None

        # List and dictionary used to define data of the guide that
        # should be saved
        # Transform of object name in this list will be saved
        self.save_transform = []
        # Primitive of object name in this list will be saved
        self.save_primitive = []
        # Normal and BiNormal of object will be saved
        self.save_blade = []
        # Define the min and max object for multi location objects
        self.minmax = {}

        # Init the guide
        self.postInit()
        self.initialHierarchy()
        self.addParameters()

    def postInit(self):
        """Define the objects name and categories.

        Note:
            REIMPLEMENT. This method should be reimplemented in each component.

        """
        self.save_transform = ["root"]
        return

    # ====================================================
    # OBJECTS AND PARAMETERS

    def initialHierarchy(self):
        """Initial hierachy.

         It's no more than the basic set of parameters and layout
         needed for the setting property.

        """
        # Parameters --------------------------------------
        # This are the necessary parameter for component guide definition
        self.pCompType = self.addParam("comp_type", "string", self.compType)
        self.pCompName = self.addParam("comp_name", "string", self.compName)
        self.pCompSide = self.addParam("comp_side", "string", self.compSide)
        self.pCompIndex = self.addParam(
            "comp_index", "long", self.compIndex, 0)
        self.pConnector = self.addParam("connector", "string", "standard")
        self.pUIHost = self.addParam("ui_host", "string", "")
        self.pCtlGroup = self.addParam("ctlGrp", "string", "")

        # Items -------------------------------------------
        typeItems = [self.compType, self.compType]
        for type in self.compatible:
            typeItems.append(type)
            typeItems.append(type)

        connectorItems = ["standard", "standard"]
        for item in self.connectors:
            connectorItems.append(item)
            connectorItems.append(item)

    def addObjects(self):
        """Create the objects of the guide.

        Note:
            REIMPLEMENT. This method should be reimplemented in each component.

        """
        self.root = self.addRoot()

    def addParameters(self):
        """Create the parameter definitions of the guide.

        Note:
            REIMPLEMENT. This method should be reimplemented in each component.

        """
        return

    def get_divisions(self):
        """Get the divisions to sample a Fcurve parameter definition.

        Note:
            REIMPLEMENT. This method should only if the component is using
            Fcurve paramDef.

        """
        return

    # ====================================================
    # SET / GET
    def setFromHierarchy(self, root):
        """Set the component guide from given hierarchy.

        Args:
            root (dagNode): The root of the hierarchy to parse.

        """
        self.root = root
        self.model = self.root.getParent(generations=-1)

        # ---------------------------------------------------
        # First check and set the settings
        if not self.root.hasAttr("comp_type"):
            mgear.log("%s is not a proper guide." %
                      self.root.longName(), mgear.sev_error)
            self.valid = False
            return

        self.setParamDefValuesFromProperty(self.root)

        # ---------------------------------------------------
        # Then get the objects
        for name in self.save_transform:
            if "#" in name:
                i = 0
                while not self.minmax[name].max > 0 or i < \
                        self.minmax[name].max:
                    localName = string.replaceSharpWithPadding(name, i)

                    node = dag.findChild(self.model, self.getName(localName))
                    if not node:
                        break

                    self.tra[localName] = node.getMatrix(worldSpace=True)
                    self.atra.append(node.getMatrix(worldSpace=True))
                    self.pos[localName] = node.getTranslation(space="world")
                    self.apos.append(node.getTranslation(space="world"))

                    i += 1

                if i < self.minmax[name].min:
                    mgear.log("Minimum of object requiered for " +
                              name + " hasn't been reached!!",
                              mgear.sev_warning)
                    self.valid = False
                    continue

            else:
                node = dag.findChild(self.model, self.getName(name))
                if not node:
                    mgear.log("Object missing : %s" % (
                        self.getName(name)), mgear.sev_warning)
                    self.valid = False
                    continue

                self.tra[name] = node.getMatrix(worldSpace=True)
                self.atra.append(node.getMatrix(worldSpace=True))
                self.pos[name] = node.getTranslation(space="world")
                self.apos.append(node.getTranslation(space="world"))

        for name in self.save_blade:

            node = dag.findChild(self.model, self.getName(name))
            if not node:
                mgear.log("Object missing : %s" % (
                    self.getName(name)), mgear.sev_warning)
                self.valid = False
                continue

            self.blades[name] = vector.Blade(node.getMatrix(worldSpace=True))

        self.size = self.getSize()

    def set_from_dict(self, c_dict):

        self.setParamDefValuesFromDict(c_dict["param_values"])
        self.child_components = c_dict["child_components"]

        temp_dict = {}
        for k in c_dict["tra"].keys():
            temp_dict[k] = datatypes.Matrix(c_dict["tra"][k])
        self.tra = temp_dict

        self.atra = [datatypes.Matrix(t) for t in c_dict["atra"]]

        temp_dict = {}
        for k in c_dict["pos"].keys():
            temp_dict[k] = datatypes.Vector(c_dict["pos"][k])
        self.pos = temp_dict

        self.apos = [datatypes.Vector(v) for v in c_dict["apos"]]
        for b in c_dict["blade"].keys():
            self.blades[b] = vector.Blade(datatypes.Matrix(c_dict["blade"][b]))

        self.size = self.getSize()

    # TODO: Need to store all his children in order to import partial in an
    # existing guide
    def get_guide_template_dict(self):
        c_dict = {}
        c_dict["child_components"] = []
        c_dict["param_values"] = self.get_param_values()

        temp_dict = {}
        for k in self.tra.keys():
            temp_dict[k] = self.tra[k].get()
        c_dict["tra"] = temp_dict

        c_dict["atra"] = [t.get() for t in self.atra]
        temp_dict = {}
        for k in self.pos.keys():
            temp_dict[k] = self.pos[k].get()
        c_dict["pos"] = temp_dict

        c_dict["apos"] = [p.get() for p in self.apos]
        c_dict["blade"] = self.get_blades_transform()

        # NOTE: what happens if there is more than 1 component children of the
        # guide root?
        if self.parentComponent:  # if parent is the root of guide will be None
            c_dict["parent_fullName"] = self.parentComponent.fullName
            c_dict["parent_localName"] = self.parentLocalName
        else:
            c_dict["parent_fullName"] = None
            c_dict["parent_localName"] = None

        return c_dict

    def get_blades_transform(self):
        b_tra = {}
        for b in self.blades.keys():
            b_tra[b] = self.blades[b].transform.get()

        return b_tra

    # ====================================================
    # DRAW

    def draw(self, parent):
        """Draw the guide in the scene.

        Args:
            parent (dagNode): the parent of the component.

        """
        self.parent = parent
        self.setIndex(self.parent)
        self.addObjects()
        pm.select(self.root)

        # TODO: add function to scale the points of the icons
        # Set the size of the root
        # self.root.size = self.root_size

    def drawFromUI(self, parent, showUI=True):
        """Draw the guide in the scene from the UI command.

        Args:
            parent (dagNode): the parent of the component.

        """
        if not self.modalPositions():
            mgear.log("aborded", mgear.sev_warning)
            return False

        self.draw(parent)
        transform.resetTransform(self.root, r=False, s=False)

        if showUI:
            guide_manager.inspect_settings()

        return True

    def modalPositions(self):
        """Launch a modal dialog to set position of the guide."""
        self.sections_number = None
        self.dir_axis = None
        self.spacing = None

        for name in self.save_transform:

            if "#" in name:

                init_window = chain_guide_initializer.exec_window()
                if init_window:
                    self.sections_number = init_window.sections_number
                    self.dir_axis = init_window.dir_axis
                    self.spacing = init_window.spacing

                # None the action is cancel
                else:
                    return False
                if self.sections_number:
                    if self.dir_axis == 0:  # X
                        offVec = datatypes.Vector(self.spacing, 0, 0)
                    elif self.dir_axis == 3:  # -X
                        offVec = datatypes.Vector(self.spacing * -1, 0, 0)
                    elif self.dir_axis == 1:  # Y
                        offVec = datatypes.Vector(0, self.spacing, 0)
                    elif self.dir_axis == 4:  # -Y
                        offVec = datatypes.Vector(0, self.spacing * -1, 0)
                    elif self.dir_axis == 2:  # Z
                        offVec = datatypes.Vector(0, 0, self.spacing)
                    elif self.dir_axis == 5:  # -Z
                        offVec = datatypes.Vector(0, 0, self.spacing * -1)

                    newPosition = datatypes.Vector(0, 0, 0)
                    for i in range(self.sections_number):
                        newPosition = offVec + newPosition
                        localName = string.replaceSharpWithPadding(name, i)
                        self.tra[localName] = transform.getTransformFromPos(
                            newPosition)
        return True

    # ====================================================
    # UPDATE

    def setIndex(self, model):
        """Update the component index to get the next valid one.

        Args:
            model (dagNode): The parent model of the guide.

        """
        self.model = model.getParent(generations=-1)

        # Find next index available
        while True:
            obj = dag.findChild(self.model, self.getName("root"))
            if not obj or (self.root and obj == self.root):
                break
            self.setParamDefValue("comp_index", self.values["comp_index"] + 1)

    def symmetrize(self):
        """Inverse the transform of each element of the guide."""

        if self.values["comp_side"] not in ["R", "L"]:
            mgear.log("Can't symmetrize central component", mgear.sev_error)
            return False
        for name, paramDef in self.paramDefs.items():
            if paramDef.valueType == "string":
                self.setParamDefValue(
                    name, string.convertRLName(self.values[name]))
        for name, t in self.tra.items():
            self.tra[name] = transform.getSymmetricalTransform(t)
        for name, blade in self.blades.items():
            self.blades[name] = vector.Blade(
                transform.getSymmetricalTransform(blade.transform))

        return True

    def rename(self, root, newName, newSide, newIndex):
        """Rename the component.

        Args:
            root (dagNode): The parent of the component
            newName (str): The new name.
            newSide (str): Side of the component.
            newIndex (int): index of the comonent.

        """
        self.parent = root

        # store old properties
        oldIndex = self.parent.attr("comp_index").get()
        oldSide = self.parent.attr("comp_side").get()
        oldName = self.parent.attr("comp_name").get()
        oldSideIndex = oldSide + str(oldIndex)

        # change attr side in root
        self.parent.attr("comp_name").set(newName)
        self.parent.attr("comp_side").set(newSide)
        # set new index and update to the next valid
        self.setParamDefValue("comp_name", newName)
        self.setParamDefValue("comp_side", newSide)

        self.setParamDefValue("comp_index", newIndex)
        self.setIndex(self.parent)

        self.parent.attr("comp_index").set(self.values["comp_index"])

        # objList = dag.findComponentChildren(self.parent,
        #                                     oldName, oldSideIndex)
        # NOTE: Experimenta  using findComponentChildren2
        objList = dag.findComponentChildren2(
            self.parent, oldName, oldSideIndex)
        newSideIndex = newSide + str(self.values["comp_index"])
        objList.append(self.parent)
        for obj in objList:
            suffix = obj.name().split("_")[-1]
            if len(obj.name().split("_")) == 3:
                new_name = "_".join([newName, newSideIndex, suffix])
            else:
                subIndex = obj.name().split("_")[-2]
                new_name = "_".join([newName, newSideIndex, subIndex, suffix])
            pm.rename(obj, new_name)

    # ====================================================
    # ELEMENTS

    def addRoot(self):
        """Add a root object to the guide.

        This method can initialize the object or draw it.
        Root object is a simple transform with a specific display and a setting
        property.

        Returns:
            dagNode: The root

        """
        if "root" not in self.tra.keys():
            self.tra["root"] = transform.getTransformFromPos(
                datatypes.Vector(0, 0, 0))

        self.root = icon.guideRootIcon(self.parent, self.getName(
            "root"), color=13, m=self.tra["root"])

        # Add Parameters from parameter definition list.
        for scriptName in self.paramNames:
            paramDef = self.paramDefs[scriptName]
            paramDef.create(self.root)

        return self.root

    def addLoc(self, name, parent, position=None):
        """Add a loc object to the guide.

        This mehod can initialize the object or draw it.
        Loc object is a simple null to define a position or a tranformation in
        the guide.

        Args:
            name (str): Local name of the element.
            parent (dagNode): The parent of the element.
            position (vector): The default position of the element.

        Returns:
            dagNode: The locator object.

        """
        if name not in self.tra.keys():
            self.tra[name] = transform.getTransformFromPos(position)
        if name in self.prim.keys():
            # this functionality is not implemented. The actual design from
            # softimage Gear should be review to fit in Maya.
            loc = self.prim[name].create(
                parent, self.getName(name), self.tra[name], color=17)
        else:
            loc = icon.guideLocatorIcon(parent, self.getName(
                name), color=17, m=self.tra[name])

        return loc

    def addLocMulti(self, name, parent, updateParent=True):
        """Add multiple loc objects to the guide.

        This method can initialize the object or draw it.
        Loc object is a simple null to define a position or a tranformation in
        the guide.

        Args:
            name (str): Local name of the element.
            parent (dagNode): The parent of the element.
            minimum (int): The minimum number of loc.
            maximum (int): The maximum number of loc.
            updateParent (bool): if True update the parent reference. False,
                keep the same for all loc.

        Returns:
            list of dagNode: The created loc objects in a list.

        """
        if "#" not in name:
            mgear.log(
                "You need to put a '#' in the name of multiple location.",
                mgear.sev_error)
            return False

        locs = []
        i = 0
        while True:
            localName = string.replaceSharpWithPadding(name, i)
            if localName not in self.tra.keys():
                break

            loc = icon.guideLocatorIcon(parent, self.getName(
                localName), color=17, m=self.tra[localName])
            locs.append(loc)
            if updateParent:
                parent = loc

            i += 1
        return locs

    def addBlade(self, name, parentPos, parentDir):
        """Add a blade object to the guide.

        This mehod can initialize the object or draw it.
        Blade object is a 3points curve to define a plan in the guide.

        Args:
            name (str): Local name of the element.
            parentPos (dagNode): The parent of the element.
            parentDir (dagNode): The direction constraint of the element.

        Returns:
            dagNode:  The created blade curve.

        """
        if name not in self.blades.keys():
            self.blades[name] = vector.Blade(
                transform.getTransformFromPos(datatypes.Vector(0, 0, 0)))
            offset = False
        else:
            offset = True

        dist = .6 * self.root.attr("scaleX").get()
        blade = icon.guideBladeIcon(parent=parentPos, name=self.getName(
            name), lenX=dist, color=13, m=self.blades[name].transform)
        aim_cns = applyop.aimCns(blade, parentDir, axis="xy", wupType=2,
                                 wupVector=[0, 1, 0], wupObject=self.root,
                                 maintainOffset=offset)
        pm.pointConstraint(parentPos, blade)

        offsetAttr = attribute.addAttribute(
            blade, "bladeRollOffset", "float", aim_cns.attr("offsetX").get())
        pm.connectAttr(offsetAttr, aim_cns.attr("offsetX"))
        attribute.lockAttribute(blade)

        return blade

    def addDispCurve(self, name, centers=[], degree=1):
        """Add a display curve object to the guide.

        Display curve object is a simple curve to show the connection between
        different guide element..

        Args:
            name (str): Local name of the element.
            centers (list of dagNode):  List of object to define the curve.
            degree (int): Curve degree. Default 1 = lineal.

        Returns:
            dagNode: The newly creted curve.

        """
        return icon.connection_display_curve(self.getName(name),
                                             centers,
                                             degree)

    # ====================================================
    # MISC
    def getObjects(self, model, includeShapes=True):
        """Get the objects of the component.

        Args:
            model(dagNode): The root of the component.
            includeShapes (boo): If True, will include the shapes.

        Returns:
            list of dagNode: The list of the objects.

        """
        objects = {}
        if includeShapes:
            children = pm.listRelatives(model, ad=True)
        else:
            children = pm.listRelatives(model, ad=True, typ='transform')
        pm.select(children)
        for child in pm.ls(self.fullName + "_*", selection=True):
            objects[child[child.index(
                self.fullName + "_") + len(self.fullName + "_"):]] = child

        return objects

    def getObjects2(self, model, includeShapes=True):
        """Get the objects of the component.

        Args:
            model(dagNode): The root of the component.
            includeShapes (boo): If True, will include the shapes.

        Returns:
            list of dagNode: The list of the objects.

        """
        objects = {}
        if includeShapes:
            children = [pm.PyNode(x) for x in cmds.listRelatives(
                model.longName(), ad=True, fullPath=True)]
        else:
            children = [pm.PyNode(x) for x in cmds.listRelatives(
                model.longName(), ad=True, typ='transform', fullPath=True)]
        for child in children:
            cName = child.longName()
            if cName.startswith(self.fullName):
                objects[cName.split("_")[-1]] = child

        return objects

    def getObjects3(self, model):
        """
        NOTE: Experimental function
        Get the objects of the component.
        This version only get the transforms by Name using Maya Cmds

        Args:
            model(dagNode): The root of the component.

        Returns:
            list of dagNode: The list of the objects.

        """
        objects = {}

        for child in cmds.ls(self.fullName + "_*", type="transform"):
            if pm.PyNode(child).getParent(-1) == model:
                objects[child[child.index(
                    self.fullName + "_") + len(self.fullName + "_"):]] = child

        return objects

    def addMinMax(self, name, minimum=1, maximum=-1):
        """Add minimun and maximum number of locator

        When we use the modal menu.

        """
        if "#" not in name:
            mgear.log(
                "Invalid definition for min/max. You should have a '#' in "
                "the name", mgear.sev_error)
        self.minmax[name] = MinMax(minimum, maximum)

    def getSize(self):
        """Get the size of the component.

        Returns:
            float: the size

        """
        size = .01
        for pos in self.apos:
            d = vector.getDistance(self.pos["root"], pos)
            size = max(size, d)
        size = max(size, .01)

        return size

    def getName(self, name):
        """Return the fullname of given element of the component.

        Args:
            name (str): Localname of the element.

        Returns:
            str: Element fullname.
        """
        return self.fullName + "_" + name

    def getFullName(self):
        """Return the fullname of the component.

        Returns:
            str: Component fullname.

        """
        return self.values["comp_name"] + "_" + self.values["comp_side"] + \
            str(self.values["comp_index"])

    def getType(self):
        """Return the type of the component.

        Returns:
            str: component type.

        """
        return self.compType

    def getObjectNames(self):
        """Get the objects names of the component

        Returns:
            set: The names set.

        """
        names = set()
        names.update(self.save_transform)
        names.update(self.save_primitive)
        names.update(self.save_blade)

        return names

    def getVersion(self):
        """Get the version of the component.

        Returns:
            str: versionof the component.

        """
        return ".".join([str(i) for i in self.version])

    fullName = property(getFullName)
    type = property(getType)
    objectNames = property(getObjectNames)

##########################################################
# OTHER CLASSES
##########################################################


class MinMax(object):
    """
    Minimun and maximum class.
    This class is used in addMinMax method.

    Attributes:
        minimum (int): minimum.
        maximum (int): maximum.
    """

    def __init__(self, minimum=1, maximum=-1):
        self.min = minimum
        self.max = maximum


##########################################################
# Setting Page
##########################################################

class mainSettingsTab(QtWidgets.QDialog, msui.Ui_Form):

    # ============================================
    # INIT
    def __init__(self, parent=None):
        super(mainSettingsTab, self).__init__()
        self.setupUi(self)


class componentMainSettings(QtWidgets.QDialog, guide.helperSlots):
    valueChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(componentMainSettings, self).__init__()
        # the inspectSettings function set the current selection to the
        # component root before open the settings dialog
        self.root = pm.selected()[0]

        self.mainSettingsTab = mainSettingsTab()

        self.create_controls()
        self.populate_controls()
        self.create_layout()
        self.create_connections()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def create_controls(self):
        """
        Create the controls for the component base

        """
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setObjectName("settings_tab")

        # Close Button
        self.close_button = QtWidgets.QPushButton("Close")

    def populate_controls(self):
        """Populate Controls attribute values

        Populate the controls values from the custom attributes
        of the component.

        """
        # populate tab
        self.tabs.insertTab(0, self.mainSettingsTab, "Main Settings")

        # populate main settings
        self.mainSettingsTab.name_lineEdit.setText(
            self.root.attr("comp_name").get())
        sideSet = ["C", "L", "R"]
        sideIndex = sideSet.index(self.root.attr("comp_side").get())
        self.mainSettingsTab.side_comboBox.setCurrentIndex(sideIndex)
        self.mainSettingsTab.componentIndex_spinBox.setValue(
            self.root.attr("comp_index").get())
        if self.root.attr("useIndex").get():
            self.mainSettingsTab.useJointIndex_checkBox.setCheckState(
                QtCore.Qt.Checked)
        else:
            self.mainSettingsTab.useJointIndex_checkBox.setCheckState(
                QtCore.Qt.Unchecked)
        self.mainSettingsTab.parentJointIndex_spinBox.setValue(
            self.root.attr("parentJointIndex").get())
        self.mainSettingsTab.host_lineEdit.setText(
            self.root.attr("ui_host").get())
        self.mainSettingsTab.subGroup_lineEdit.setText(
            self.root.attr("ctlGrp").get())

    def create_layout(self):
        """
        Create the layout for the component base settings

        """
        return

    def create_connections(self):
        """
        Create the slots connections to the controls functions

        """
        self.close_button.clicked.connect(self.close_settings)

        self.mainSettingsTab.name_lineEdit.editingFinished.connect(
            self.updateComponentName)
        self.mainSettingsTab.side_comboBox.currentIndexChanged.connect(
            self.updateComponentName)
        self.mainSettingsTab.componentIndex_spinBox.valueChanged.connect(
            self.updateComponentName)
        self.mainSettingsTab.useJointIndex_checkBox.stateChanged.connect(
            partial(self.updateCheck,
                    self.mainSettingsTab.useJointIndex_checkBox,
                    "useIndex"))
        self.mainSettingsTab.parentJointIndex_spinBox.valueChanged.connect(
            partial(self.updateSpinBox,
                    self.mainSettingsTab.parentJointIndex_spinBox,
                    "parentJointIndex"))
        self.mainSettingsTab.host_pushButton.clicked.connect(
            partial(self.updateHostUI,
                    self.mainSettingsTab.host_lineEdit,
                    "ui_host"))
        self.mainSettingsTab.subGroup_lineEdit.editingFinished.connect(
            partial(self.updateLineEdit,
                    self.mainSettingsTab.subGroup_lineEdit,
                    "ctlGrp"))
