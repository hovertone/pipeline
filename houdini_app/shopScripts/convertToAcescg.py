import linecache
import sys
import os

#print '======= in convert to acescg =========='


tp = hou.pwd()
mp = tp.parm('master_path')
if mp.rawValue() != '':
    par = tp.parent()
    parpar = par.parent()

    tta = parpar.createNode('tex_to_aces', node_name="tex_to_aces")
    tta.setPosition((par.position().x(), par.position().y() - 1))
    #tta.moveToGoodPosition()
    tta.parm('tp_path').set(tp.path())
else:
    hou.ui.displayMessage('Master path should not be empty')