'''
Equalizer Track to Nuke 
__Last edit 22.05.13
'''

from CUF import getFreeInputs, selectOnly
import nuke

def changeLocators(grp):
    '''
    Group node will have a slider to controls scale of the trackers. And now you can select trackers in Viewport

    Arguments(grp)
        grp - group node where all the trackers live

    '''

    # Creating and adding scale knob
    scaleK = nuke.Double_Knob('scale')
    scaleK.setRange(0, 10)
    scaleK.setLabel('Points Scale')
    scaleK.setValue(1)
    grp.addKnob(scaleK)

    # Creatinf and adding color knob
    k = nuke.AColor_Knob('color')
    k.setLabel('Points Color')
    grp.addKnob(k)

    # Entering the group
    grp.begin()
 
    markersColor = nuke.allNodes('Constant')[0]['color'].value()
    for c in nuke.allNodes('Constant'):
        c['color'].setExpression('parent.color')

    # Flag for moving object in the track. If moving object exists then it creates translation and rotation knobs to a group node
    movingObject = False
    if len(nuke.allNodes('Axis')) == 0:
        constant = nuke.allNodes('Constant')[0]
        print 'constant %s' % constant.name()

        # Deleting all the sphere 
        for s in nuke.allNodes('Sphere'):
            nuke.delete(s)

        # and all the mergeGeo nodes
        for m in nuke.allNodes('MergeGeo'):
            nuke.delete(m)

        transforms = nuke.allNodes('TransformGeo')
        markers = []
        # Creating new spheres with proper amount of polygons and right translations
        for t in transforms:
            s = nuke.createNode('Sphere')
            s['rows'].setValue(2)
            s['columns'].setValue(4)
            s.setXYpos(t.xpos(), t.ypos())
            s.setInput(0, constant)
            s['translate'].setValue(t['translate'].value())
            # Setting an expression to control uniform scale via group slider
            s['uniform_scale'].setExpression('parent.scale')
            # New sphere has been created. Getting rid of transform node
            nuke.delete(t)
            markers.append(s)

        # Merging all trackers into one scene
        scene = nuke.nodes.Scene(inputs = markers)
        scene.setXpos(constant.xpos() + 10)#, scene.ypos()+20)

        # Connecting Scene node with all our markers to an output node
        nuke.allNodes('Output')[0].setInput(0, scene)
    else:
        movingObject = True
        for s in nuke.allNodes('Sphere'):
            s['uniform_scale'].setExpression('parent.scale')
        animAxis = nuke.allNodes('Axis')[0]

        # Copying animation curve to paste them in group node
        translateCurves, rotateCurves = animAxis['translate'].animations(), animAxis['rotate'].animations()

        # Copying axis 
        selectOnly(animAxis)
        nuke.nodeCopy("%clipboard%") 

    # Closing the group
    grp.end()

    grp['color'].setValue(markersColor)

    if movingObject == True:
        # Pasting moving object's axis node
        pastedAxis = nuke.nodePaste("%clipboard%")
        pastedAxis.setXYpos(grp.xpos() + 10, grp.ypos() - 70)
        pastedAxis['name'].setValue(grp.name() + ' Moving Object')
        pastedAxis['tile_color'].setValue(4294967295L)

        # Creating translation XYZ knob and copying corresponding curve data to it
        trK = nuke.XYZ_Knob('translate')
        trK.setLabel('Object Translation')
        trK.copyAnimations(translateCurves)
        grp.addKnob(trK)

        # Creating rotation XYZ knob and copying corresponding curve data to it
        rotK = nuke.XYZ_Knob('rotate')
        rotK.setLabel('Object Rotation')        
        rotK.copyAnimations(rotateCurves)
        grp.addKnob(rotK)



def importScript():
    '''
    Makes Equalizer Track more friendly to work with.  
    '''
    # Importing a .nk file of Equalizer track
    nuke.nodePaste(nuke.getFilename('Select 3DEqualizer Track (.nk file)', '*.nk'))

    # Assigning all the necessary nodes to a variables
    importedNodes = nuke.selectedNodes()
    grps = []
    for n in importedNodes:
        if n.Class() == 'Scene':
            scene = n
        elif n.Class() == 'Group':
            grps.append(n)
        elif n.Class() == 'ScanlineRender':
            sl = n
        elif n.Class() == 'Camera':
            cam = n

    # Locating nodes in a suitable way and connecting them
    scene.setXpos(sl.xpos() + 10)
    cam.setXpos(scene.xpos() + 125)
    scene.setInput(getFreeInputs(scene)[0], cam)

    

    # Creating a reformat node for a BG input of the ScanlineRenderer node
    nuke.selectAll()
    nuke.invertSelection()
    ref = nuke.createNode('Reformat')
    ref.setXYpos(sl.xpos() + 130, sl.ypos())
    sl.setInput(0, ref)

    # Looping through all group nodes
    for i in range(0, len(grps)):
        # Setting up the connections between scene node and a group node
        scene.setInput(getFreeInputs(scene)[0], grps[i])
        grps[i].setXpos(sl.xpos() + 110 * i)
        # Making markers more friendly to work with
        #changeLocators(grps[i])     


#importScript()