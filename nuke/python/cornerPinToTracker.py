###    CornerPin to tracker 
###    
###    ---------------------------------------------------------
###    cornerPintoTracker.py
###    Created: 10/05/2011
###    Modified: 20/06/2011
###    Written by BLUE FACES
###    info@bluefaces.eu
### 
###    Usefull for converting CornerPin node imported from Mocha to tracker node
###    Script set transform mode to matchmove and reference frame to current frame	
### 


import nuke
from CUF import renameMochaCornerPin

def cornerPinToTracker():

    cp = nuke.selectedNode()
    if cp.Class() != "CornerPin2D":
        nuke.message("Select a CornerPin node, please")
        return
    
    tr=nuke.createNode("Tracker3", inpanel = False)
    name = cp['name'].value()
    tr.knob('enable2').setValue('True')
    tr.knob('enable3').setValue('True')
    tr.knob('enable4').setValue('True')
    tr.knob('warp').setValue('srt')
    tr.knob('transform').setValue('match-move')
    tr.knob('use_for1').setValue('all')
    tr.knob('use_for2').setValue('all')
    tr.knob('use_for3').setValue('all')
    tr.knob('use_for4').setValue('all')
    tr.knob('reference_frame').setValue(nuke.frame())  
    tr.knob('transform').setValue('match-move')

    for number in range(4):
        curves = []
        for xy in range(2):
            curve = cp['to'+str(number+1)].animation(xy)
            if nuke.root().firstFrame() == 0:
                for i in range(curve.size()):
                    curve.keys()[i].x += -1
            curves += [curve]
        tr['track'+str(number+1)].copyAnimations(curves)
    
    tr.setXYpos(cp.xpos()+20, cp.ypos()+10)
    name = cp['name'].value()
    
    nuke.delete(cp)
    tr['name'].setValue(name)

    tr.knob('transform').setValue('stabilize')
    tr.knob('transform').setValue('match-move')
    tr['jitter_period'].setValue('9')

def refresh():
    n = nuke.selectedNode()
    n['reference_frame'].setValue(n['reference_frame'].value()+1)
    n['reference_frame'].setValue(n['reference_frame'].value()-1)

def cornerPinToTrackerRefresh():
    renameMochaCornerPin()
    cornerPinToTracker()
    refresh()
