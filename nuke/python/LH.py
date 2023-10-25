import nuke, os.path, nukescripts, versioning
from nukescripts import node_copypaste, autocrop
from CUF import selectOnly, fixPath, isNumber

from getpass import getuser
username = getuser()

# SET INPUT RANDGE OF READ NODE INTO LABEL
def setRangeForReads():
    for c in nuke.allNodes():
        if c.Class() == 'Read':
            f = str(c['first'].value())
            l = str(c['last'].value())
            c.knob('label').setValue(f + ' - ' + l)

# SET INPUT VALUE TO THE BEFORE AND AFTER KNOBS (BLACK, HOLD ETC)
def setBeforeAfter(v):
    for c in nuke.allNodes():
        if c.Class() == 'Read':
            c.knob('before').setValue(v)
            c.knob('after').setValue(v)

# SET INPUT VALUE TO THE ON ERROR KNOB (BLACK, ERROR ETC)
def setOnError(v):
    for c in nuke.allNodes():
        if c.Class() == 'Read':
            c.knob('on_error').setValue(v)

# TOGGLE VIEWER INPUTS ON OR offset
def toggleViewerInput(inpt = None):
    allViewers = nuke.allNodes('Viewer')
    if inpt == None:
        val = not allViewers[0]['hide_input'].value()
        for v in allViewers:
             v.knob('hide_input').setValue(val)
    else:
        for v in allViewers:
            v.knob('hide_input').setValue(inpt)

# TOGGLE INPUT OF SELECTED NODE
def toggleSelectedInput():
    n = nuke.selectedNode()
    h = n['hide_input'].value()
    if n.Class() == 'Dot':
        if h == False:
            n['hide_input'].setValue(True)    
            rgbColor = hsvToRGB(1, 1, 1)
            n['tile_color'].setValue(int('%02x%02x%02x%02x' % (int(rgbColor[0]*255),int(rgbColor[1]*255),int(rgbColor[2]*255),1*255),16))
            if n.dependencies()[0].Class() == 'Camera2' or n.dependencies()[0].Class() == 'Camera':
                n['label'].setValue('CAM')
                n['note_font_size'].setValue(33)
            elif n.dependencies()[0].Class() == 'Dot' or n.dependencies()[0].Class() == 'Read' or n.dependencies()[0].Class() == 'TimeOffset':
                n['label'].setValue('SRC')
                n['note_font_size'].setValue(33)
        else:
            n['hide_input'].setValue(False)    
            rgbColor = hsvToRGB(1, 0, 1)
            n['tile_color'].setValue(int('%02x%02x%02x%02x' % (int(rgbColor[0]*255),int(rgbColor[1]*255),int(rgbColor[2]*255),1*255),16))
            n['label'].setValue('')
            n['note_font_size'].setValue(11)
    

# LINES UP SELECTED NODES
def lineupNodes():
    count = 0
    sum = 0
    for n in nuke.selectedNodes():
        sum = sum + n['ypos'].value()
        count = count + 1
    
    for n in nuke.selectedNodes():
        n['ypos'].setValue(sum/count)


# LINES DOWN SELECTED NODES
def linedownNodes():
    count = 0
    sum = 0
    for n in nuke.selectedNodes():
        sum = sum + n['xpos'].value()
        count = count + 1
    
    for n in nuke.selectedNodes():
        n['xpos'].setValue(sum/count)

# TOGGLES APPROPRIATE MERGE NODE (CleanupMerge)
def toggleMerge():
    try:    
        m = nuke.toNode('CleanupMerge')
        b = m['disable'].value()
        m['disable'].setValue(not b)
    except TypeError:
        print('WARNING LH.ToggleMerge() exception.')


# CREATES LINKS WITH MOTION BLUR CONTROL (MB_Ctrl)
def linkMB():
    m=nuke.selectedNodes()
    for i in range (0,len(m)):
        n=m[i]
        n['motionblur'].setExpression("MB_Ctrl.motionblur")
        n['shutter'].setExpression("MB_Ctrl.shutter")
        n['shutteroffset'].setExpression("MB_Ctrl.shutteroffset")
        n['shuttercustomoffset'].setExpression("MB_Ctrl.shuttercustomoffset")

# TOGGLES DISABLE KNOB OF SELECTED NODE
def ToggleSelNode():
    node = nuke.selectedNode()
    Val = node.knob('disable').value()
    node.knob('disable').setValue(not Val)

# RELOADS ALL OF THE READ NODES
def reloadReads():
    if nuke.selectedNodes == []:
        nodes = nuke.allNodes("Read")
    else:
        if nuke.selectedNodes("Read") == []:
            nodes = nuke.allNodes("Read")
        else:
            nodes = nuke.selectedNodes("Read")

    for i in nodes:
        i['reload'].execute()
            
def setLabelEmpty():
    for node in nuke.selectedNodes():
        if node.Class() == "Read":
            node.knob('label').setValue('')
            
# SET READ LABEL WITH A DIRECTORY NAME WHERE THIS FILE LIVES
def setReadLabel(search = ''):
    if search == '':
        search = nuke.getInput('Set a word to searh for in Read node filepath')
    if search != '':
        nodeCount = len(nuke.selectedNodes())
        errorCount = 0
        for node in nuke.selectedNodes():
            if node.Class() == 'Read':
                file = node.knob('file').value()
                path = os.path.dirname(file)
                
                list = path.split('/')
                print(list)
                
                error = True
                for i in range(0,len(list)):
                    if list[i] == search:
                        label = ""
                        for j in range(i+1,len(list)):
                            label = label + "[" + str(list[j]) + "]"
                        oldLabel = node.knob('label').value()
                        if oldLabel == '':
                            node.knob('label').setValue(label)
                        elif oldLabel == label:
                            pass
                        else:
                            node.knob('label').setValue(oldLabel + '\n' + label)
                        error = False
                        break                        
                if error == True: errorCount += 1                                
    

    if errorCount > 0: 
        message = "%s out of %s selected Read nodes filepaths don't have folder \'%s\' in it" % (errorCount, nodeCount, search)
        nuke.message(message)
        
        
