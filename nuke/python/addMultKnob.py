from CUF import isNumber
import nuke

def checkKnobsExistence(n):
    biggestNumber = 0
    keys = n.knobs().keys()
    for key in keys:
        if 'mult' in n.knobs()[key].name():
            for c in n.knobs()[key].name():
                if isNumber(c): 
                    if c > biggestNumber:
                        biggestNumber = c

    return int(biggestNumber) + 1

def addKnobs(node, knob):
    knobVer = checkKnobsExistence(node)
    sep = nuke.Text_Knob('', knob.label())
    multK = nuke.Double_Knob(str('mult' + str(knobVer)), 'mult%s' % knobVer)
    range = nuke.getInput('Set range for MULT knob:', '0-1')
    if not range: return
    try:
        lower, upper = range.split('-')
        lower = float(lower)
        upper = float(upper)
    except:
        return 

    multK.setRange(lower, upper)
    multK.setValue(lower + upper / 2)

    node.addKnob(multK)

    return multK

def addMultExpression(node, knob):
    multKnob = addKnobs(node, knob) # mult knob
    if knob.hasExpression():
        knob.setExpression(knob.toScript()[1:-1] + '*%s' % multKnob.name())
    else:
        knob.setExpression('%s' % multKnob.name())

if nuke.env['gui']:
    ng = nuke.menu('Animation')
    ng.addCommand('Add mult expression (and knob)', 'addMultKnob.addMultExpression(nuke.thisNode(), nuke.thisKnob())', icon = 'SoftClip.png')