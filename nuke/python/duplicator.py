import nuke
import os
import shutil
import sys
import fileinput
import time

# ===============================================================================================

def getNodeList():
    ''' 
    If any node selected, returns list of selected nodes,
    and returns all nodes if none selected
    '''
    if nuke.selectedNodes() == []:
        nodes = nuke.allNodes("Read")
    else:
        nodes = nuke.selectedNodes("Read")
    return nodes


# ===============================================================================================

def findCurFrame(path, frame):
    '''
    returns current frame full path
    from provided sequence path 
    '''
    if path.find('%') == -1:
        return False
    else:
        padd = int(path[path.find('%')+1: path.find('%')+3])
        return '/'.join([os.path.split(path)[0], os.path.splitext(os.path.split(path)[-1])[0][:os.path.splitext(os.path.split(path)[-1])[0].find('%')]+str(frame).zfill(padd)+ os.path.splitext(os.path.split(path)[-1])[-1]])


# ===============================================================================================

def createProxy(nodes = getNodeList()):
    if nuke.selectedNodes() == []:
        if not nuke.ask("Do you really want to create proxy files for all read nodes?"):
            return   
        
    selection = nuke.selectedNodes()      
    
    nuke.root()['proxy'].setValue(False)
    
    brokenReads = []
    for r in nodes:
        # deselect all nodes
        nuke.selectAll() 
        nuke.invertSelection() 
        colorSpace = r['colorspace'].value()
        
        print 'first frame is', findCurFrame(r['file'].value(), r['first'].value())
        print 'exists is', os.path.exists(findCurFrame(r['file'].value(), r['first'].value()))
#        if 'knob' in r['file'].value():
#            readPath = r['local'].value()
#            
#        elif os.path.exists(findCurFrame(r['file'].value(), r['first'].value())) or os.path.exists(r['file'].value()):
#            readPath = r['file'].value()
#        else:
#            brokenReads.append(r['name'].value())
#            break
        
        if '[knob' in r['file'].value(): 
            readPath = r['local'].value() #################################
        else:
            readPath = r['file'].value() #################################
        
        print "read path is", readPath
        
        #select current node to add reformat and write nodes
        r.setSelected(True)
        
        ref = nuke.createNode("Reformat")
        ref['type'].setValue('2')
        ref['scale'].setValue(0.5)
        ref['filter'].setValue('Rifman')
        
        w = nuke.createNode('Write')
        w['channels'].setValue('all')
        
        
        proxyPath = '/'.join(readPath.split('/')[:-1]) + "/proxy/" + readPath.split('/')[-1]
        if not os.path.exists('/'.join(proxyPath.split('/')[:-1])):
            os.mkdir('/'.join(proxyPath.split('/')[:-1]))
        
        w['file'].setValue(proxyPath)
        w['colorspace'].setValue(r['colorspace'].value())
        
        w['channels'].setValue('all')        
        
        try: 
            media = proxyPath.split('/')[-1]
            # if sequence 
            if not media.find('%') == -1:
                # print "sequence"
                if proxyPath[media.find('%')+1] != 'd':
                    padd = int ( media[media.find('%')+2:media.find('%')+3] )
                else:
                    padd = 1
                
                exist = True
                
                mediaFolder = '/'.join(readPath.split('/')[:-1])
                ext = proxyPath.split('/')[-1][-4:]
                seqName = media[0:(media.find('%')-1)]
                seqNameDot = media[0:media.find('%')]  
                
                # Check if proxy files already exists
                for f in range(r['first'].value(), r['last'].value()+1):
                    print mediaFolder + '/' + seqNameDot + str(f).zfill(padd) + ext
                    if not os.path.exists(mediaFolder + '/proxy/' + seqNameDot + str(f).zfill(padd) + ext):
                        exist = False
                        break
                
                # if proxy files doesn't exist create them
                if exist == False:
                    print 'Lets render proxy'
                    nuke.execute(w.name(), r['first'].value(), r['last'].value())
                    r['proxy'].setValue(proxyPath)               
                else:
                    r['proxy'].setValue(proxyPath)  
            #not sequence
            else:
                if not os.path.exists(proxyPath):
                    nuke.execute(w.name(), r['first'].value(), r['last'].value())
                    r['proxy'].setValue(proxyPath)
                else:
                    r['proxy'].setValue(proxyPath)                    
        finally:
            nuke.delete(w)
            nuke.delete(ref)
            
    if brokenReads != []:        
        nuke.message('%s node has wrong file path' % ('\n'.join(brokenReads)))
        
    nuke.selectAll()
    nuke.invertSelection()
    
    for n in selection:
        n.setSelected(True)

