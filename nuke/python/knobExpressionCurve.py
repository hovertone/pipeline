from scripts import isNumber
import nuke

def checkKnobsExistence(n):
    biggestNumber = -1
    keys = n.knobs().keys()
    for key in keys:
        if 'freq' in n.knobs()[key].name():
            for c in n.knobs()[key].name():
                if isNumber(c): 
                    if c > biggestNumber:
                        biggestNumber = c

    return int(biggestNumber) + 1

def addKnobs(node, knob):
    knobVer = checkKnobsExistence(node)
    sep = nuke.Text_Knob('', knob.label())
    freq = nuke.Double_Knob(str('freq' + str(knobVer)), 'Frequency')
    freq.setValue(0.13)
    freq.setRange(0, 1)

    seed = nuke.Double_Knob(str('seed' + str(knobVer)), 'Seed')
    seed.setValue(36)
    seed.setRange(0, 100)

    amp = nuke.Double_Knob(str('amp' + str(knobVer)), 'Amplitude')
    amp.setValue(0.19)
    amp.setRange(0, 1)

    to = nuke.Double_Knob(str('to' + str(knobVer)), 'Time Offset')
    to.setValue(34.98)
    to.setRange(0, 100)

    amount = nuke.Double_Knob(str('amount' + str(knobVer)), 'Amount')
    amount.setValue(0.555)
    amount.setRange(0, 1)

    node.addKnob(sep)
    node.addKnob(freq)
    node.addKnob(seed)
    node.addKnob(amp)
    node.addKnob(to)
    node.addKnob(amount)

    return freq.name(), seed.name(), amp.name(), to.name(), amount.name()

def addCurveExpression(node, knob):
    knobs = addKnobs(node, knob) # freq, seed, amp, to, amount
    knob.setExpression('(1*(noise((frame+(%s*100))*%s, (%s*5), 0)*2-1)*%s+(%s*.7))+%s' % (knobs[3], knobs[0], knobs[1], knobs[2], knobs[2], knobs[4]))

if nuke.env['gui']:
    ng = nuke.menu('Animation')
    ng.addCommand('Add Expression Random Curve', 'knobExpressionCurve.addCurveExpression(nuke.thisNode(), nuke.thisKnob())', icon = 'SoftClip.png')