# ALIGNS NODES. MAIN WILL ALLWAYS STAYS IN PLACE
def alignNodes(main, minor):
    difx = abs(main.xpos() - minor.xpos())
    dify = abs(main.ypos() - minor.ypos())
    kissx = False
    kissy = False
    increasey = 0
    if difx < 90: kissx = True
    if dify < 90: kissy = True
    if difx < dify:
        minor.setXpos(main.xpos())
        if kissy == True: 
            if main.ypos() > minor.ypos():
                minor.setYpos(main.ypos()-(minor.screenHeight()+6))
            else:
                minor.setYpos(main.ypos()+(main.screenHeight()+6))
    else:
        minor.setYpos(main.ypos() -  ((minor.screenHeight() - main.screenHeight())/2))
        if kissx == True: 
            if main.xpos() > minor.xpos():
                minor.setXpos(main.xpos()-90)
            else:
                minor.setXpos(main.xpos()+90)
    print("ALIGNED")
            
        
        
        
def zhivchikLabel6():
    node = nuke.thisNode()
    #bottles = {'one' = 1, 'two' = 2,'three' = 3, 'four' = 4}
    bottles = ['one', 'two','three', 'four', 'five', 'six']
    parts = ['bottle', 'lid', 'coverc', 'cover', 'liquid', 'plastic']
    strName = ""
    strLabel = ""
    for i in bottles:
        if node[i].value() == 1:
            strName = strName + i + " "
    
    for i in parts:
        if node[i].value() == 1:
            strLabel = strLabel + i + " "
    
    if strName == "": strName = "{empty}"
    if strLabel == "": strLabel = "{empty}"
    
    label = strName + "\n" + strLabel    
    return label

def arrangeZhivchikGizmos6():    
    all = nuke.allNodes()
    for i in all:
        if i.Class() == 'ZhivchikMattes6.gizmo':
            i.knob('autolabel').setValue('LH.zhivchikLabel6()')
            dep = i.dependent()[0]
            alignNodes(dep,i)

def zhivchikLabel4():
    node = nuke.thisNode()
    #bottles = {'one' = 1, 'two' = 2,'three' = 3, 'four' = 4}
    bottles = ['one', 'two','three', 'four']
    parts = ['bottle', 'lid', 'coverc', 'cover', 'liquid']
    strName = ""
    strLabel = ""
    for i in bottles:
        if node[i].value() == 1:
            strName = strName + i + " "    

    for i in parts:
        if node[i].value() == 1:
            strLabel = strLabel + i + " "
    
    if strName == "": strName = "{empty}"
    if strLabel == "": strLabel = "{empty}"
    
    label = strName + "\n" + strLabel    
    return label

def arrangeZhivchikGizmos4():
    all = nuke.allNodes()
    for i in all:
        if i.Class() == 'ZhivchikMattes4.gizmo':
            i.knob('autolabel').setValue('LH.zhivchikLabel4()')
            dep = i.dependent()[0]            
            alignNodes(dep,i)

# SCALING NODES ARRANGEMENT FROM CENTER
def scaleNodes(scale):
    nodes = nuke.selectedNodes()
    amount = len(nodes)
    if amount == 0: return
    
    allX = 0
    allY = 0
    
    for n in nodes:
        allX += n.xpos()
        allY += n.ypos()
    
    centerX = allX/amount
    centerY = allY/amount
    
    for n in nodes:
        n.setXpos(centerX + (n.xpos() - centerX)*scale)
        n.setYpos(centerY + (n.ypos() - centerY)*scale)


# MIRRORS 7th VIEWER PIPE
mirrored = False
def mirrorViewer():
    global mirrored
    if mirrored == False:
        if nuke.exists('VIEWER_INPUT'):
            oldVI = nuke.toNode('VIEWER_INPUT')
            oldVI['name'].setValue('VIEWER_INPUT_1')
        selNodes = nuke.selectedNodes()
        nuke.selectAll()
        nuke.invertSelection()
        m = nuke.createNode('Mirror', 'name VIEWER_INPUT Horizontal True')
        v = nuke.toNode('Viewer1')
        m.setXYpos(v.xpos() + 110, v.ypos())
        for n in selNodes:
            n.setSelected(True)
        mirrored = True
    else:
        try:
            ViewerInput = nuke.toNode('VIEWER_INPUT')
            if ViewerInput.Class() == 'Mirror':
                nuke.delete(ViewerInput)
                if nuke.exists('VIEWER_INPUT_1'):
                    nuke.toNode('VIEWER_INPUT_1')['name'].setValue('VIEWER_INPUT')
        finally:
            mirrored = False
        
        
def hsvToRGB(h, s, v):
    """Convert HSV color space to RGB color space
    
    @param h: Hue
    @param s: Saturation
    @param v: Value
    return (r, g, b)  
    """
    import math
    hi = math.floor(h / 60.0) % 6
    f =  (h / 60.0) - math.floor(h / 60.0)
    p = v * (1.0 - s)
    q = v * (1.0 - (f*s))
    t = v * (1.0 - ((1.0 - f) * s))
    return {
        0: (v, t, p),
        1: (q, v, p),
        2: (p, v, t),
        3: (p, q, v),
        4: (t, p, v),
        5: (v, p, q),
    }[hi]

def rgbToHSV(r, g, b):
    """Convert RGB color space to HSV color space
    
    @param r: Red
    @param g: Green
    @param b: Blue
    return (h, s, v)  
    """
    maxc = max(r, g, b)
    minc = min(r, g, b)
    colorMap = {
        id(r): 'r',
        id(g): 'g',
        id(b): 'b'
    }
    if colorMap[id(maxc)] == colorMap[id(minc)]:
        h = 0
    elif colorMap[id(maxc)] == 'r':
        h = 60.0 * ((g - b) / (maxc - minc)) % 360.0
    elif colorMap[id(maxc)] == 'g':
        h = 60.0 * ((b - r) / (maxc - minc)) + 120.0
    elif colorMap[id(maxc)] == 'b':
        h = 60.0 * ((r - g) / (maxc - minc)) + 240.0
    v = maxc
    if maxc == 0.0:
        s = 0.0
    else:
        s = 1.0 - (minc / maxc)
    return (h, s, v)        