# ===============================================================================================

def findProjectName():
    nodes = getNodeList()
    
    projectName = "none"
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

def findShotName(node):
    pathSplit = node['file'].value().split('/')
    if pathSplit[-1].find('%') != -1:
        if pathSplit[-1][pathSplit[-1].find('%')-1] == '_' or pathSplit[-1][pathSplit[-1].find('%')-1] == '.' or pathSplit[-1][pathSplit[-1].find('%')-1] == '-':
            media = pathSplit[-1][:pathSplit[-1].find('%')-1]
        else:
            media = pathSplit[-1][:pathSplit[-1].find('%')]
    else:
        media = pathSplit[-1][:pathSplit[-1].find('.')]
    
    return pathSplit[-3], pathSplit[-2], media


# ===============================================================================================

def findShotName(node):
    pathSplit = node['file'].value().split('/')
    if pathSplit[-1].find('%') != -1:
        if pathSplit[-1][pathSplit[-1].find('%')-1] == '_' or pathSplit[-1][pathSplit[-1].find('%')-1] == '.' or pathSplit[-1][pathSplit[-1].find('%')-1] == '-':
            media = pathSplit[-1][:pathSplit[-1].find('%')-1]
        else:
            media = pathSplit[-1][:pathSplit[-1].find('%')]
    else:
        media = pathSplit[-1][:pathSplit[-1].find('.')]
    
    return pathSplit[-3], pathSplit[-2], media            

# ===============================================================================================

def reCopy():    
    n = nuke.thisNode()
    
    # Get the file path value and split it
    fullPath = n.knob('netw').getValue()
    # Split the path
    splitPath = fullPath.split('/')  # nuke UNIXfies paths LOL
    # Get the file folder location
    mediaPath = splitPath[-2]
    # Get the file name
    daMedia = splitPath[-1]
    # get the extension || format    
    fExt = daMedia[daMedia.find('.', -5):]    
    # Check if media is sequence
    
    progTask = nuke.ProgressTask("Collecting...") 
    
    if not daMedia.find('%') == -1:
        seqFolder = fullPath[0:fullPath.find(daMedia)]
        if '%' in daMedia:
            if daMedia[daMedia.find('%')+1] != 'd':
                padd = int ( daMedia[daMedia.find('%')+2:daMedia.find('%')+3] )
            else:
                padd = 1

        startFrame = int( n.knob('first').getValue() )
        endFrame = int( n.knob('last').getValue() )

        seqName = daMedia[0:(daMedia.find('%')-1)]
        seqNameDot = daMedia[0:daMedia.find('%')]                

        newSeqFolder = '/'.join(n['local'].value().split('/')[:-1])

        os.chdir(newSeqFolder)                    

        for f in range(startFrame, endFrame+1):    # don't omit last image
            ## PROGRESS DIALOG >> if the collect task is cancelled
            if progTask.isCancelled():
                nuke.message("Media files might not be complete")
                progTask.setProgress(100)
                del progTask  
                break
                
            #delete existing local file
            fileToDelete = findCurFrame(n['local'].value(), f)
            try:
                os.remove(fileToDelete)
            except WindowsError:
                pass

            # variable for progress percent
            percent = int( (float(f) / float(endFrame)) * 100.0 )
            # print "[ FRAME %s ]  [ end frame %s ]  [ percent %s ]" %(f, endFrame, percent)                        

            # SET PROGRESS
            progTask.setProgress(percent)                        

            # compile var for copying
            # current file on the current sequence
            curFile = seqFolder + seqNameDot + str(f).zfill(padd)+fExt                        

            # copy or new file
            copyFile = seqNameDot + str(f).zfill(padd)+fExt

            # Finally actually copy the files                
            shutil.copy(curFile, copyFile)                        

            ## SHOW THE CURRENT SEQUENCE IN PROGRESS
            progTask.setMessage("Copying: " + seqNameDot + str(f).zfill(padd)+fExt  )                        
    
    else:
        ######################################################################################
        #
        #                         NOT SEQUENCE
        #
        ######################################################################################

        newDestFolder = '/'.join(n['local'].value().split('/')[:-1])

        if progTask.isCancelled():
            nuke.message("Media files might not be complete")
            progTask.setProgress(100)
            del progTask 
            return
          
        # SET PROGRESS
        progTask.setProgress(0)                        

        # Finally actually copy the files
