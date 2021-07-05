# Copyright (c) 2018 Guillaume Barlier
# This file is part of "anim_picker" and covered by MIT,
# read LICENSE.md and COPYING.md for details.
import gui
reload(gui)

__version__ = "1.1.0"


# =============================================================================
# Load user interface function
# =============================================================================
def load(edit=False, dockable=False, *args, **kwargs):
    """To launch the ui and not get the same instance

    Returns:
        Anim_picker: instance

    Args:
        edit (bool, optional): Description
        dockable (bool, optional): Description

    """
    return gui.load(edit=edit, dockable=dockable)