def CreateShotSetup(shotPath = "", shotName = ""):
    p = nuke.Panel("Create %s Setup" % shotName)
    p.addSingleLineInput("Shot Name", shotName)
    p.addBooleanCheckBox("Local Copy", False)
    p.addFilenameSearch("Output Path", shotPath)
    p.addButton("Create")
    p.addButton("OK")
    
    if p.show():
        return p.value( 'Shot Name' ), p.value( 'Local Copy' ), p.value('Output Path')

def randomColor(satIn = 1.0, valIn = 1.0, alpha = 1):
    import random
    import LH
    hue = random.randint(0,360)
    sat = satIn
    val = valIn
    print("HSV", hue, sat, val)
    color = []
    for i in LH.hsvToRGB(hue,sat,val):
        color.append(i)
    color.append(alpha)
    print("RGB", color)
    r = color[0]
    g = color[1]
    b = color[2]
    a = color[3]
    clr = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,a*255),16)
    return clr

def shotSetup():
    if nuke.selectedNode().Class() == "Read":
        import os.path
        from time import sleep

        v = nuke.toNode("Viewer1")
        read = nuke.selectedNode()
        lastNode = read
        pathName = os.path.split(read.knob('file').value())[1]
        pathNameList = pathName.split(".")
        if len(pathNameList) < 3:
            shotName = pathNameList[0].split("_")[0]
        else:
            shotName = pathNameList[0]
        
        panelResult = CreateShotSetup(os.path.split(read.knob('file').value())[0], shotName)
        
        note = nuke.nodes.StickyNote()
        note['tile_color'].setValue(randomColor(0.7, 0.7, 1))
        note['label'].setValue("SHOT " + panelResult[0])
        fontSize = 2000/len(shotName)
        note['note_font_size'].setValue(int(fontSize))
        while note.screenWidth() > 300:
            fontSize -= 10
            note['note_font_size'].setValue(fontSize)
        print(note.screenWidth())
        
            
        centerPos = read.xpos()+40
        if panelResult[1] == True:
            dot = nuke.nodes.Dot()
            dot.setXYpos(read.xpos()+200,read.ypos()+read.screenHeight()/2-6)
            dot.setInput(0, read)
            lastNode = dot
            centerPos = dot.xpos()+6
        
        timeOffset = nuke.nodes.TimeOffset()
        timeOffset.setYpos(read.ypos()+read.screenHeight()+8)
        timeOffset.setXYpos(centerPos-40,lastNode.ypos()+lastNode.screenHeight()+40)
        timeOffset.setInput(0,lastNode)
        timeOffset.knob('time_offset').setValue(read.knob('first').value()*(-1))
    
        
        
        dot2 = nuke.nodes.Dot()
        dot2.setInput(0,timeOffset)
        dot2.setXYpos(centerPos-6, timeOffset.ypos()+140)
        v.setInput(3, dot2)
        v.setInput(0, dot2)
        dot4 = nuke.nodes.Dot()
        dot4.setXYpos(centerPos-6,timeOffset.ypos()+2450)
        dot4.setInput(0,dot2)
        v.setInput(6, dot4)
        rtimeOffset = nuke.nodes.TimeOffset()
        rtimeOffset.knob('time_offset').setValue(read.knob('first').value())
        rtimeOffset.setXYpos(centerPos-40,timeOffset.ypos()+2500)
        rtimeOffset.setInput(0, dot4)
        meta = nuke.nodes.CopyMetaData()
        meta.setXYpos(centerPos-40,rtimeOffset.ypos()+24)
        meta.setInput(0,rtimeOffset)
        dot3 = nuke.nodes.Dot()
        if panelResult[1] == True:
            dot3.setInput(0,dot)
        else:
            dot3.setInput(0,read)
        dot3.setXYpos(centerPos-100, meta.ypos()+3)
        dot3.knob('hide_input').setValue('True')
        write = nuke.nodes.Write()
        write.setXYpos(centerPos-40,meta.ypos()+24)
        write.setInput(0, meta)
        write.knob('colorspace').setValue('linear')
        meta.setInput(1,dot3)
        
        panelPath = panelResult[2]
        if os.path.splitext(panelPath)[1] == "":
            outputPath = panelPath
        else:
            outputPath = os.path.split(panelPath)[0]
        
        writeFileKnob = os.path.join(outputPath,os.path.split(read.knob('file').value())[1])
        
        write.knob('file').setValue(writeFileKnob)
        write['beforeRender'].setValue("OhuIO.createOutDir(nuke.thisNode()['file'].value())")
        
        note.setXpos(read.xpos()-note.screenWidth()-200)
        note.setYpos(read.ypos())
        toggleViewerInput()
    else:
        nuke.message("Select a Read node")


# COLORIZED ALL BACKDROP NODES
def colorizeBackdrops():
    if nuke.selectedNodes('BackdropNode') == []:
        for i in nuke.allNodes('BackdropNode'):
            i['tile_color'].setValue(randomColor(0.9, 0.4, 1))
    else:
        for i in nuke.selectedNodes('BackdropNode'):
            i['tile_color'].setValue(randomColor(0.9, 0.4, 1))
            
# COLORIZED ALL STICKYNOTES
def colorizeStickyNotes():
    if nuke.selectedNodes('StickyNote') == []:
        for i in nuke.allNodes('StickyNote'):
            i['tile_color'].setValue(randomColor(0.9, 0.4, 1))
    else:
        for i in nuke.selectedNodes('StickyNote'):
            i['tile_color'].setValue(randomColor(0.9, 0.4, 1))
    