#        print "newDestFolder is %s. \nfullPath is %s \ndaMedia is %s" %(newDestFolder, fullPath, daMedia)
        os.chdir(newDestFolder)
        shutil.copy(fullPath, daMedia) 

        progTask.setProgress(100)
        del progTask 
        
# ===============================================================================================

def panelDuplicator(proxyEnable = True):
    if len(nuke.selectedNodes('Read')) < 1:
        nuke.message('Select Read nodes, please.')
        return      
    p = nuke.Panel("Duplicator", 450)
    p.addFilenameSearch("Select local projects dir:",  "C:/LocalProjects/")
    findProjectNameResult = findProjectName()
    # print findProjectNameResult
    if '[knob' in nuke.selectedNodes()[0]['file'].value():
        path = nuke.selectedNodes()[0]['netw'].value()
    else:
        path = nuke.selectedNodes()[0]['file'].value()
    pulldownChoice = ' '.join(path.split('/')[1:-1])
    p.addEnumerationPulldown("Project Name:", pulldownChoice)
    p.addSingleLineInput('Or type it here:', '')
        
    p.addBooleanCheckBox("Relative Path", "True") 
    p.addBooleanCheckBox("Override Duplicator connections", "True") # True
    if proxyEnable == True:
        p.addBooleanCheckBox("Create proxy files", "False") # True
    p.addButton("Cancel")
    p.addButton("OK")

    result = p.show()


    # IF OK
    if result == 1:
        if p.value("Select local projects dir:")[-1] == '/':
            outDir = p.value("Select local projects dir:")[:-1]
        else:
            outDir = p.value("Select local projects dir:")
        
        if proxyEnable == True:    
            renderProxy = p.value("Create proxy files")
        else:
            renderProxy = False
            
        rel = p.value("Relative Path")


        # IF user didn't chose a folder than message and execute MainFunc again,
        # then return

        if outDir == "Choose dir" or not os.path.exists(outDir):
            nuke.message("Select existing local projects folder, please")
            mainFuncDuplicator()
            return
        
        print outDir[-1]
#        if outDir[-1] == '/':
#            outDir = outDir[:-2]
        
        print "Outdir is", outDir
        
        if p.value('Or type it here:') == '':
            projectName = p.value("Project Name:")
        else:
            projectName = p.value('Or type it here:')
            
        if rel == True and projectName not in path:
            nuke.message("Can't use relative path because project name %s in not in %s" % (projectName, str(path)))
            mainFuncDuplicator()
            return            
            
