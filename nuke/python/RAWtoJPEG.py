import os
from nuke import addFormat, getFilename, createNode, selectedNodes
from CUF import fixPath
from LH import autoplace, selectOnly


def avgValue(*args):
    items = []
    if len(args) == 1:
        for i in args[0]:
            items.append(i)
    else:
        for i in args:
            items.append(i)
    
    summ = 0.0
    for i in items:
        summ += i
    return summ/len(items)
    
def createReads(path):
    path = fixPath(path)
    if path[-1] != '/':
        path += '/'
        
    filesList = os.listdir(path)
    readNodes = []
    for i in filesList:
        r = createNode('Read')
        r['file'].setValue(path + i)
        readNodes.append(r)
        
        if i == '_DSC5550.NEF':
            return readNodes
    
    return readNodes

def createLensReformats(readNodes):
    reformatsList = []
    for r in readNodes:
        selectOnly(r)
        ld = createNode('LensDistortion')
        ld['distortion1'].setValue(-0.03455073)
        ld['distortion2'].setValue(0.00180492)
        
        selectOnly(ld)
        reformat = createNode('Reformat')
        reformat['format'].setValue('DvaIvana')
        reformat['resize'].setValue('none')
        reformatsList.append(reformat)
        
    return reformatsList

def createWrites(reformatsList, readNodes):
    writesList = []
    for i in range(0,len(reformatsList)):
        selectOnly(reformatsList[i])
        w = createNode('Write')
        w['file'].setValue(os.path.splitext(readNodes[i]['file'].value())[0] + '.jpg') # 
        w['_jpeg_quality'].setValue(1)
        w.setXYpos(r.xpos(), r.ypos()+ 140)
        writesList.append(w)
        
    return writesList

# =============================================================================================


def createNodes(path, reads = []):    
    writesList = []
    if reads == []:
        path = fixPath(path)
        if path[-1] != '/':
            path += '/'
            
        filesList = os.listdir(path)
        first = True
        
        for i in range(0,len(filesList)):
            if first == True:
                r = createNode('Read')
                r['file'].setValue(path + filesList[i])
                lastRead = r
                first = False            
            else:
                r = createNode('Read')
                r['file'].setValue(path + filesList[i])
                r.setXYpos(lastRead.xpos() + 110, lastRead.ypos())
                lastRead = r
        
            ld = createNode('LensDistortion')
            if lastRead.format().width() > lastRead.format().height():
                ld['distortion1'].setValue(-0.03455073)
                ld['distortion2'].setValue(0.00180492)
            else:
                ld['distortion1'].setValue(-0.04316897)
                ld['distortion2'].setValue(0.00626172)
            ld['invertDistortion'].setValue(1)
                
            
            selectOnly(ld)
            reformat = createNode('Reformat')
            if lastRead.format().width() > lastRead.format().height():
                reformat['format'].setValue('DvaIvana')
            else:
                reformat['format'].setValue('DvaIvanaVert')
            reformat['resize'].setValue('none')
            
            selectOnly(reformat)
            w = createNode('Write')
            w['file'].setValue(os.path.splitext(r['file'].value())[0] + '.jpg') # 
            w['_jpeg_quality'].setValue(1)
            w.setXYpos(r.xpos(), r.ypos()+ 200)
            writesList.append(w)
                
            #if i == 50:
                #return
                
    else:
        for i in range(0, len(reads)):
            r, lastRead = reads[i], reads[i]
            selectOnly(r)
            
            ld = createNode('LensDistortion')
            if lastRead.format().width() > lastRead.format().height():
                ld['distortion1'].setValue(-0.03455073)
                ld['distortion2'].setValue(0.00180492)
            else:
                ld['distortion1'].setValue(-0.04316897)
                ld['distortion2'].setValue(0.00626172)
            ld['invertDistortion'].setValue(1)
                
            
            selectOnly(ld)
            reformat = createNode('Reformat')
            if lastRead.format().width() > lastRead.format().height():
                reformat['format'].setValue('DvaIvana')
            else:
                reformat['format'].setValue('DvaIvanaVert')
            reformat['resize'].setValue('none')
            
            selectOnly(reformat)
            w = createNode('Write')
            w['file'].setValue(os.path.splitext(r['file'].value())[0] + '.jpg') # 
            w['_jpeg_quality'].setValue(1)
            w.setXYpos(r.xpos(), r.ypos()+ 200)
            writesList.append(w)
            
        
    
def main():
    addFormat('3112 2063 DvaIvana')
    addFormat('2066 3118 DvaIvanaVert')
    
    if len(selectedNodes()) == 0:
        path = getFilename('Select folder or images')
        if path[-1] != '/' or path[-1] != '\/':
            path = os.path.split(path)[0] + '/'
            
        createNodes(path)
    else:
        print 'Here'
        reads = selectedNodes()
        
        createNodes('', reads)
        
    
    
    #readNodes = createReads(path)
    #selectOnly(readNodes)
    #autoplace()
    #
    #nuke.addFormat('3112 2063 DvaIvana')
    #reformatsList = createLensReformats(readNodes)
    #
    #readNodes = nuke.selectedNodes('Read')
    #writesList = createWrites(reformatsList, readNodes)
    