# CREATES A THUMBNAILS FROM PATH OF READ NODES
def createThumbs():
    for i in nuke.selectedNodes('Read'):
        w = nuke.nodes.Write()
        w.setInput(0,i)
        path =  i['file'].value().split('/')
        output = 'Z:/36_Henkel_TVC/00_OUT/Dailies/2012_04_18/CC_Stills/' + 'Thumb_' + path[-3] + '_' + path[-2] + '.jpg'
        w['file'].setValue(output)
        w['colorspace'].setValue('linear')
    
# DELETES ALL ERROR NODES    
def deleteErrorReads():
    import os.path
    if nuke.selectedNodes("Read") == []:
        nodes = nuke.allNodes("Read")
    else:
        nodes = nuke.selectedNodes("Read")
    
    for i in nodes:
        if i.error() == True:
            nuke.delete(i)
            
    if nuke.selectedNodes("Read") != []:
        autoplace()
        nodes = nuke.selectedNodes("Read")
        for i in range(len(nodes)):
            nodes[i]['label'].setValue(os.path.split(nodes[i]['file'].value())[0].split('/')[-1])
        
    


# SETS READ NODES COLORSPACE KNOB TO sRGB. DEPENDS IF READ NODES ARE SELECTED. IF SO SETS ONLY SELECTED. ELSE SETS EVERY READ NODE TO sRGB
def sRGBReads():
    if nuke.selectedNodes("Read") == []:
        reads = nuke.allNodes("Read")
    else:
        reads = nuke.selectedNodes("Read")
    
    for r in reads:
        r['colorspace'].setValue('sRGB')


def getxpos(node):
        return node.xpos()
    
def arrange():
    nodes = nuke.selectedNodes()
    nodes = sorted(nodes, key=getxpos)
    
    
    sumx = 0
    for n in range(len(nodes)):
        if n == 0:
            ypos = nodes[n].ypos()    
        else:
            sumx += nodes[n].xpos() - nodes[n-1].xpos()
    
    average = sumx/len(nodes)-1
    
    for n in range(len(nodes)):
        if n != 0:
            nodes[n].setYpos(ypos)
            nodes[n].setXpos(nodes[n-1].xpos()+average)
            
def fSteadinessToCornerPin():
    fs = nuke.selectedNode()
    
    BL = [fs['pinBL'].animation(0),fs['pinBL'].animation(1)]
    BR = [fs['pinBR'].animation(0),fs['pinBR'].animation(1)]
    TL = [fs['pinTL'].animation(0),fs['pinTL'].animation(1)]
    TR = [fs['pinTR'].animation(0),fs['pinTR'].animation(1)]
    
    cp=nuke.createNode("CornerPin2D", inpanel = False)
    
    cp['to1'].copyAnimations(BL)
    cp['to2'].copyAnimations(BR)
    cp['to3'].copyAnimations(TR)
    cp['to4'].copyAnimations(TL)
    
    cp.setXYpos(fs.xpos()+110,fs.ypos())
    
    
def getXpos(n):
    return n.xpos()

def autoplace():
    nodes = sorted(nuke.selectedNodes(),key=getXpos)
    
    for i in range(len(nodes)):
        nodes[i].setXYpos(nodes[0].xpos() + i*110,nodes[0].ypos())

def backdropMergeInput(a):
    import nukescripts
    nodesToClimb = a.dependencies()
    nodesToClimb.pop(0)
    nodesToSelect = []
    
    def climb(node):
        for n in node.dependencies():
            nodesToSelect.append(n)
            climb(n)
    
    for b in nodesToClimb:
        nodesToSelect.append(b)
        climb(b)    
    a.setSelected(False)
    
    for n in nodesToSelect:
        n.setSelected(True)
    
    nukescripts.autoBackdrop()
 
def dependenciesSelect(nodesToClimb):    
    nodesToSelect = []
    
    def climb(node):
        for n in node.dependencies():
            nodesToSelect.append(n)
            climb(n)
    
    for b in nodesToClimb:
        nodesToSelect.append(b)
        climb(b)    
    
    return nodesToSelect

    
def backdropMergeInputs():
    nodes = nuke.selectedNodes('Merge2')
        
    if len(nodes) > 0:
        for n in nodes:
            for m in nuke.allNodes():
                m.setSelected(False)
            backdropMergeInput(n)
    else:
        nuke.message('Select Merge node')
        
        
def createRotoPremult():
    global username
    if len(nuke.selectedNodes()) > 0:
        a = nuke.selectedNodes()
        for n in a:
            b = n.dependent()
            r = nuke.nodes.Roto(output ='alpha', premultiply = 'rgb', replace = True)
            r['disable'].setValue(True)
            r.setXYpos(n.xpos(),n.ypos()+n.screenHeight()+6)        
            r.setInput(0,n)
            for m in b:
                m.setInput(0, r)

        for v in n.dependent(): 
            if v.Class == 'Viewer': 
                break
        
        inpt = 0
        for i in v.dependencies():
            if i == n:
                break
            else:
                inpt += 1
        v.setInput(inpt, n)
       
    else:
        r = nuke.createNode("C:/Users/%s/.nuke/ToolSets/RotoPremult.nk" % (username))
        r['disable'].setValue(True)
        

def createReformat():
    if len(nuke.selectedNodes()) > 0:
        a = nuke.selectedNodes()
        for n in a:
            b = n.dependent()
            r = nuke.nodes.Reformat()
            r.setXYpos(n.xpos(),n.ypos()+n.screenHeight()+6)        
            r.setInput(0,n)
            for m in b:
                m.setInput(0, r)
            #r['filter'].setValue("Rifman")
    else:
        r = nuke.createNode("Reformat")  
        #r['filter'].setValue("Rifman")
    
def pathSwitch():
    node =  nuke.thisNode()
    temp = node['local'].value()
    node['local'].setValue(node['network'].value())
    node['network'].setValue(temp)
    
    
def frameHoldSet():
	n = nuke.thisNode()
	
	#Sets current frame on create
	n['first_frame'].setValue(nuke.frame())
	
	#Creates SetThisFrame button
	tabName = nuke.Tab_Knob("Set_This_Frame", "SetThisFrame")
	n.addKnob(tabName)
	scriptButton = nuke.PyScript_Knob("SetThisFrame", "SetThisFrame")
	n.addKnob(scriptButton)
	n.knob("SetThisFrame").setCommand("""node = nuke.thisNode()
node['first_frame'].setValue(nuke.frame()) """)     
    