#        if projectName == "Set the Project Name (not shot or scene)":
#            nuke.message("You should set the project name (again, not shot or scene)")
#            mainFuncDuplicator()
#            return

        nodes = getNodeList()
            
        if p.value("Override Duplicator connections") == False:
            trueNodes = []
            for n in nodes:
                print 'knob' in n['file'].value()
                if not 'knob' in n['file'].value():
                    print 'in'
                    trueNodes.append(n)
            nodes = trueNodes
            
        for n in range(0, len(nodes)):
            if nodes[n].error():
                nodes.pop(n)

        if nodes == []:
            nuke.message("No appropriate Read nodes are selected. Dismiss")
            return

        # Return Values
        
        print "find project name result is", findProjectNameResult
        if findProjectNameResult[1] == 'CP':
            print "CP"
            pluginPaths =  nuke.pluginPath()
            for p in pluginPaths:
                path = p.split('/')
                if path[-1] == '.nuke':
                    dotNukePath = p
    
            txt_name = str(dotNukePath) + '/' + 'checkCompany.txt'
            
            phrases = ['Coffee POST? sweet)', 'Coffee POST still using my stuff? COOL)', 'Looks like u find my script really usefull. Thanks)', 'If u want, u can contats me at gamaiunchik@gmail.com. \n Messages like this will never appear again. Good luck!)']
            
            if not os.path.exists(txt_name):
                print "we're in creation txt file part"
                nuke.message(phrases[0])
                file = open(txt_name, 'w')
                file.write("0")
                file.close()
            else:
                print "file exists"
                file = open(txt_name, 'r')
                if time.time() - os.path.getmtime(txt_name) > 604800 and file.read() == '0':
                    nuke.message(phrases[1]) 
                    file = open(txt_name, 'w')
                    file.write("1")
                    file.close()
                elif time.time() - os.path.getmtime(txt_name) > 1814400 and file.read() == '1':
                    nuke.message(phrases[2]) 
                    file = open(txt_name, 'w')
                    file.write("2")
                    file.close()
                elif time.time() - os.path.getmtime(txt_name) > 3024000 and file.read() == '2':
                    nuke.message(phrases[3]) 
                    file = open(txt_name, 'w')
                    file.write("3")
                    file.close()    
                else:
                    file.close()          
        
        return outDir, projectName, nodes, renderProxy, rel       

    # IF pressed cancel just print and return nothing
    else:
        print "You pressed cancel!"
        return




# ===============================================================================================    

#def folderCreator(localProjects, projectName):
#    folders = []
#    def climb(list, currentDir):
#        for j in list:
#            if type(j) == str:
#                folders.append(currentDir + '/' + j)
#            else:
#                climb(j, currentDir + '/' + j)
#        

#    folderScheme = ["projectName",[["00_OUT",["Client", "Dailies", "Master"]],["SRC", ["AUDIO", "IMAGES", "VIDEO"]]]]
#    climb(folderScheme, localProjects)#    

#    print folders

#folderCreator('test', 'Z:')    

# ===============================================================================================

def folderCreator(localProjects, projectName):
    foldersList = ['_DUPLICATOR', '_DUPLICATOR/IMAGES', '_DUPLICATOR/VIDEO']
    
    projectFolder = localProjects + '/' + projectName
    if not os.path.exists(projectFolder):
        os.mkdir(projectFolder)
    for i in foldersList:
        if not os.path.exists(projectFolder + '/' + i):
            os.mkdir(projectFolder + '/' + i)           

        

# ===============================================================================================


def pathSwitch(n = getNodeList()):
    if nuke.selectedNodes() == []:
        nodes = nuke.thisNode()
    else:        
        allNodes = nuke.selectedNodes("Read")
        nodes = []
        for n in allNodes:
            if 'knob' in n['file'].value():
                nodes.append(n)

    localCount = 0
    for n in nodes:
        if n['file'].value() == '[knob local]':
            localCount += 1
            
    if len(nodes)/(localCount+0.0000001) <= 2:
        local = True
    else:
        local = False
    
    for n in nodes:
        if n.Class() == "Read":
            if local == False:
                n['file'].setValue('[knob local]')
                n['file'].setEnabled(False)
                n['tile_color'].setValue(intColor([0.498, 1, 0.985]))                    

            else:
                n['file'].setValue('[knob netw]')
                n['file'].setEnabled(False)
                n['tile_color'].setValue(intColor([1, 0.4, 0.4]))   
    
