import nuke
from scripts import selectOnly

def inputsPanel():
    p = nuke.Panel("Deep defocus slicer", 250)
    p.addSingleLineInput('Number of slices:', '3')
    p.addSingleLineInput('Far:', '')
    p.addButton("Cancel")
    p.addButton("OK")

    result = p.show()
    if result:
        return int(p.value('Number of slices:')), p.value('Far:')

def deepDefocus():
    inputs = inputsPanel()
    if not inputs:
        return
    else:
        slices, maxDepth = inputs
        maxDepth = float(maxDepth)

    n = nuke.selectedNode()

    ctrl = nuke.createNode('NoOp', 'name Defocus_controls')
    ctrl.setXYpos(n.xpos() - 110, n.ypos() + 200)
    ctrl.setInput(0, None)

    defK = nuke.Double_Knob('def', 'Defocus')
    defK.setRange(0, (slices-1) * 10)
    multK = nuke.Double_Knob('mult', 'Defocus Amount')
    multK.setRange(0, 10)

    ctrl.addKnob(defK)
    ctrl.addKnob(multK)

    defs = []
    step = maxDepth / slices
    for i in range(slices):
        dc = nuke.createNode('DeepCrop', 'use_bbox False ')
        dc.setInput(0, n)
        dc.setXYpos(n.xpos() + 110 *i, n.ypos() + 110)
        
        dti = nuke.createNode('DeepToImage')
        dti.setInput(0, dc)

        if i == 0:
            dc['use_znear'].setValue(False)
            dc['use_zfar'].setValue(True)
            dc['zfar'].setValue(step)
            print 'first, %s' % step
        elif i == slices:
            dc['use_znear'].setValue(True)
            dc['use_zfar'].setValue(False)
            dc['znear'].setValue(step * (slices -1))
            print 'last, %s' % step * (slices -1)
        else:
            dc['use_znear'].setValue(True)
            dc['use_zfar'].setValue(True)
            dc['znear'].setValue(step * i)
            dc['zfar'].setValue(step * (i + 1))
            print 'mid, %s, %s' % (step * i , step * (i + 1))

        df = nuke.createNode('Defocus', 'channels rgba')
        df['label'].setValue(str(i * 10))
        df['defocus'].setExpression('abs(%s.def - label) * %s.mult' % (ctrl.name(), ctrl.name()))
        df.setInput(0, dti)
        df.setXYpos(dti.xpos(), dti.ypos() + 70)

        defs.append(df)

    m = nuke.createNode('Merge2')
    m.setXYpos(defs[0].xpos(), defs[0].ypos() + 70)
    inputs = range(slices + 1)
    inputs.pop(2)
    for i, v in enumerate(inputs):
        m.setInput(v, defs[i])







