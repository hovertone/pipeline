#!/usr/bin/env python
import nuke, os, re, time
import platform




# ===============================================================================================
'''

=======================================================
'''

def getNodeList():
    ''' 
    If any node selected, returns list of selected nodes,
    and returns all nodes if none selected
    
    No arguments needed
    =======================================================
    '''
    if nuke.selectedNodes() == []:
        nodes = nuke.allNodes("Read")
    else:
        nodes = nuke.selectedNodes("Read")
    return nodes

# ===============================================================================================

def getCurFrame(path, frame):
    '''
    returns current frame full path
    from provided sequence path
    
    Arguments(path, frame)
        {path} in str form 'C:/Users/Administrator/Desktop/test/test_%04d.tga'
        {frame} str int form
    =======================================================
    '''
    if path.find('%') == -1:
        return False
    else:
        padd = int(path[path.find('%')+1: path.find('%')+3])
        return '/'.join([os.path.split(path)[0], os.path.splitext(os.path.split(path)[-1])[0][:os.path.splitext(os.path.split(path)[-1])[0].find('%')]+str(frame).zfill(padd)+ os.path.splitext(os.path.split(path)[-1])[-1]])


# ===============================================================================================

def getProjectFolder(path):
    if 'Z:/' in path:
        netwPath = path.replace('Z:/', '//nas/raidtwo/')
        pathToLookFor = '//' + '/'.join(netwPath[2:].split('/')[:3])
        if os.path.exists(pathToLookFor):
            return pathToLookFor
    elif '//nas/raidtwo/' in path:
        netwPath = path
        pathToLookFor = '//' + '/'.join(netwPath[2:].split('/')[:3])
        if os.path.exists(pathToLookFor):
            return pathToLookFor
    else:
        return False

# ===============================================================================================

def getProjectName(nodes = getNodeList()):
    '''
    Returns project name from selected Nodes or provided nodes
    
    Aruments(NodeList)
        {NodeList} in form of list of nodes. If no argument provided - list will be created from getNodeList() function
    =======================================================
    '''
        
    projectName = ""
    company = "other"
    
    for n in nodes:
        fullPath = n['file'].value().split('/')
        if ('SRC' or 'Src' or 'VIDEO' or 'Video' or 'IMAGES' or 'Images') in n['file'].value():
            company = "CP"
            for s in range(0, len(fullPath)):
                if 'SRC' in fullPath[s].upper():
                    projectName = fullPath[s-1]
                    break            
        elif '//nas/' in n['file'].value() or "Z:/" in n['file'].value(): 
            company = "chupa"
            for s in range(0, len(fullPath)):
                if 'raidtwo' in fullPath[s].lower():
                    projectName = fullPath[s+1]
                    break
                elif 'Z:/' in fullPath[s]: 
                    projectName = fullPath[s+1]
                    break  
        
    return projectName, company

# ===============================================================================================

def hsvToRGB(h, s, v):
    """Convert HSV color space to RGB color space
    
    @param h: Hue
    @param s: Saturation
    @param v: Value
    return (r, g, b)  
    =======================================================
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
    
# ===============================================================================================

def rgbToHSV(r, g, b):
    """Convert RGB color space to HSV color space
    
    @param r: Red
    @param g: Green
    @param b: Blue
    return (h, s, v) 
    ======================================================= 
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

# ===============================================================================================

def intColor(color):
    """Converts rgb value to integer single value
    
    Aruments(color)
        color - list type [r, g, b]
    ======================================================= 
    """    
    r = color[0]
    g = color[1]
    b = color[2]
    if len(color) > 3:
        a = color[3]
        clr = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,a*255),16)

    else:
        a = 0
        clr = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,a*255),16)

    return clr

# ===============================================================================================
    
def randomColor(satIn = 1.0, valIn = 1.0, alpha = 1):
    '''
    Returns random color int, which you can set to any color knob
    
    Arguments(satIn, valIn, alpha)
        {satIn} saturation from 0 to 1
        {valIn} saturation from 0 to 1
        {alpha} alpha from 0 to 1
    =======================================================    
    '''
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

# ===============================================================================================

