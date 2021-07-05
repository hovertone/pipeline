import pymel.core as pm
import mgear
from mgear import rigbits
from mgear.rigbits import (rbf_manager_ui,
                           postSpring,
                           rope,
                           facial_rigger,
                           eye_rigger,
                           lips_rigger,
                           channelWrangler,
                           proxySlicer,
                           utils,
                           mirror_controls)
from mgear.rigbits.sdk_manager import SDK_manager_ui
from mgear.core import string
from mgear.core.anim_utils import bakeSprings
from mgear.core.anim_utils import clearSprings
from functools import partial

menuID = "Rigbits"


def install():
    """Install Rigbits submenu
    """
    pm.setParent(mgear.menu_id, menu=True)
    pm.menuItem(divider=True)
    commands = (
        ("Add NPO", rigbits.addNPO),
        ("-----", None),
        (None, gimmick_submenu),
        ("-----", None),
        ("Mirror Controls Shape", mirror_controls.show),
        ("Replace Shape", rigbits.replaceShape),
        ("-----", None),
        ("Match All Transform", rigbits.matchWorldXform),
        ("Match Pos with BBox", rigbits.matchPosfromBBox),
        ("Align Ref Axis", rigbits.alignToPointsLoop),
        ("-----", None),
        (None, pCtl_sub),
        (None, cCtl_sub),
        ("-----", None),
        ("Duplicate symmetrical", rigbits.duplicateSym),
        ("-----", None),
        ("RBF Manager", rbf_manager_ui.show),
        ("SDK Manager (BETA)", SDK_manager_ui.show),
        ("-----", None),
        ("Space Jumper", rigbits.spaceJump),
        ("Interpolated Transform", rigbits.createInterpolateTransform),
        (None, connect_submenu),
        ("-----", None),
        ("Spring", postSpring.spring_UI),
        ("Rope", rope.rope_UI),
        ("-----", None),
        ("Channel Wrangler", channelWrangler.openChannelWrangler),
        ("-----", None),
        ("Facial Rigger", facial_rigger.show),
        ("-----", None),
        ("Proxy Slicer", proxySlicer.slice),
        ("Proxy Slicer Parenting", partial(proxySlicer.slice, True)),
        ("-----", None),
        ("Bake Spring nodes", bakeSprings),
        ("Clear Baked Spring nodes", clearSprings),
        ("-----", None),
        (None, legacy_submenu),
    )

    mgear.menu.install(menuID, commands)


def connect_submenu(parent_menu_id):
    """Create the connect local Scale, rotation and translation submenu

    Args:
        parent_menu_id (str): Parent menu. i.e: "MayaWindow|mGear|menuItem355"
    """
    commands = (
        ("Connect SRT", partial(rigbits.connectLocalTransform, None, 1, 1, 1)),
        ("Connect S", partial(rigbits.connectLocalTransform, None, 1, 0, 0)),
        ("Connect R", partial(rigbits.connectLocalTransform, None, 0, 1, 0)),
        ("Connect T", partial(rigbits.connectLocalTransform, None, 0, 0, 1))

    )

    mgear.menu.install("Connect Local SRT", commands, parent_menu_id)


def legacy_submenu(parent_menu_id):
    """Create the legacy submenu

    Args:
        parent_menu_id (str): Parent menu. i.e: "MayaWindow|mGear|menuItem355"
    """
    commands = (
        ("FACIAL: Eye Rigger", eye_rigger.showEyeRigUI),
        ("FACIAL: Lips Rigger", lips_rigger.showLipRigUI)
    )

    mgear.menu.install("Legacy", commands, parent_menu_id)


def gimmick_submenu(parent_menu_id):
    """Create the gimmick joint submenu

    Args:
        parent_menu_id (str): Parent menu. i.e: "MayaWindow|mGear|menuItem355"
    """
    commands = (
        ("Add Joint", rigbits.addJnt),
        ("-----", None),
        ("Add Blended Joint", rigbits.addBlendedJoint),
        ("Add Support Joint", rigbits.addSupportJoint)
    )

    mgear.menu.install("Gimmick Joints", commands, parent_menu_id)


def _ctl_submenu(parent_menu_id, name, cCtl=False):
    """Create contol submenu

    Args:
        parent_menu_id (str): Parent menu. i.e: "MayaWindow|mGear|menuItem355"
        name (str): Menu name
        pCtl (bool, optional): If True, the new control will be child
                               of selected
    """
    ctls = ["Square",
            "Circle",
            "Cube",
            "Diamond",
            "Sphere",
            "Cross Arrow",
            "Pyramid",
            "Cube With Peak"]
    commands = []
    for c in ctls:
        cm = string.removeInvalidCharacter(c).lower()
        commands.append([c, partial(rigbits.createCTL, cm, cCtl)])

    mgear.menu.install(name, commands, parent_menu_id)


def pCtl_sub(parent_menu_id):
    """Create control as parent of selected elements

    Args:
        parent_menu_id (stro): Parent menu. i.e: "MayaWindow|mGear|menuItem355"
    """
    _ctl_submenu(parent_menu_id, "CTL as Parent", cCtl=False)


def cCtl_sub(parent_menu_id):
    """Create control as child of selected elements

    Args:
        parent_menu_id (stro): Parent menu. i.e: "MayaWindow|mGear|menuItem355"
    """
    _ctl_submenu(parent_menu_id, "CTL as Child", cCtl=True)


def install_utils_menu(m):
    """Install rigbit utils submenu
    """
    pm.setParent(m, menu=True)
    pm.menuItem(divider=True)
    pm.menuItem(label="Create mGear Hotkeys", command=utils.createHotkeys)