def timeOffset():
    if len(nuke.selectedNodes()) > 0:
        n = nuke.selectedNodes()[0]
        offset = n.firstFrame() * -1
    else:
        offset = 0
    nuke.thisNode()['time_offset'].setValue(offset)
#    nuke.thisNode().setXYpos(n.xpos(), n.ypos() + n.screenHeight() + 6)

def createTimeOffset():
    '''
    Create a TimeOffset node and set offset value its first value of the selected Node.
    '''
    
    if len(nuke.selectedNodes()) > 0:
        print("many nodes selected")
        nodes = nuke.selectedNodes()
        for n in nodes:
            depFlag = False
            if len(n.dependent()) > 0:
                depFlag = True
                dep = []
                for d in n.dependent():
                    dep.append(d)    
            selectOnly(n)
            to = nuke.createNode('TimeOffset', inpanel = False)
            to.setXYpos(n.xpos(), n.ypos() + n.screenHeight() + 6)
            to['time_offset'].setValue((n.firstFrame()*-1)+1)
            
            if depFlag == True:
                for d in dep:
                    d.setInput(0, to)
    else:
        nuke.createNode('TimeOffset', inpanel = False)
        
        
def knobExists(node, knob):
    '''
    Returns True if knob exists. False if not
    
    Arguments (node, knob)
        node - single node 
        knob - knob name in string type
    
    '''
    try:
        v = node[str(knob)]
        return True
    except:
        return False


def setAlphaChannel():
    node = nuke.thisNode()
    dep = []
    if len(nuke.selectedNodes()) > 0:
        dep = nuke.selectedNodes()[0]

    if len(dep) > 0:
        print("in")
        if knobExists(dep, 'channels'):
            if dep['channels'].value() == 'alpha':
                try:
                    node['output'].setValue('alpha')
                except NameError:
                    node['channels'].setValue('alpha')
                    
        elif knobExists(dep, 'output'):
            if dep['output'].value() == 'alpha':
                if node.Class() == 'Blur':
                    print("1")
                    node['channels'].setValue('alpha')

def renderWrites(glb = False):
    writes = nuke.selectedNodes("Write")
    for w in writes:
        if w['disable'].value() == False:
            wLabel = w['label'].value()
            w['label'].setValue('yes')
            if glb == False:
                nuke.execute(w.name(), w.firstFrame(), w.lastFrame())
            else:
                nuke.execute(w.name(), nuke.root()['first_frame'].value(), nuke.root()['last_frame'].value())
            w['label'].setValue(wLabel)
                
        
        
def copyTrackingToRoto(linkinp = False):
    nodes = nuke.selectedNodes()
    if linkinp == True:
      link = True
    else:
      link = False
        
    for n in nodes:
        #print n.Class()
        if n.Class() == 'Roto' or n.Class() == 'RotoPaint' or n.Class() == 'Bezier': roto = n
        elif n.Class() == 'Tracker3' or n.Class() == 'Tracker4': tr = n
        elif n.Class() == 'Dot': 
            link = True
            dot = n

    if 'roto' not in locals() or 'tr' not in locals():
        nuke.message('Select proper nodes')
        return

    knobsTemplate = ['translate', 'rotate', 'scale', 'center']
    for i in knobsTemplate:
        if tr.knobs()[i].isAnimated:
          if link:
              trName = tr.name()
              roto[i].setExpression('parent.' + trName + '.' +  i)
          else:
              roto[i].fromScript(tr[i].toScript())

    if 'dot' in locals():
        nuke.delete(dot)

    roto['label'].setValue('frame ' + str(tr['reference_frame'].value()))
    


def splitAbc(n):
    k = n['scene_view']
    items = k.getAllItems()

    geos = [n]
    k.setSelectedItems([items[0]])
    for i in range(len(items)-1):
        node_copypaste()
        n = nuke.selectedNode()
        n['scene_view'].setSelectedItems([items[i+1]])
        geos.append(n)

    nuke.selectAll()
    nuke.invertSelection()


    for n in geos:
        n.setSelected(True)

    autoplace()

    nuke.selectAll()
    nuke.invertSelection()

def splitMultipleAbc():
    nodes = nuke.selectedNodes()
    for n in nodes:
        splitAbc(n)


def createJpegs():
    nodes = nuke.selectedNodes()
    minFrame, maxFrame = 0, 0
    writes = []
    for n in nodes:
        selectOnly(n)
        fullPath = n['file'].value()
        nameExt = os.path.split(fullPath)[-1]
        name = nameExt[:nameExt.find('.')]
        w = nuke.createNode('Write')
        writes.append(n)
        
        w['file'].setValue(fixPath(os.path.join(os.path.split(fullPath)[0], 'jpg', name + '.jpg')))
        w['_jpeg_quality'].setValue('1')
        w['label'].setValue('yes')
        w['use_limit'].setValue(True)

        rFirst, rLast = n['first'].value(), n['last'].value()
        w['first'].setValue(rFirst)
        w['last'].setValue(rLast)

        if rFirst < minFrame: minFrame = rFirst
        if rLast > maxFrame: maxFrame = rLast
    
        nuke.execute(w.name(), minFrame, maxFrame)
        w['createRead'].execute()

        print(":: %s\n:__ [%s - %s] done." % (w['file'].value(), rFirst, rLast))

