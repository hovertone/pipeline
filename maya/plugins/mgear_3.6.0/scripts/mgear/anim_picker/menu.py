import mgear.menu
from mgear import anim_picker
from functools import partial
import mgear
import pymel.core as pm

def install():
    """Install Skinning submenu
    """
    pm.setParent(mgear.menu_id, menu=True)
    pm.menuItem(divider=True)
    commands = (
        ("Anim Picker", partial(anim_picker.load, False, False)),
        ("-----", None),
        ("Edit Anim Picker", partial(anim_picker.load, True, False))
    )

    mgear.menu.install("Anim Picker", commands)