def dependenciesSelect(nodesToClimb, cls = ''):
    '''
    Returns list of all dependencies nodes
    
    Arguments(nodeToClimb, cls)
        {nodeToClimb} node dependencies of which should be returned
        {cls} node class type to select, if argument passed then all nodes will be selected
    =======================================================
    '''
    
    nodesToSelect = []
    
    def climb(node):
        for n in node.dependencies():
            if cls != '':
                if n.Class() == cls:
                    nodesToSelect.append(n)
                climb(n)
            else:
                nodesToSelect.append(n)
                climb(n)
    
    for b in nodesToClimb:
            if cls != '':
                if b.Class() == cls:
                    nodesToSelect.append(b)
                climb(b)
            else:
                #nodesToSelect.append(b)
                climb(b)
    
    return nodesToSelect

# ===============================================================================================

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
        
# ===============================================================================================
        
def nodeToList(inpt):
    '''
    Returns list of nodes if node variable is porvided.
    
    Arguments(input)
        {input}
    =======================================================
    '''
    if type(inpt) != list:
        return [inpt]
    else:
        return inpt
    
# ===============================================================================================

def insertFolder(path, folder, create = False):
    '''
    Inserts folder between last Folder in path and file name.
    Creates is if you need
    
    Arguments(path, folder, create)
        {path} path string type where to insert a folder
        {folder} name of the folder you want to insert. string type
        {create} boolean. Set to True is u want to create folder
    =======================================================
    '''
    
    import os
    parts = os.path.split(path)
    folderPath = os.path.join(parts[0], folder).replace('\\', '/')
    newPath = os.path.join(parts[0], folder, parts[1]).replace('\\', '/')
    
    if create == True:
        if not os.path.exists(folder):
            os.mkdir(folder)
    
                      
    return newPath, folderPath

# ===============================================================================================

def fixPath(path):
    '''
    Fixes path string for Windows. Replaces \ or \\ with /.
    
    Arguments(path)
        {path} string to fix
    =======================================================
    '''
    newPath = path.replace('\\\\', '/')
    newPath = path.replace('\\', '/')
    
    return newPath


# ===============================================================================================

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
    
# ===============================================================================================

def paddingFix(path, padd = 4):
    '''
    Fixes path padding. %d becomes %04d (by default)
    
    Arguments(path, padd)
        {path} - path to fix, string type
        {padd} - number of digits in padding (4 by default)
    =======================================================   
    '''
    percIndex = path.find('%')
    if not isNumber(path[percIndex + 1]):
        return path[:percIndex+1] + '04' + path[percIndex+1:]
    else:
        return path[:percIndex+2] + '4' + path[percIndex+3:]    
    
# ===============================================================================================

def getFreeInputs(node, *args):
    '''
    Returns list of inputs of the provided node which are free. 

    Arguments (node, *args)
        node - free inputs of this node will be returned
        args - optional arguments. First provided will be as a frequency. Default value is 20
               For instance you need to look for free inputs of the scene node. Scene input has 
               a 999 inputs. Which meens that you will bee provided wil list of about 950 integers. 
               If you don't need all of those you can parce a freq value (lets say 20) and function 
               will check each 20 input, and if freeInputs are something around 20 (too little inputs 
               are occupied) function will be breaked and you will get not a infinite list of values.
               Second and next args will be printed as a unknown args.
    =======================================================
    '''
    # This list wil be filled and returned
    freeInputs = []

    unknownArgs = []
    freq = 20
    # Sorting args. First will be recognized as a frequency to check. Default is 20
    for keyi in range(0, len(args)):
        if keyi == 0:
            freq = args[keyi]
        else:
            unknownArgs.append(args[keyi])

    # Loop through all of the inputs of the node
    for i in range(0, node.maxInputs()):
        # If input is free then append it to our list
        if node.input(i) == None:
            freeInputs.append(i)
        # If index is 20 or 40 or 60 and list lenght is something between 12-20 or 24-40 pr 36-60 items then break and stop counting
        if (i % freq  == 0 ) and (len(freeInputs) > i * 0.6):
            break

    # If Unknown args are exist
    if unknownArgs != []:
        # print them
        print('Unknown args were provided: %s' % (unknownArgs))

    return freeInputs

# ===============================================================================================
    