def createThumbs(path, nodes = '', scaleValue = 0.2, jpegQuality = 90):
    if nodes == '':
        nodes = nuke.selectedNodes('Read')

    for n in nodes:
        if 'sequences' in n['file'].value():
            shotName = n['file'].value().split('/')[-3]

            selectOnly(n)
            ref = nuke.createNode('Reformat')
            ref['type'].setValue('scale')
            ref['scale'].setValue(scaleValue)

            selectOnly(ref)
            
            w = nuke.createNode('Write')
            
            if path[-1] != '/': 
                if path[-1] != '\\':
                    path = path[:-1] + '/'
                else:
                    path = path + '/'

            w['file'].setValue(path + shotName + '.jpg')
            w['label'].setValue('yes')
            w['_jpeg_quality'].setValue(90)
            nuke.execute(w['name'].value(), w.firstFrame(), w.firstFrame())
        
            nukescripts.cache_clear("")

        else:
            print('WARNING: Read %s is out of TFX pipeline structure.' % n.name())

def addOpenEButton():
    if os.name == 'nt':
        openEK = nuke.PyScript_Knob('openE')
        openEK.setValue('from CUF import openE\nopenE()')
        openEK.setLabel('Open in Explorer')
        openEK.setTooltip("This button will open a node's filepath in Explorer")
        nuke.thisNode().addKnob(openEK)

        try:
            tabK = nuke.thisNode()['User']
            tabK.setLabel('Q(-_-Q)')
        except:
            pass

def addCreateReadFromWriteButton():
    if os.name == 'nt':
        createWriteK = nuke.PyScript_Knob('createRead')
        createWriteK.setValue('from createReadFromWrite import createReadFromWrite\ncreateReadFromWrite()')
        createWriteK.setLabel('Create Read')
        createWriteK.setTooltip("This button will create Read node from this node's file path")
        nuke.thisNode().addKnob(createWriteK)

        try:
            tabK = nuke.thisNode()['User']
            tabK.setLabel('Q(-_-Q)')
        except:
            pass

def normalizeDepth(node = '', chn = 'rgb', first = nuke.frame(), last  = nuke.frame()):
    def getName(node):
        return node.name()

    if node == '':
        srcNode = nuke.selectedNode()
    else:
        srcNode = node

    MinColor = nuke.nodes.MinColor(target=0, inputs=[srcNode], channels = chn)
    Inv = nuke.nodes.Invert(inputs=[srcNode], channels = chn)
    MaxColor = nuke.nodes.MinColor(target=0, inputs=[Inv], channels = chn)

    curFrame = nuke.frame()
    nuke.execute( MinColor, curFrame, curFrame )
    min = -MinColor['pixeldelta'].value()
   
    nuke.execute( MaxColor, curFrame, curFrame )
    max = MaxColor['pixeldelta'].value() + 1
   
    for n in ( MinColor, MaxColor, Inv ):
        nuke.delete( n )

    allNormalizers = [i for i in nuke.allNodes('Expression') if ('Normalizer' in i.name()) and (isNumber(i.name().strip('Normalizer')) == True)]
    if len(allNormalizers) == 0:
        name = 'Normalizer01'
    else:
        name = 'Normalizer%s' % str(int(sorted(allNormalizers, key = getName)[-1].name().strip('Normalizer'))+1).zfill(2)

    return nuke.createNode( 'Expression', 'name %s temp_name0 minVal temp_expr0 %s temp_name1 maxVal temp_expr1 %s expr0 (r-minVal)/maxVal channel0 rgba channel1 none channel2 none' % (name, min, max))

def normalizeRGB(node = ''):

    if node == '':
        node = nuke.selectedNodes()[0]

    for c in ('r', 'g', 'b'):
        selectOnly(node)
        if c == 'r':
            s = nuke.nodes.Shuffle(red='red', green='red', blue='red', alpha='black', inputs=[node])
            s.setXYpos(node.xpos(), node.ypos() + 60)
            selectOnly(s)
            rexpr = normalizeDepth()
        elif c == 'g':
            s = nuke.nodes.Shuffle(red='green', green='green', blue='green', alpha='black', inputs=[node])
            s.setXYpos(node.xpos() + 110, node.ypos() + 60)
            selectOnly(s)
            gexpr = normalizeDepth()
            copy1 = nuke.nodes.Copy(from0='green', to0='green', inputs=[rexpr, gexpr], xpos = rexpr.xpos(), ypos = rexpr.ypos() + 60)
        elif c == 'b':
            s = nuke.nodes.Shuffle(red='blue', green='blue', blue='blue', alpha='black', inputs=[node])
            s.setXYpos(node.xpos() + 220, node.ypos() + 60)
            selectOnly(s)
            bexpr = normalizeDepth()
            copy2 = nuke.nodes.Copy(from0='blue', to0='blue', inputs=[copy1, bexpr], xpos = copy1.xpos(), ypos = copy1.ypos() + 60)

    nuke.nodes.Grade(inputs=[copy2])


def createPMatteRepr():
    src = nuke.thisNode()
    srcname = src.name()
    pp = src['p_matte_in'].value()
    
    with nuke.root():
        dest = nuke.createNode('P_Matte_repr')
        
        kk = ['matteShape', 'rot_order', 'center', 'rotate', 'scaling', 'uniform_scale']
        for k in kk:
            dest[k].setExpression('%s.%s' % (srcname, k))
        
    dest['label'].setValue('Linked to %s' % srcname)
    dest['in'].setValue(pp)

    dest.setXYpos(src.xpos() + 200, src.ypos() + dest.screenWidth()/2)
    try:
        dest.setInput(0, src.dependencies()[0])
    except:
        pass

def platformBasedSwitchReadPath(switchTo = None):
    if switchTo == None:
        if os.name == 'nt':
            switchTo = 'pc'
        elif os.name == 'posix':
            switchTo = 'linux'
    
    allNodes = nuke.allNodes()
    neededNodes = []
    for n in allNodes:
        if ('Read' or 'ReadGeo' or 'Camera2' or 'Camera1' or 'Camera3') in n.Class():
            neededNodes.append(n)
    for n in neededNodes: print(n.name())

    if switchTo == 'pc':
        for n in neededNodes:
            try:
                n['file'].setValue(n['file'].value().replace('/mnt/projects', 'P:'))
            except:
                pass

            try:
                n['file'].setValue(n['file'].value().replace('/mnt/data', 'O:'))
            except:
                pass            

            try:
                n['file'].setValue(n['file'].value().replace('/mnt/src', 'S:'))
            except:
                pass  
    elif switchTo == 'linux':
        print('In ToLinux part')
        for n in neededNodes:
            try:
                n['file'].setValue(n['file'].value().replace('P:', '/mnt/projects'))
            except:
                pass

            try:
                #print n['file'].value()
                n['file'].setValue(n['file'].value().replace('O:', '/mnt/data'))
            except:
                pass

            try:
                #print n['file'].value()
                n['file'].setValue(n['file'].value().replace('S:', '/mnt/data'))
            except:
                pass
                
    elif switchTo != None and switchTo != 'pc' and switchTo != 'linux':
        nuke.message('There is no such argument as %s.' % switchTo)
        return
        return

