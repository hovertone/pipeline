import nuke

def main():
    #cleanUp()  # develop purposes
    nuke.tprint('++++++++++')
    node = nuke.selectedNode()
    if node.Class() != 'Read':
        nuke.message('Select Read node with proper metadata')
        return

    if 'exr/wtm' in node.metadata().keys() and 'exr/focal' in node.metadata().keys() and 'exr/haperture' in node.metadata().keys():
        customMD = True
    else:
        nuke.message('No metadata was found')
        return
        customMD = False

    firstFrame = node.firstFrame()
    lastFrame = node.lastFrame()
    aspect = float(node.format().width())/node.format().height()

    c = nuke.createNode('Camera2')   
    c.setXYpos(node.xpos() - 110, node.ypos())
    c['tile_color'].setValue(151672575)

    if customMD:
        c['useMatrix'].setValue(True)
        for s in ['focal', 'matrix', 'haperture', 'vaperture']:
            c[s].setAnimated()
    else:
        c['useMatrix'].setValue(True)
        for s in ['matrix']:
            c[s].setAnimated()
    

    for f in range(firstFrame, lastFrame+1):
        #print 'frame %s' % f
        
        #tr = node.metadata('exr/translate', f).split(',')
        #rt = node.metadata('exr/rotate', f).split(',')


        #MATRIX STUFF
        if customMD:
            c['label'].setValue('from matrix')
            focal = float(node.metadata('exr/focal', f))
            c['focal'].setValueAt(focal, f)
            haperture = float(node.metadata('exr/haperture', f))
            c['haperture'].setValueAt(haperture, f)
            c['vaperture'].setValueAt(float(haperture/aspect), f)

            wtm = node.metadata('exr/wtm', f).replace('(', '').replace(')', '')
            array = [float(i) for i in wtm.split(',')]
            arrayInArray = list()
            for i in range(4):
                l = []
                for j in range(4):
                    l.append(array[j + 4*i])
                arrayInArray.append(l)

            newArray = zip(*arrayInArray)

            for i, e in enumerate(newArray):
                for ii, ee in enumerate(e):
                    c['matrix'].setValue(ee, ii + i*4, f)
        else:
            #NO CUSTOM MD
            c['label'].setValue('from arnold default')
            if 'exr/worldToCamera' not in node.metadata().keys():
                nuke.message('No camera positions (even arnolds default) has been found in metadata.')
                return
            else:
                nuke.tprint('in proper place')
                newArray = node.metadata('exr/worldToCamera', f)

                for i, e in enumerate(newArray):
                    c['matrix'].setValue(e, i, f)

        

def cleanUp():
    for c in nuke.allNodes('Camera2'):
        if 'TRS' in c['label'].value() or 'WTM' in c['label'].value():
            print ('deleteing %s' % c.name())
            nuke.delete(c)