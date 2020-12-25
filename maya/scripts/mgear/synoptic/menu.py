import pymel.core as pm
import mgear
from mgear import synoptic


def install():
    """Install synotic menu
    """
    pm.setParent(mgear.menu_id, menu=True)
    pm.menuItem(divider=True)
    pm.menuItem(label="Synoptic", command=synoptic.open)
