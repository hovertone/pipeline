import nuke
import nuke.rotopaint as rp

def getElements(layer):
    elements = []
    for element in layer:
        #print 'EL ' + element.name
        if isinstance(element, nuke.rotopaint.Layer):
            elements.append(element)
            getElements(element)
        elif isinstance(element, nuke.rotopaint.Stroke) or isinstance(element, nuke.rotopaint.Shape):
            elements.append(element)

    return elements

def main():
    print 'IN MASK SCALER'
    nodes = nuke.selectedNodes()
    if nodes == []:
        nuke.message('Select some nodes.')
        return

    if 'SCALER' in [i.name() for i in nuke.allNodes('NoOp')]:
        # USE EXISTING
        ctrl = nuke.toNode('SCALER')
    else:
        # CREATE NEW
        ctrl = nuke.createNode('NoOp', 'name SCALER')
        ctrl.setXYpos(nodes[0].xpos() - 110, nodes[0].ypos() + 200)
        ctrl.setInput(0, None)
        ctrl['tile_color'].setValue(2868860415)

        tabK = nuke.Tab_Knob('options', 'OPTIONS')
        ctrl.addKnob(tabK)

        coefK = nuke.Double_Knob('coef', 'coef')
        coefK.setRange(0, 3)
        coefK.setValue(1)
        ctrl.addKnob(coefK)

        fromK = nuke.Enumeration_Knob('from', 'FROM', ['720x405', '1280x720', '1920x1080', '2880x1620', '3200x1800'])
        ctrl.addKnob(fromK)

        toK = nuke.Enumeration_Knob('to', 'TO', ['720x405', '1280x720', '1920x1080', '2880x1620', '3200x1800'])
        toK.clearFlag(nuke.STARTLINE)
        ctrl.addKnob(toK)

        calcK = nuke.PyScript_Knob('calculate', 'CALCULATE', "f = float(nuke.thisNode()['from'].value().split('x')[0])\nt = float(nuke.thisNode()['to'].value().split('x')[0])\nnuke.thisNode()['coef'].setValue(t/f)")
        calcK.clearFlag(nuke.STARTLINE)
        ctrl.addKnob(calcK)


    for n in nodes:
        if n.Class() == 'Roto' or n.Class() == 'RotoPaint':
            print 'NODE NAME IS %s    ::    TYPE ROTO' % n.name()

            nodec = n['curves']
            root = nodec.rootLayer

            elms = getElements(root)
            #print 'ELEMS %s' % str(elms)
            scalar_exists = False
            for e in elms:
                if isinstance(e, nuke.rotopaint.Layer) and e.name == 'SCALER':
                    print '\tSCALAR FOLDER FOUND. SKIPPING THIS NODE'
                    scalar_exists = True

            if scalar_exists:
                break

            scalerFolder = rp.Layer(nodec)  # the assumption here was that this works similar to how the Stroke method creates a new paintstroke
            scalerFolder.name = 'SCALER'
            root.append(scalerFolder)
            #help(newLayer)

            # CLONE ITEMS
            names = []
            for e in elms:
                attr = e.getAttributes()

                if isinstance(e, nuke.rotopaint.Shape):
                    #print 'copying %s' % e.name
                    names.append(e.name)
                    scalerFolder.append(e.clone())

                    #fo = attr.getValue(1, 'fx')
                    # print attr.getValue(1, 'fx')
                    # print attr.getValue(1, 'fy')
                    attr.set(1, 'fx', 3.0)
                    attr.set(1, 'fy', 3.0)

                elif isinstance(e, nuke.rotopaint.Stroke):
                    names.append(e.name)
                    scalerFolder.append(e.clone())

                    bs = attr.getValue(1, attr.kBrushSizeAttribute)
                    attr.set(attr.kBrushSizeAttribute, bs * 2.5)

            # REMOVE UNNEEDED
            root_elms = list(root)
            for i, re in reversed(list(enumerate(root_elms))):
                #print 'checking %s' % re.name
                if re.name in names:
                    #print 'have to delete it'
                    root.remove(i)

            scalerFolder.getTransform().getScaleAnimCurve(0).useExpression = True
            scalerFolder.getTransform().getScaleAnimCurve(1).useExpression = True
            scalerFolder.getTransform().getScaleAnimCurve(0).expressionString = 'SCALER.coef'
            scalerFolder.getTransform().getScaleAnimCurve(1).expressionString = 'SCALER.coef'


            nodec.changed()
            #help(scalerFolder.getTransform().getScaleAnimCurve(1))