def commonPrefix(m):
    '''
    Given a list of pathnames, returns the longest common leading component

    Arguments (m)
        m - list of strings with common substring to find. List type
    =======================================================
    '''
    if not m: return ''
    s1 = min(m)
    s2 = max(m)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1


# ===============================================================================================

def returnAnimatedNodes(selNodes):   
    '''
    Returns nodes with animated knobs (from provided ones)

    Arguments(selNodes)
        selNodes - which nodes to look for animated knobs
    =======================================================
    ''' 
    nodesToShow = []
    for n in selNodes:
        knobs = n.knobs()
        keys = knobs.keys()
        for key in keys:
            if knobs[key].isAnimated():
                nodesToShow.append(n)
                break
    
    return nodesToShow    

# ===============================================================================================

def removeInputs(node):
    '''
    Removes all input connections of node

    Arguments(node)
        node - node to remove input connections
    =======================================================
    '''     
    for j in range(node.inputs()): 
        node.setInput(j, None)

# ===============================================================================================

def openE():
    '''
    Opens a Windows Explorer with a path from file-knob of the node

    Arguments()
        * no arguments provided because of the fact that the function uses file-knob
        of the node.
    =======================================================
    '''      
    from CUF import fixPath
    from subprocess import Popen
    import re
    path = nuke.thisNode()['file'].value()
    path = os.path.split(path)[0]
    path = fixPath(os.path.join(path, os.listdir(path)[0]))

    fixedPath = path.replace('/', '\\')
    Popen(r'explorer /select, "%s"' % fixedPath)
    
# ===============================================================================================

def createAndMoveNode(newNodeClass, selNode = [], x = 0, y = 0, offsetNode = [], inpanel = False):
    '''
    Creates node. Also can move node in nodegraph

    Arguments(newNodeClass, selNode = [], x = 0, y = 0, offsetNode = [], inpanel = False)
        newNodeClass - class of the node to be created
        selNode - nodes to select before creating of the new one. -1 will deselect all of the nodes
        x, y - x and y offsets
        offsetNode - node to offset from. If this arguments is missing then selected node will count
          as offsetNode
        inpanel - argument to open a propery window when node has been created
    =======================================================
    '''  
    if selNode == -1:
        selectOnly()
    elif selNode != []:
        selNode = nodeToList(selNode)
        for n in selNode:
            n.setSelected(True)


    n = nuke.createNode(newNodeClass, inpanel = False)
    if offsetNode != []:
        n.setXYpos(offsetNode.xpos() + x, offsetNode.ypos() + y)
    elif x != 0 or y != 0:
        offsetNode = nuke.selectedNode()
        n.setXYpos(offsetNode.xpos() + x, offsetNode.ypos() + y)

    return n

# ===============================================================================================
def returnVersion(str):
    '''
    Returns a version of provided string

    Arguments(str):
        str - string to find the version
    =======================================================
    '''  
    result = re.search(r'[vV]\d+.', str)
    if result:
        return result.group()[:-1]
    else:
        return False

# ===============================================================================================
def returnVersionFilmua():
    return nuke.root().name()[-4:-3]  # A|B|C|D patterns


# ===============================================================================================
def moveToBegin(listToEdit, desiredElements):
    '''
    Moves a desire elements to the beginning of the list. Moves in a way (position of elements) it was povided

    Arguments(listToEdit, desiredElements)
        listToEdit - list to sort
        desiredElements - patern of elements to move to the beginning

    returns listToEdit(sorted list), desiredElements, unsorted (list of elements from filrst list which has not been sorted)
    =======================================================
    '''
    for d in reversed(desiredElements):
        if d in listToEdit:
            listToEdit.insert(0, listToEdit.pop(listToEdit.index(d)))

    unsorted = []
    for i in listToEdit:
        if i not in desiredElements:
                unsorted.append(i)


    return listToEdit, desiredElements, unsorted

# ===============================================================================================

def platformBasedFixPath(path):
    if os.name == 'nt':
        if 'Z:/' in path:
            path = path.replace('Z:/', '//nas/nas/')
        else:
            pass

        return fixPath(path)

# ===============================================================================================