def findGizmos(noMessages = False):
    selectOnly()
    gizmos = []
    noGizmos = True
    for n in nuke.allNodes():
        if '.gizmo' in n.Class():
            #print n.name()
            noGizmos = False
            gizmos.append(n)

    if noGizmos == True: 
        if noMessages == False:
            nuke.message('There is no gizmo nodes.')
        return None
    else:
        if noMessages == False:
            for g in gizmos:
                g.setSelected(True)
        return gizmos
        


def autocropSelected(layer = 'alpha'):
    for n in nuke.selectedNodes():
        autocrop(first = n.firstFrame(), last = n.lastFrame(), layer = layer)

def convertGizmosToGroups(nodes = ''):
   ###Node Selections
   if nodes == '': nodeSelection = nuke.selectedNodes()
   elif nodes == None: return
   elif type(nodes) == list: nodeSelection = nodes

   noGizmoSelection = []
   gizmoSelection = []
   for n in nodeSelection:
       if 'gizmo_file' in n.knobs():
           gizmoSelection.append(n)
       else:
           noGizmoSelection.append(n)
   groupSelection = []

   for n in gizmoSelection:
       bypassGroup = False
       ###Current Status Variables
       nodeName = n.knob('name').value()
       nodeXPosition = n['xpos'].value()
       nodeYPosition = n['ypos'].value()
       nodeHideInput = n.knob('hide_input').value()
       nodeCached = n.knob('cached').value()
       nodePostageStamp = n.knob('postage_stamp').value()
       nodeDisable = n.knob('disable').value()
       nodeDopeSheet = n.knob('dope_sheet').value()
       nodeDependencies = n.dependencies()
       nodeMaxInputs = n.maxInputs()
       inputsList = []

       ###Current Node Isolate Selection
       for i in nodeSelection:
           i.knob('selected').setValue(False)            
       n.knob('selected').setValue(True)

       nuke.tcl('copy_gizmo_to_group [selected_node]')

       ###Refresh selections
       groupSelection.append(nuke.selectedNode())
       newGroup = nuke.selectedNode()

       ###Paste Attributes
       newGroup.knob('xpos').setValue(nodeXPosition)
       newGroup.knob('ypos').setValue(nodeYPosition)
       newGroup.knob('hide_input').setValue(nodeHideInput)
       newGroup.knob('cached').setValue(nodeCached)
       newGroup.knob('postage_stamp').setValue(nodePostageStamp)
       newGroup.knob('disable').setValue(nodeDisable)
       newGroup.knob('dope_sheet').setValue(nodeDopeSheet)

       ###Connect Inputs
       for f in range(0, nodeMaxInputs):
           inputsList.append(n.input(f))
       for num, r in enumerate(inputsList):
           newGroup.setInput(num, None)
       for num, s in enumerate(inputsList):
           newGroup.setInput(num, s)

       n.knob('name').setValue('temp__'+nodeName+'__temp')
       newGroup.knob('name').setValue(nodeName)

       newGroup.knob('selected').setValue(False)

   ###Cleanup (remove gizmos, leave groups)
   for y in gizmoSelection:
       y.knob('selected').setValue(True)
   nukescripts.node_delete(popupOnError=False)
   for z in groupSelection:
       z.knob('selected').setValue(True)
   for w in noGizmoSelection:
       w.knob('selected').setValue(True)

def sendToPlatform():
    p = nuke.Panel("Duplicator", 450)

    p.addEnumerationPulldown("Send to ", 'linux pc')
    p.addBooleanCheckBox('Save with new filename?', True)
    p.addButton("Cancel")
    p.addButton("OK")

    result = p.show()


    # IF NOT OK
    if result == 0: return False # _________________ EXIT

    sendTo = p.value("Send to ")
    save = p.value('Save with new filename?')
    scriptFullPath = nuke.root()['name'].value()

    # LINIX PART
    # SAVE FEW NODES

    if sendTo == 'linux':
        if len(nuke.selectedNodes()) > 0:
            pass # insert partical tree selection save to lnx
        else:
            findGizmos()
            convertGizmosToGroups()
            platformBasedSwitchReadPath('linux')
            if save == True: # if user wants to save with different filename
                print('__here')
                if scriptFullPath != '':
                    nuke.scriptSaveAs(scriptFullPath[:-3] + '_lnx.nk')
                else:
                    nuke.scriptSaveAs()
    # PC PART
    else:
        #nuke.message("oops, doesn't currently working.")
        platformBasedSwitchReadPath('pc')
        versioning.new_script_version_up()
        scriptFullPath = nuke.root()['name'].value()
        nuke.scriptSaveAs(scriptFullPath[:-7] + '.nk')