#    if n.Class() == "Read":
#        if n['file'].value() == '[knob netw]':
#            n['file'].setValue('[knob local]')
#            n['file'].setEnabled(False)
#            n['tile_color'].setValue(intColor([0.498, 1, 0.985]))
#                
#
#        else:
#            n['file'].setValue('[knob netw]')
#            n['file'].setEnabled(False)
#            n['tile_color'].setValue(intColor([1, 0.4, 0.4]))    

# ===============================================================================================    


#def pathSwitchAll():
#    allNodes = nuke.allNodes("Read")
#    nodes = []
#    for n in allNodes:
#        if 'knob' in n['file'].value():
#            nodes.append(n)
#
#    for n in nodes:
#        if n.Class() == "Read":
#            if n['file'].value() == '[knob netw]':
#                n['file'].setValue('[knob local]')
#                n['file'].setEnabled(False)
#                n['path'].setValue('Local')
#                n['tile_color'].setValue(intColor([0.498, 1, 0.985]))                    
#
#            else:
#                n['file'].setValue('[knob netw]')
#                print n.knobs()
#                n['path'].setValue('Network')
#                n['file'].setEnabled(False)
#                n['tile_color'].setValue(intColor([1, 0.4, 0.4]))    
# 
 # ===============================================================================================            
 
def pathSwitchAll():
    allNodes = nuke.allNodes("Read")
    nodes = []
    for n in allNodes:
        if 'knob' in n['file'].value():
            nodes.append(n)

    localCount = 0
    for n in nodes:
        if n['file'].value() == '[knob local]':
            localCount += 1
            
    if len(nodes)/(localCount+0.0000001) <= 2:
        local = True
    else:
        local = False
    
    for n in nodes:
        if n.Class() == "Read":
            if local == False:
                n['file'].setValue('[knob local]')
                n['file'].setEnabled(False)
                n['tile_color'].setValue(intColor([0.498, 1, 0.985]))                    

            else:
                n['file'].setValue('[knob netw]')
                n['file'].setEnabled(False)
                n['tile_color'].setValue(intColor([1, 0.4, 0.4]))   

# ===============================================================================================            

def intColor(color):
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
def createDuplicatorKnobs(n, kl = None):
    tab = nuke.Tab_Knob('duplicator', 'Duplicator')
                            
    kn = nuke.File_Knob('netw', "network path")
    if 'Z:/' in n['file'].value():
        netwPath = n['file'].value().replace('Z:', '//nas/nas')
    else:
        netwPath = n['file'].value()
    kn.setValue(netwPath)
    kn.setTooltip('Network path to file')
    
    if kl != None:                
        kl.setTooltip('Local path to file')
    else:
        kl = nuke.File_Knob('local', "local path")
        kl.setValue("")
        
    button = nuke.PyScript_Knob('button', 'Switch')
    button.setValue('duplicator.pathSwitch(nuke.thisNode())')
    button.setTooltip('Switch current node paths (network to local and vice versa)')
        
    buttonAll = nuke.PyScript_Knob('buttonAll', 'Switch All')
    buttonAll.setValue('duplicator.pathSwitchAll()')
    buttonAll.setTooltip('Switch all read node paths (network to local and vice versa)')
    
    buttonReCopy = nuke.PyScript_Knob('buttonReCopy', 'ReCopy')
    buttonReCopy.setValue('duplicator.reCopy()')
    buttonReCopy.setTooltip('Force copy network files onto local drive')    
        
    n.addKnob(tab)
    n.addKnob(kn)
    n.addKnob(kl)
    n.addKnob(button)
    n['button'].setFlag(nuke.STARTLINE)
    n.addKnob(buttonAll) 
    n.addKnob(buttonReCopy)
    n['tile_color'].setValue(intColor([0.498, 1, 0.985]))     
        
    n['file'].setValue('[knob local]')
    n['file'].setEnabled(False)

