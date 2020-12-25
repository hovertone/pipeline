import hou

def createNodeBasedOnSelection(nodeType = 'xform'):
    print 'in %s create' % nodeType

    nodes = hou.selectedNodes()
    pwd = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor, 0)
    vb = hou.ui.findPaneTab(pwd.name()).visibleBounds()

    netw_context = hou.node(pwd.pwd().path())
    if len(nodes) == 0:
        xf = netw_context.createNode(nodeType)
        xf.setPosition(vb.center())
    elif len(nodes) == 1:
        xf = netw_context.createNode(nodeType)
        n = nodes[0]
        xf.setInput(0, n)
        xf.moveToGoodPosition()

        n.setSelected(False)
        xf.setSelected(True)

        xf.setRenderFlag(True)
        xf.setDisplayFlag(True)
    elif len(nodes) > 1:
        for n in nodes:
            xf = netw_context.createNode(nodeType)
            xf.setInput(0, n)
            xf.moveToGoodPosition()

            n.setSelected(False)
            xf.setSelected(True)

def createNull(rename = None):
    nodes = hou.selectedNodes()
    pwd = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor, 0)
    vb = hou.ui.findPaneTab(pwd.name()).visibleBounds()

    netw_context = hou.node(pwd.pwd().path())
    type_color = hou.Color((0.07, 0.07, 0.07))

    #if netw_context.type().name() == 'geo':
    if len(nodes) == 0:
        null = netw_context.createNode('null')
        null.setPosition(vb.center())

        null.setColor(type_color)
        if rename:
            null.setName(rename, unique_name=True)
    elif len(nodes) == 1:
        null = netw_context.createNode('null')
        n = nodes[0]
        null.setInput(0, n)
        null.moveToGoodPosition()

        n.setSelected(False)
        null.setSelected(True)

        null.setRenderFlag(True)
        null.setDisplayFlag(True)

        null.setColor(type_color)
        if rename:
            null.setName(rename, unique_name=True)
    elif len(nodes) > 1:
        for n in nodes:
            null = netw_context.createNode('null')
            null.setInput(0, n)
            null.moveToGoodPosition()

            n.setSelected(False)
            null.setSelected(True)

            null.setColor(type_color)
            if rename:
                null.setName(rename, unique_name=True)


def clipMirror():
    nodes = hou.selectedNodes()
    pwd = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor, 0)
    vb = hou.ui.findPaneTab(pwd.name()).visibleBounds()

    pn = hou.node(pwd.pwd().path())

    clip = pn.createNode('clip')
    if len(nodes) == 1:
        clip.setInput(0, nodes[0])
        clip.moveToGoodPosition()
    else:
        clip.setPosition(vb.center())

    clip.parm('dirx').set(-1)
    clip.parm('diry').set(0)
    clip.setSelected(True, clear_all_selected=True)

    mir = pn.createNode('mirror')
    mir.setInput(0, clip)
    mir.moveToGoodPosition()
    mir.setSelected(True)

    mir.parm('dist').setExpression("ch('../%s/dist')" % clip.name())
    for s in ['x', 'y', 'z']:
        mir.parm('origin%s' % s).setExpression("ch('../%s/origin%s')" % (clip.name(), s))
        mir.parm('dir%s' % s).setExpression("ch('../%s/dir%s')" % (clip.name(), s))

    if len(nodes) > 0:
        mir.setDisplayFlag(True)
        mir.setRenderFlag(True)

def toggleSmoothing():
    pwd = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor, 0)
    pn = hou.node(pwd.pwd().path())

    if pn.type().name() == 'geo':
        val = pn.parm('viewportlod').eval()
        if val == 0:
            pn.parm('viewportlod').set(5)
        else:
            pn.parm('viewportlod').set(0)

prevDisplay = None
def displayResult():
    p = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor, 0)
    pwd = hou.node(p.pwd().path())
    out = pwd.node("EXIT")

    global prevDisplay
    print 'GLOBAL VAR IS %s' % prevDisplay
    if prevDisplay:
        prevDisplay.setDisplayFlag(True)
        prevDisplay = None
    else:
        for n in pwd.children():
            if n.isDisplayFlagSet():
                prevDisplay = n
                break
        out.setDisplayFlag(True)
        print 'now its %s' % prevDisplay