def getFilteredList(folder, fltr = '', forFolder = True, showAllPath = True):   
    '''
    Returns a list of folder / files from provided path. Output depends of optional arguments.

    Arguments (folder, fltr, forFolder, showAllPath)
        folder      - path to a folder. String type
        fltr        - filter to search for. '' means no filter. String type.       '' - Default value
        forFolder   - Boolean type to look for folders or files. 
                      Non booleam type will return both folders and files       True - Default value
        showAllPath - True will return list of whole paths, False - only the 
                    names of a files / folders.  True - Default value
    =======================================================
    '''
    try:
        if folder[-1] == '/': folder = folder[:-1]
        #nuke.message(folder)
        if showAllPath == True:
            if forFolder == True:
                fltredList = [ folder + '/' + f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder,f)) and fltr in f]
            else:
                fltredList = [ folder + '/' + f for f in os.listdir(folder) if fltr in f and not os.path.isdir(os.path.join(folder,f))]
        else:
            if forFolder == True:
                fltredList = [ f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder,f)) and fltr in f]
            else:
                fltredList = [ f for f in os.listdir(folder) if fltr in f and not os.path.isdir(os.path.join(folder,f))]
            
        fltredList.sort()
        # if int(getPadding(fltredList[0])[0]) < 1:
        #   fltredList = fltredList[::-1]

        return fltredList
    except:
        return False

# ===============================================================================================

def getFileList(path, fltr = '', forFolder = False, fullPath = False, diveOnes = False):
    '''
    Returns a list of folder / files from provided path. Output depends on optional arguments.

    Arguments (folder, fltr, forFolder, fullPath)
        folder      - path to a folder. String type
        fltr        - filter to search for. '' means no filter. String type.       '' - Default value
        forFolder   - Boolean type to look for folders or files. 
                      Non booleam type will return both folders and files       True - Default value
        fullPath - True will return list of whole paths, False - only the 
                    names of a files / folders.  True - Default value
        diveOnes - If True, function will return the content of folder path of which has been provided
                    Basically the content of folder level 1. Boolean type. False - default value
    =======================================================
    '''
    returnList = []
    if path[-1] == '/': path = path[:-1]
    for d, dirs, files in os.walk(path):
        # Files
        if forFolder == False:
            for f in files:
                if fltr in f:
                    if fullPath == True:
                        path = platformBasedFixPath(os.path.join(d,f))
                    else:
                        path = f
                    returnList.append(path)
        # Folders
        elif forFolder == True:
            for f in dirs:
                if fltr in f:
                    if fullPath == True:
                        path = platformBasedFixPath(os.path.join(d,f))
                    else:
                        path = f
                    returnList.append(path)

        # Both
        else:
            for f in dirs:
                if fltr in f:
                    if fullPath == True:
                        path = platformBasedFixPath(os.path.join(d,f))
                    else:
                        path = f
                    returnList.append(path)
                if diveOnes == True: break

            for f in files:
                if fltr in f:
                    if fullPath == True:
                        path = platformBasedFixPath(os.path.join(d,f))
                    else:
                        path = f
                    returnList.append(path)
        if diveOnes == True: break

    return returnList

# ===============================================================================================

def replaceListItem(lst, searchFor, replaceWith):
    '''
    Repaces a list item with provided new one.

    Arguments (lst, searchFor, replaceWith)
        lst         - the list to replace where. list type
        searchFor   - item to look for. (type should match the list items type)
        replaceWith - item to replace with.
    =======================================================
    '''
    for n, i in enumerate(lst):
        if i == searchFor:
            lst[n] = replaceWith
    return lst

# ===============================================================================================

def toggleKnobEnable(knob = nuke.thisKnob()):
    '''
    Toggle knob enabled func

    Arguments (knob)
        knob - knob to toggle. Default parameter value 'nuke.thisKnob()'
    =======================================================
    '''
    value = knob.value()
    knob.setEnabled(not value)

# ===============================================================================================

def dropData(path):

    '''
    Almsot the same as nukescripts.dropData except this func will delete all error read nodes
    and return a list of newly create read nodes.

    Arguments (path)
        path - folder path (string type) to import from
    =======================================================
    '''
    from nukescripts import dropData

    prevNodes = nuke.allNodes()
    dropData('', path)
    allNodes = nuke.allNodes()

    addedNodes = []
    delete = []
    for n in allNodes:
        if (n not in prevNodes) and (n.error() == False): 
            addedNodes.append(n)
        elif n.error() == True:
            delete.append(n)

    for n in delete:
        nuke.delete(n)

    return [n for n in addedNodes if n.Class() == 'Read']

