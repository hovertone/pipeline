import nuke

def getRange():
    inpt = nuke.getInput('Set enabled frames')
    if not inpt: return

    if '-' not in inpt:
        nuke.message('You need to enter frame range(s). Something like "3-44 66-77"')
        return getRange()

    pairs = []
    if ' ' in inpt:
        # if multiple frame ranges
        for p in inpt.split(' '):
            pair = (int(p.split('-')[0]), int(p.split('-')[1]))
            if pair[0] > pair[1]:
                nuke.message('First frame should be smaller (earlier) than second.')
                return getRange()
            pairs.append(pair)
    else:
        # if one single frame range
        pair = (int(inpt.split('-')[0]), int(inpt.split('-')[1]))
        if pair[0] > pair[1]:
            nuke.message('First frame should be smaller (earlier) than second.')
            return getRange()
        pairs.append(pair)

    return pairs

def setMix():
    nodes = nuke.selectedNodes()
    if len(nodes) < 1:
        nuke.message('Select node(s).')
        return

    ranges = getRange()
    noMixNodeNames = []
    for n in nodes:
        if 'mix' in n.knobs().keys():
            for r in ranges:
                start, end = r[0], r[1]
                k = n['mix']
                k.setAnimated(0)
                an = k.animations()[0]
                an.setKey(start-1, 0)
                an.setKey(start, 1)
                an.setKey(end, 1)
                an.setKey(end+1, 0)

                n['label'].setValue('%s-%s' % (start, end))

        else:
            noMixNodeNames.append(n['name'].value())
    
    if noMixNodeNames != []:
        nodesToMessage = ', '.join(noMixNodeNames)
        print "No mix knob in %s" % nodesToMessage