# ===============================================================================================

def fileDuplicator(outDir, projectName, nodes, rel):
    nodesAmount = 0
    chaosCounter = 0
    for n in nodes:
        if ('SRC' or 'Src' or 'VIDEO' or 'Video' or 'IMAGES' or 'Images') in n['file'].value():
            nodesAmount += 1
        else:
            nodesAmount += 1
            chaosCounter += 1
    
    # print 'nodes amount', nodesAmount
    # print 'chaos counter', chaosCounter    
    
    if nodesAmount/(chaosCounter + 0.000001) <= 2:
        chaos = True
    else:
        chaos = False
    print chaos            

    progTask = nuke.ProgressTask("Collecting...")    

    chaos = True
    
    if chaos == True:
        for n in nodes:
            if 'knob' in n['file'].value():
                n['file'].setValue(n['netw'].value())
                knobsToDelete =['netw', 'local', 'button', 'buttonAll', 'buttonReCopy', 'duplicator']
                for k in knobsToDelete:
                    n.removeKnob(n.knobs()[k])
            # Get the file path value and split it
            fullPath = n.knob('file').getValue()
            # Split the path
            splitPath = fullPath.split('/')  # nuke UNIXfies paths LOL
            # Get the file folder location
            mediaPath = splitPath[-2]
            # Get the file name
            daMedia = splitPath[-1]
            # get the extension || format
            
            fExt = daMedia[daMedia.find('.', -5):]
            #fExt2 = daMedia.split('.')[-1]            

            # complete path without the file name
        
            #folderCreator(outDir, projectName)

            ### <11> Find if this is a sequence or a single file
            # If this is a sequence of images
            # IF not -1 then is a sequence else is a still OK
            relUnicPath = '/'.join(splitPath[splitPath.index(projectName)+1:-1]) # Second part without seqname of relative path 
            print 'relUnicPath is', relUnicPath
        
            if not daMedia.find('%') == -1:
                ### <12> Find padding
                print daMedia + " is a sequence"
                seqFolder = fullPath[0:fullPath.find(daMedia)]
                print "Sequence folder is", seqFolder    

                if '%' in daMedia:
                    print daMedia
                    if daMedia[daMedia.find('%')+1] != 'd':
                        padd = int ( daMedia[daMedia.find('%')+2:daMedia.find('%')+3] )
                    else:
                        padd = 1

                print "Padding is", padd                

                # Get start, end and sequence name
                startFrame = int( n.knob('first').getValue() )
                endFrame = int( n.knob('last').getValue() )
                # get sequence name alone and with a dot at the end
                seqName = daMedia[0:(daMedia.find('%')-1)]
                seqNameDot = daMedia[0:daMedia.find('%')]                

                ### <13> create sequence directory and jump inside it
                # Change to the Sources directory
                # if media located in different locations


                if chaos == True:
                    print "projectName is %s, mediaPath is %s" % (projectName, mediaPath)
                    if rel == True:
                        newSeqFolder = outDir + '/' + projectName + '/' + relUnicPath
                    else:
                        newSeqFolder = outDir + '/' + projectName + '/_DUPLICATOR/VIDEO/' + projectName + '/' + mediaPath
                    print newSeqFolder
                    if not os.path.exists(newSeqFolder):
                        print "lets create", newSeqFolder