# ===============================================================================================

def replaceListItem(list, index, item):
    list.pop(index)
    list.insert(index, item)

# ===============================================================================================

def noteTime(start, comment = '', tprint = True):
    '''
    Returns a print of measured time between START and current time.

    Arguments (start, comment, tprint):
        start - is time.time() value to start from
        comment - text to attach before of timing number in print string (string type)
        tprint - boolean either or not to print this in terminal (nuke only)
    =======================================================
    '''

    #return 1.0 # EXIT

    end = time.time()
    timeElapsed = str(round(float(end - start), 2))  # string
    if tprint == True:
        if comment != '':
            nuke.tprint(comment + ': ' + timeElapsed + 's')
        else:
            nuke.tprint(timeElapsed + 's')
    else:
        if comment != '':
            print(comment + ': ' + timeElapsed + 's')
        else:
            print(timeElapsed + 's')
    return end

# ===============================================================================================

def checkNodesNameExistence(nodeName):
    for n in nuke.allNodes():
        if nodeName == n['name'].value():
            return True
    return False

# ===============================================================================================

def renameMochaCornerPin():
    nodes = nuke.allNodes('CornerPin2D')
    for n in nuke.allNodes('Tracker3'):
        nodes.append(n)

    for n in nodes:
        if 'CornerPin2D' in n['name'].value():
            newName = n['name'].value().replace('CornerPin2D', 'M') + '_01'
            while checkNodesNameExistence(newName):
                print(newName[-2:])
                if isNumber(newName[-2:]):
                    currentDigit = int(newName[-2:])
                    newDigit = str(currentDigit + 1).zfill(2)
                    newName = newName.replace(str(currentDigit).zfill(2), newDigit)

            n['name'].setValue(newName
)
# ===============================================================================================

def getMostBottomNode(nodes = None):
    if not nodes:
        x = nuke.selectedNode()
    else:
        if type(nodes) == list:
            x = nodes

    end = 0
    while end == 0:
        try:
            x = x.dependent()[0]
        except:
            lastNode = x
            end = 1
    #nuke.selectedNode()['selected'].setValue(0)
    return lastNode

# ===============================================================================================

def alignNodeToNode(n1, n2, axis = 'x', check = False):
    if axis != 'x' and axis != 'y':
        print('incorrent axis. No actions applied.')
        return None

    if check == True:
        posDict = {n2: (n2.xpos(), n2.ypos())}
    n1center = [n1.xpos() + n1.screenWidth()/2, n1.ypos() + n1.screenHeight()/2]

    if axis == 'x':
        n2.setYpos(n1center[1] - n2.screenHeight()/2)
    else:
        n2.setXpos(n1center[0] - n2.screenWidth()/2)

    if check == True:
        newPosDict = {n2: (n2.xpos(), n2.ypos())}
        if newPosDict == posDict:
            return False
        else:
            return True

# ===============================================================================================

def upstream(startNode, maxDepth=-1, found=set([])):
    if maxDepth != 0:
       newDeps = set([n for n in nuke.dependencies(startNode) if n not in found])
       found |= newDeps
       for dep in newDeps:
          upstream(dep, maxDepth - 1, found)
    return found

# ================================================================================================

def makeAtristicTileColors():
    for n in nuke.selectedNodes():
        n['tile_color'].setValue(1149486591)

# ================================================================================================

def creationDate(path_to_file):
    """
    Taken from http://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    import platform
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


def hotboxFix():
    p = 'C:/Users/Admin/ns/python/hotbox/All'
    for f in os.listdir(p):
        fullPath = os.path.join(p, f)
        if os.path.isdir(fullPath):
            for i in os.listdir(fullPath):
                os.rename(os.path.join(fullPath, i), os.path.join(fullPath, i).strip('.tmp'))

        print(os.path.join(p, f))
        os.rename(os.path.join(p, f), os.path.join(p, f).strip('.tmp'))







