import mgear.menu
from mgear.animbits import softTweaks
from mgear.animbits import channel_master
from mgear.animbits.cache_manager.dialog import run_cache_mamanger
from mgear.core import attribute


def install():
    """Install Skinning submenu
    """
    commands = (
        ("Channel Master", channel_master.openChannelMaster),
        ("-----", None),
        ("Soft Tweaks", softTweaks.openSoftTweakManager),
        ("Cache Manager", run_cache_mamanger),
        ("-----", None),
        ("Smart Reset Attribute/SRT", attribute.smart_reset)
    )

    mgear.menu.install("Animbits", commands)