#                        os.chdir(outDir + '/_DUPLICATOR/VIDEO')
#                        print "dir changed"
                    # OK create it
                        os.makedirs(newSeqFolder)
                        print  newSeqFolder, "created"

                    # Jump into it
                    os.chdir(newSeqFolder)                    

                    #Make a directory to hold the current sequence
                    # jump inside it
                    # But First check if the directory exists                    

                    ### <14> Wake up LOL :)
                    # loop and copy (finally) the frame range
                    copyFile = newSeqFolder + '/' + seqNameDot + str(n['first'].value()).zfill(padd) + fExt
                    # print "_________ COPY FILE" + str(copyFile) 
                    if os.path.exists(copyFile):
                        if nuke.ask('%s already exists. Replace?' % (newSeqFolder + '/' + seqNameDot + "#"*padd + fExt)): 
                            for f in range(startFrame, endFrame+1):    # don't omit last image
                                ## PROGRESS DIALOG >> if the collect task is cancelled
                                if progTask.isCancelled():
                                    nuke.message("Media files might not be complete")
                                    break;                        
        
                                # variable for progress percent
                                percent = int( (float(f) / float(endFrame)) * 100.0 )
                                # print "[ FRAME %s ]  [ end frame %s ]  [ percent %s ]" %(f, endFrame, percent)                        
        
                                # SET PROGRESS
                                progTask.setProgress(percent)                        
        
                                # compile var for copying
                                # current file on the current sequence
                                curFile = seqFolder + seqNameDot + str(f).zfill(padd)+fExt                        
        
                                # copy or new file
                                copyFile = seqNameDot + str(f).zfill(padd)+fExt
        
                                # Finally actually copy the files
                                print fExt
                                print newSeqFolder + '/' + copyFile
                                if os.path.exists(curFile):
                                    if os.path.exists(newSeqFolder):
                                        print 'copying to ' + str(newSeqFolder)
                                        shutil.copy(curFile, copyFile)                        
        
                                ## SHOW THE CURRENT SEQUENCE IN PROGRESS
                                progTask.setMessage("Copying: " + seqNameDot + str(f).zfill(padd)+fExt  )
                        else:
                            pass
                        localSeqPath = newSeqFolder + '/' + daMedia
                    else:
                            for f in range(startFrame, endFrame+1):    # don't omit last image
                                ## PROGRESS DIALOG >> if the collect task is cancelled
                                if progTask.isCancelled():
                                    nuke.message("Media files might not be complete")
                                    break;                        
        
                                # variable for progress percent
                                percent = int( (float(f) / float(endFrame)) * 100.0 )
                                # print "[ FRAME %s ]  [ end frame %s ]  [ percent %s ]" %(f, endFrame, percent)                        
        
                                # SET PROGRESS
                                progTask.setProgress(percent)                        
        
                                # compile var for copying
                                # current file on the current sequence
                                curFile = seqFolder + seqNameDot + str(f).zfill(padd)+fExt                        
        
                                # copy or new file
                                copyFile = seqNameDot + str(f).zfill(padd)+fExt
        
                                # Finally actually copy the files
                                print fExt
                                # print newSeqFolder + '/' + copyFile
                                if os.path.exists(curFile):
                                    print "HERE"
                                    localSeqPath = newSeqFolder + '/' + daMedia                                    
                                    if os.path.exists(newSeqFolder):
                                        
                                        print 'copying to ' + str(newSeqFolder)
                                        shutil.copy(curFile, copyFile)                        
        
                                ## SHOW THE CURRENT SEQUENCE IN PROGRESS
                                progTask.setMessage("Copying: " + seqNameDot + str(f).zfill(padd)+fExt  )                                                
                                        
                    kl = nuke.File_Knob('local', "local path")
                    kl.setValue(localSeqPath)                                               
            
            else:
                ######################################################################################
                #
                #                         NOT SEQUENCE
                #
                ######################################################################################

                if chaos == True:
                    # print "projectName is %s, mediaPath is %s" % (projectName, mediaPath)

                    videoExts = ['.mov', '.avi', 'mp4', '.mkv', '.wmv']
                    if fExt in videoExts:
                        print daMedia + " is a video file"
                        if rel == True:
                            newDestFolder = outDir + '/' + projectName + '/' + relUnicPath
                        else:
                            newDestFolder = outDir + '/' + projectName + '/_DUPLICATOR/VIDEO/' + projectName
                    else:
                        if rel == True:
                            newDestFolder = outDir + '/' + projectName + '/' + relUnicPath
                        else:
                            newDestFolder = outDir + '/' + projectName + '/_DUPLICATOR/IMAGES/' + projectName
                    print newDestFolder
                    if not os.path.exists(newDestFolder):
                        print "lets create", newDestFolder
