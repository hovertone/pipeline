import nuke, os, platform, time, nukescripts

def selectOnly(nodes = []):
    '''
    Deselects all nodes, and selects nodes from provided list of nodes
    
    Arguments(nodes)
        {nodes} list of the nodes to select ([ by default])
    =======================================================
    '''
    nuke.selectAll()
    nuke.invertSelection()
    if type(nodes) == list:
        for n in nodes:
            n.setSelected(True)
    else:
        nodes.setSelected(True)

def addFrameRangeLockExpression(n):
    n['use_limit'].setValue(True)
    n['first'].setExpression('[python {nuke.thisNode().dependencies()[0].firstFrame()}]')
    n['last'].setExpression('[python {nuke.thisNode().dependencies()[0].lastFrame()}]')

def addBeforeRenderExpression(n):
    n['beforeRender'].setValue("if not os.path.exists(os.path.dirname(nuke.thisNode()['file'].value())): os.makedirs(os.path.dirname(nuke.thisNode()['file'].value()))")
        

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


#AUTOPLACE
def getXpos(n):
    return n.xpos()

def autoplace():
    nodes = sorted(nuke.selectedNodes(),key=getXpos)
    
    for i in range(len(nodes)):
        nodes[i].setXYpos(nodes[0].xpos() + i*110,nodes[0].ypos())


def creationDate(path_to_file):
    """
    Taken from http://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return time.ctime(stat.st_birthtime)
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return time.ctime(stat.st_mtime)


def isNumber(s):
    '''
    Checks if provided str contains numbers.
    
    Arguments(s)
        {s} string to check
    =======================================================
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False
    
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
        

def autocropSelected(layer = 'rgb'):
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

# ===============================================================================================

def renameMochaCornerPin():
    nodes = nuke.allNodes('CornerPin2D')
    for n in nuke.allNodes('Tracker3'):
        nodes.append(n)

    for n in nodes:
        if 'CornerPin2D' in n['name'].value():
            newName = n['name'].value().replace('CornerPin2D', 'M') + '_01'
            while checkNodesNameExistence(newName):
                print newName[-2:]
                if isNumber(newName[-2:]):
                    currentDigit = int(newName[-2:])
                    newDigit = str(currentDigit + 1).zfill(2)
                    newName = newName.replace(str(currentDigit).zfill(2), newDigit)

            n['name'].setValue(newName)

# ===============================================================================================

def afanasyFromWrites():
    nnodes = nuke.selectedNodes('Write')
    selectOnly()
    print nnodes
    for n in nnodes:
        first = n.firstFrame()
        last = n.lastFrame()
        selectOnly(n)
        af = nuke.createNode('afanasy', inpanel = False)
        af['framefirst'].setValue(first)
        af['framelast'].setValue(last)
        af['framespertask'].setValue(6)

# ===============================================================================================

def executeAfanasyNodes():
    nodes = nuke.selectedNodes('afanasy')
    for n in nodes:
        w = n.dependencies()[0]
    folder = os.path.dirname(w['file'].value())
    if not os.path.exists(folder): os.makedirs(folder)
    n['knob_1'].execute()

# ===============================================================================================

def splitCamsFromAbc(abcpath):
   """ Function to load Multiple camera form Alembic file
   Args:
       abcpath (str): Alembic file path
   """
   infoCam = nuke.createNode(
       'Camera2', 'file {%s} read_from_file True' % abcpath)
   camlist = infoCam['fbx_node_name'].values()

   # Create Cam from List
   for i, c in enumerate(camlist):
       cam = nuke.createNode(
           'Camera2', 'file {%s} read_from_file True' % abcpath)
       cam.setSelected(False)
       cam.setXYpos(infoCam.xpos() + 110 * (i + 1), infoCam.ypos())
       cam['fbx_node_name'].setValue(i)
       cam['name'].setValue(os.path.basename(os.path.dirname(c)))

   # Delete Info CamNode
   nuke.delete(infoCam)

# ===============================================================================================
def duplicateNode(node, to_file = None):
    """Slightly convoluted but reliable(?) way duplicate a node, using
    the same functionality as the regular copy and paste.
    Could almost be done tidily by doing:
    for knobname in src_node.knobs():
        value = src_node[knobname].toScript()
        new_node[knobname].fromScript(value)
    ..but this lacks some subtly like handling custom knobs
    to_file can be set to a string, and the node will be written to a
    file instead of duplicated in the tree
    """

    # Store selection
    orig_selection = nuke.selectedNodes()

    # Select only the target node
    [n.setSelected(False) for n in nuke.selectedNodes()]
    node.setSelected(True)

    # If writing to a file, do that, restore the selection and return
    if to_file is not None:
        nuke.nodeCopy(to_file)
        [n.setSelected(False) for n in orig_selection]
        return


    # Copy the selected node and clear selection again
    nuke.nodeCopy("%clipboard%")
    node.setSelected(False)

    if to_file is None:
        # If not writing to a file, call paste function, and the new node
        # becomes the selected
        nuke.nodePaste("%clipboard%")
        new_node = nuke.selectedNode()

    # Restore original selection
    [n.setSelected(False) for n in nuke.selectedNodes()] # Deselect all
    [n.setSelected(True) for n in orig_selection] # Select originally selected

    return new_node

    