def saveSwitch():
    global username
    if username != 'SNKA':
        popup = False
    else:
        popup = True

    scriptPath = nuke.root()['name'].value()
    if '//nas/nas/' in scriptPath:
        newSavePath = scriptPath.replace('//nas/nas/', 'C:/LocalProjects/')
        if os.path.exists(os.path.split(newSavePath)[0]) == False: 
            os.makedirs(os.path.split(newSavePath)[0])
        nuke.scriptSaveAs(newSavePath)
        if popup == True:
            nuke.message("Now you're saved localy.")
    elif 'Z:/' in scriptPath:
        newSavePath = scriptPath.replace('Z:/', 'C:/LocalProjects/')
        if not os.path.exists(os.path.split(newSavePath)[0]): os.makedirs(os.path.split(newSavePath)[0])
        nuke.scriptSaveAs(newSavePath)
        if popup == True:
            nuke.message("Now you're saved localy.")
    elif 'C:/LocalProjects/' in scriptPath:
        newSavePath = scriptPath.replace('C:/LocalProjects/', '//nas/nas/')
        if not os.path.exists(os.path.split(newSavePath)[0]): os.makedirs(os.path.split(newSavePath)[0])
        nuke.scriptSaveAs(newSavePath)
        if popup == True:
            nuke.message("Now you're saved to network.")        

    print("Now the project is saved to %s" % (newSavePath))

def toggleSpecialNode():
    for n in nuke.allNodes():
        if n['label'].value() == 'tm':
            break

    n['disable'].setValue(not n['disable'].value())


def makeThisNodeSpecial():
    for n in nuke.allNodes():
        if n['label'].value() == 'tm': n['label'].setValue('')
    if len(nuke.selectedNodes()) > 0:
        nuke.selectedNode()['label'].setValue('tm')

def shiftNodes(direction = 'up'):
    n = nuke.selectedNodes()
    if len(n) == 0:
        nuke.message('Select nodes(s) please')
        return
    elif len(n) == 1:
        if direction == 'up':
            ypos = n[0].ypos() - 10
            nodes = [node for node in nuke.allNodes() if node.ypos() < ypos]
            for n in nodes:
                n.setYpos(n.ypos() - 100)
        else:
            ypos = n[0].ypos() + 10
            nodes = [node for node in nuke.allNodes() if node.ypos() > ypos]
            for n in nodes:
                n.setYpos(n.ypos() + 100)
    elif len(n) > 1:
            for node in n:
                if direction == 'down':
                    node.setYpos(node.ypos() + 100)
                else:
                    node.setYpos(node.ypos() - 100)

def viewportHotkey():
    from hiero.ui import findMenuAction
    pr = findMenuAction('Preferences...')
    pr.setShortcut('')
    nuke.menu('Nodes').addCommand('Little Helpers/Unused/Go to previous keyframe', 'nuke.activeViewer().frameControl(-4)', 'shift+s')
    nuke.menu('Viewer').addCommand('Go to previous keyframe', 'nuke.activeViewer().frameControl(-4)', 'shift+s')
    nuke.menu('Viewer').addCommand('Go to nextkeyframe', 'nuke.activeViewer().frameControl(4)', 'shift+d')

def colorNodes():
    color = nuke.getColor()
    for n in nuke.selectedNodes():
        n['tile_color'].setValue(color)

def copyColor():
    nodes = nuke.selectedNodes()
    color = nodes[-1]['tile_color'].value()
    for n in nodes[:-1]:
        n['tile_color'].setValue(color)

def afanasyFromWrites():
    nnodes = nuke.selectedNodes('Write')
    selectOnly()
    print(nnodes)
    for n in nnodes:
        first = n.firstFrame()
        last = n.lastFrame()
        selectOnly(n)
        af = nuke.createNode('afanasy', inpanel = False)
        af['framefirst'].setValue(first)
        af['framelast'].setValue(last)
        af['framespertask'].setValue(6)

def executeAfanasyNodes():
    nodes = nuke.selectedNodes('afanasy')
    for n in nodes:
        w = n.dependencies()[0]
        folder = os.path.dirname(w['file'].value())
        if not os.path.exists(folder):
            os.makedirs(folder)
            n['knob_1'].execute()

def findReducenoise():
    if nuke.allNodes('OFXcom.absoft.neatvideo4_v4') != []: print('__ There is at least one reduce noise node.')

def findReadWithPattern():
    pattern = nuke.getInput('Find:')
    if pattern:

        for n in nuke.allNodes('Read'):
            if pattern in n['file'].value(): 
                n.setSelected(True)

def renameHotboxFolders():
    tree = os.walk('/home/a.gamaiunov/ns/python/hotbox')
    for d, dirs, files in tree:
        if '.tmp' in d:
            os.rename(d, d.strip('.tmp'))
        if files:
            for f in files:
                if '.tmp' in f:
                    #print f
                    os.rename(os.path.join(d, f), os.path.join(d, f).strip('.tmp'))

nuke.addOnScriptLoad(viewportHotkey)

def bbox_to_crop():
    print('in bbox to crop')
    n = nuke.selectedNode()
    #n = nuke.toNode('Crop7')
    c = nuke.createNode('Crop')
    ct = nuke.createNode('CurveTool')

    if nuke.ask('Animated?'):
        ff = n.firstFrame()
        lf = n.lastFrame()

        print('%s %s' % (ff, lf))

        for f in range(ff, lf+1):
            #nuke.frame(f)
            #print 'frame ' + str(f)

            nuke.execute(ct, f, f)

            bb = n.bbox()
            x = bb.x()+1
            y = bb.y()+1
            w = bb.w()-1
            h = bb.h()-1

            c['box'].setAnimated(0)
            c['box'].setAnimated(1)
            c['box'].setAnimated(2)
            c['box'].setAnimated(3)
            #help(c['box'])
            c['box'].setValueAt(x, f, 0)
            c['box'].setValueAt(y, f, 1)
            c['box'].setValueAt(x+w-1, f, 2)
            c['box'].setValueAt(y+h-1, f, 3)
    else:
        f = nuke.frame()
        nuke.execute(ct, f, f)
        bb = n.bbox()
        x = bb.x() + 1
        y = bb.y() + 1
        w = bb.w() - 1
        h = bb.h() - 1

        c['box'].setAnimated(0)
        c['box'].setAnimated(1)
        c['box'].setAnimated(2)
        c['box'].setAnimated(3)
        # help(c['box'])
        c['box'].setValueAt(x, f, 0)
        c['box'].setValueAt(y, f, 1)
        c['box'].setValueAt(x + w - 1, f, 2)
        c['box'].setValueAt(y + h - 1, f, 3)

    nuke.delete(ct)