#                        os.chdir(outDir + '/_DUPLICATOR/VIDEO')
#                        print "dir changed"
                    # OK create it
                        os.makedirs(newDestFolder)
                        print  newDestFolder, "created"

                    # Jump into it
                    os.chdir(newDestFolder)                    

                    #Make a directory to hold the current sequence
                    # jump inside it
                    # But First check if the directory exists                    

                    ### <14> Wake up LOL :)
                    # loop and copy (finally) the frame range

                    if progTask.isCancelled():
                        nuke.message("Media files might not be complete")
                        break                        
                      
                    # SET PROGRESS
                    progTask.setProgress(0)                        

                    # Finally actually copy the files
                    if not os.path.exists(newDestFolder + '/' + daMedia):
                        print 'copying to ' + str(newDestFolder)
                        shutil.copy(fullPath, daMedia)                        
                                          
                    kl = nuke.File_Knob('local', "local path")
                    kl.setValue(newDestFolder + '/' + daMedia)    

                
            if not progTask.isCancelled():              
                createDuplicatorKnobs(n, kl)
            else:
                knobsToDelete = ['netw', 'local', 'button', 'buttonAll', 'duplicator']
                for n in nodes:
                    if 'knob' in n['file'].value():
                        n['file'].setValue(n['netw'].value())
                        n['file'].setEnabled(True)
                        n['tile_color'].setValue(intColor([1, 1, 1])) 
                        for k in knobsToDelete:
                            n.removeKnob(n.knobs()[k])         

            
            if progTask.isCancelled():
                break 
            
    progTask.setProgress(100)
    del progTask    
    return True                


#    if chaos == True:
#        for r in range(0,len(chaos)):
#            kn = nuke.File_Knob('netw', "network path")
#            kn.setValue('')
#            r.addKnob(k)
#            r['file'].setValue('[knob netw]')
#            r['file'].setEnabled(False)
                
# ===============================================================================================   

def deleteDuplicatorStuff():
    if nuke.selectedNodes() == []:
        nodes = nuke.allNodes("Read")
        strNodes = "all"
    else:
        nodes = nuke.selectedNodes("Read")
        strNodes = "selected"
        
    if nuke.ask("Are you sure you want to delete all of Duplicator connections from %s read nodes?" % (strNodes)) == True:
        knobsToDelete =['netw', 'local', 'button', 'buttonAll', 'buttonReCopy' ,'duplicator']
        for n in nodes:
            if 'knob' in n['file'].value():
                n['file'].setValue(n['netw'].value())
                n['file'].setEnabled(True)
                n['tile_color'].setValue(intColor([1, 1, 1])) 
                for k in knobsToDelete:
                    n.removeKnob(n.knobs()[k])        
 
# ===============================================================================================  

def filePathDisable():
    print "we're in"
    if 'knob' in nuke.thisNode()['file'].value():
        nuke.thisNode()['file'].setEnabled(False)
 
# ===============================================================================================

def mainFuncDuplicator(proxyEnable = True):
    # if userd from Shot Setup Menu, 
    # we don't need proxy checkbox in duplicator panel
    if proxyEnable == True:
        panelResults = panelDuplicator()
    else:
        panelResults = panelDuplicator(False)
        
    print panelResults
    if panelResults != None:

        if fileDuplicator(panelResults[0], panelResults[1], panelResults[2], panelResults[4]) != None:    # outDir, projectName, nodes, renderProxy, rel
            if panelResults[3] == True:
                createProxy(panelResults[2])
            print "Success!"
            # nuke.message("Successfully duplicated!")
    else:
        pass
            
        
