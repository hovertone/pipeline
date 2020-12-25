import nuke
from CUF import selectOnly, nodeToList, createAndMoveNode

def channelSplit(rnode):
    '''
    Splits all of the layers from exr file. Except 'rgba'

    Arguments (rnode)
        rnode - node to split from
    '''    
    channels = rnode.channels()
    # creates a list of uniaque channels
    layers = list( set([c.split('.')[0] for c in channels]) )
    layers.sort()
    del layers[layers.index('rgba')]
    dot = nuke.createNode('Dot')
    dot.setYpos(rnode.ypos()+ 200)
    
    for i in range(0, len(layers)):
        s = nuke.createNode('Shuffle', inpanel = False)
        s['out'].setValue('rgb')
        
        s.setInput(0, dot)
        s.setXYpos(rnode.xpos() + i * 110, dot.ypos() + 75)
        s['in'].setValue(layers[i])

# ==========================================================================================================================================
# Arnold Composite
# ==========================================================================================================================================

def getChannels(inpNode, exceptChannels = []):
    '''
    Returns channels from provided nodes. exceptChannels can subtract layers from existant

    Arguments (inpNode, exceptChannels)
        inpNode - node to extract layer names from
        exceptChannels - channels to igrone
    '''      
    channels = inpNode.channels()
    # creates a list of uniaque channels
    layers = list( set([c.split('.')[0] for c in channels]) )
    layers.sort()

    # remove unwanted layers
    # if exceptChannels != []:
    #     for c in exceptChannels:
    #         try:
    #             del layers[layers.index(c)]
    #         except:
    #             print('WARNING. There is no %s channel in this pipe.' % index(c))

    priority = ['direct_diffuse', 'indirect_diffuse', '']


    return layers

def branchAndCompositeChannel(channel, inpDot, lastNode):
    '''
    Creates a shuffle branch of provided layer

    Arguments (channel, inpDot, lastNode)
        channel - channel to shuffle out
        inpDot - from this node branch will begin
        lastNode - this node will be merged with newly created
    '''  
    # if it's a first branch then don't merge it, just shuffle
    if lastNode == inpDot:
        s = createAndMoveNode('Shuffle', selNode = inpDot, y = 40)
        s['in'].setValue(channel)
        s['label'].setValue('[knob in]')
        s['in2'].setValue('alpha')
        s['alpha'].setValue(7)
        return inpDot, s
    else:
        upperDot = createAndMoveNode('Dot', selNode = -1, offsetNode = inpDot, x = 180)
        upperDot.setInput(0, inpDot)
        s = createAndMoveNode('Shuffle', selNode = upperDot, y = 40)
        s['in'].setValue(channel)
        s['label'].setValue('[knob in]')

        # The second branch will have a slightly different y offset
        if lastNode.Class() == 'Shuffle':
            yoffset = 135
        else:
            yoffset = 70

        bottomDot = createAndMoveNode('Dot')
        bottomDot.setXYpos(s.xpos() + 34, lastNode.ypos() + yoffset + 3)
        merge = createAndMoveNode('Merge2', selNode = [lastNode, bottomDot], offsetNode = lastNode, y = yoffset)
        merge['name'].setValue(channel)
        merge['operation'].setValue('plus')
        merge['Achannels'].enableChannel(3, False)


        return upperDot, merge # returns new dot to branch from again and a merge to merge next branch on top

def arnoldComposite(rnode = ''):
    '''
    Creates a tree to composite Arnold (c) renders

    Arguments (rnode)
        rnode - node to begin tree from
    '''  
    if rnode == '':
        try:
            rnode = nuke.selectedNode()
        except:
            nuke.message('Select read node for god sake...')
            return

    lastNode = createAndMoveNode('Unpremult', y = 40)
    lastNode['channels'].setValue('all')

    lastNode = createAndMoveNode('Dot', y = 40)
    channelsToComposite = getChannels(nuke.selectedNode(), exceptChannels = ['N', 'P', 'depth', 'rgba'])
    return
    inpDot = lastNode
    # Loops through all of the channels and creates a branch for each one independently
    for channel in channelsToComposite:
        results = branchAndCompositeChannel(channel, inpDot, lastNode)
        # Reassigning a dot to negin branch from and a merge (shuffle) node to merge next branch on top
        inpDot, lastNode = results[0], results[1]

    createAndMoveNode('Premult', selNode = lastNode, y = 40)
