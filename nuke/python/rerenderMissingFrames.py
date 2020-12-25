import re, nuke, os

def rerenderMissedFrame(exceptionalFrames = []):
    node = nuke.selectedNodes('Write')
    if not node: 
        nuke.message('Select a Write node')
        return

    node = node[0]
    path = node['file'].value()

    # replace %04d pattern with "#"s
    if '%' in path:
        ind = path.find('%')
        paddingAmount = int(path[ind+2])
        path = path[:ind] + '#'*paddingAmount + path[ind+4:]
    else:
        search = re.search(r'\#+', path)
        paddingAmount = len(search.group())        
    
    # make a list of files in Path directory
    w = os.listdir(os.path.split(path)[0])
    w.sort()

    # Filter w list to ww list to fits current sequence
    ww = []
    lookForPattern = os.path.splitext(os.path.split(path)[1])[0][:os.path.splitext(os.path.split(path)[1])[0].find('#')-1]
    lookForPatternExt = os.path.splitext(os.path.split(path)[1])[1]
    for f in w:
        if (lookForPattern in f) and (lookForPatternExt in f):
            ww.append(f)

    #Find first and last number of padding
    ww.sort()
    sFirst = re.search(r'[\., \_]\d+\.', ww[0])
    sLast = re.search(r'[\., \_]\d+\.', ww[-1])
    
    firstFrame, lastFrame = int(sFirst.group()[1:-1]), int(sLast.group()[1:-1])
    
    missingFrames = []
    for i in range(firstFrame, lastFrame+1):
        currentFilePath = path.replace('#'*paddingAmount, str(i).zfill(paddingAmount))
        if not os.path.exists(currentFilePath): 
            #print "File %s doesn't exists" % currentFilePath
            if i not in exceptionalFrames:
                missingFrames.append(i)

    frSet = nuke.FrameRanges(missingFrames)

    if nuke.ask('Are you sure you want to render %s frames?' % len(missingFrames)):
        nuke.render(node.name(), frSet)

#rerenderMissedFrame()

#nuke.menu('Nodes').addCommand('Little Helpers/Rerender Missing Frames', 'rerenderMissedFrame()') 



#from hiero.uis222 import findMenuAction

#pr = findMenuAction('Preferences...')
#pr.setShortcut('')
#nuke.menu('Nodes').addCommand('adaittle Helpers/Unused/Go to previous keyframe', 'nuke.activeViewer().frameControl(-4)', 'shift+s')
