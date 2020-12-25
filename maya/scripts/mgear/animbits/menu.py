import mgear.menu
from mgear.animbits import softTweaks
from mgear.core import attribute


def install():
    """Install Skinning submenu
    """
    commands = (
        ("Soft Tweaks", softTweaks.openSoftTweakManager),
        ("-----", None),
        ("Smart Reset Attribute/SRT", attribute.smart_reset)
    )

    mgear.menu.install("Animbits", commands)
