import nuke
from attribManager import addStringAttr, addTab

def connectViewer():
    #print 'in connect viewer'
    d = dict()
    for n in nuke.allNodes():
        if 'viewerBinds' in n.knobs().keys() and 'input' in n.knobs().keys() and n['input'].value() != '':
            d[n.name()] = n['input'].value()

    #print d

    for v in nuke.allNodes('Viewer'):
        for i in d.keys():
            v.setInput(int(d[i])-1, nuke.toNode(i))

def addInputAttr(node, val):
    for n in nuke.allNodes():
        if 'viewerBinds' in n.knobs().keys() and 'input' in n.knobs().keys() and n['input'].value() == str(val):
            n['input'].setValue('')

    addTab(node, 'viewerBinds')
    addStringAttr(node, 'input', str(val))

