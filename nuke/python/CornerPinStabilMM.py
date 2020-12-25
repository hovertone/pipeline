import nuke
from scripts import selectOnly

def trackerToCP(n = ''):
    if n == '':
        n = nuke.selectedNodes()[0]

    if n.Class() != 'Tracker3':
        nuke.message('Only TRACKER3 (the old one with 4 knobs only) will do the job.')
        return

    selectOnly(n)
    xpos = n.xpos()
    ypos = n.ypos()
    cp = nuke.createNode('CornerPin2D')
    cp.setXYpos(xpos, ypos)
    messagedOnce = False
    for i in range(1,5):
        if n['track' + str(i)].isAnimated():
            cp['to' + str(i)].fromScript(n['track' + str(i)].toScript())
        else:
            while messagedOnce == False:
                nuke.message('One of 4 knobs is not animated. CornerPin will work in unappropriate way.')
                messagedOnce = True

    nuke.delete(n)
    return cp


def createKnobs():
    if len(nuke.selectedNodes()) == 0:
        nuke.message("You need to select a node.")
        return

    nodes = nuke.selectedNodes()
    nodes = [n for n in nodes if n.Class() == 'CornerPin2D']

    for n in nodes:
        if n.Class() == 'Tracker3':
            n = trackerToCP(n)
        elif n.Class() == 'CornerPin2D':
            pass
        else:
            nuke.message("Select a CornerPin node.")
            return

        tab = nuke.Tab_Knob('CPStabilMM_Tab', '-.-')
        refFrame = nuke.Int_Knob('refFrame', 'Reference frame')
        refFrame.setValue(nuke.frame())
        setThisFrame = nuke.PyScript_Knob('setThisFrame', 'This Frame')
        setThisFrame.setValue('''node = nuke.thisNode()
node['refFrame'].setValue(nuke.frame())''')

        stabilButton = nuke.PyScript_Knob('stabil', 'Stabilize')
        stabilButton.setValue('CornerPinStabilMM.stabil()') #CornerPinStabilMM.stabil()
        mmButton = nuke.PyScript_Knob('mm', 'Match-Move')
        mmButton.setValue('CornerPinStabilMM.mm()') #CornerPinStabilMM.mm()
        pos1 = nuke.XY_Knob('pos1', 'pos 1')
        pos2 = nuke.XY_Knob('pos2', 'pos 2')
        pos3 = nuke.XY_Knob('pos3', 'pos 3')
        pos4 = nuke.XY_Knob('pos4', 'pos 4')

        n.addKnob(tab)
        n.addKnob(refFrame)
        n.addKnob(setThisFrame)
        n.addKnob(stabilButton)
        n['stabil'].setFlag(nuke.STARTLINE)
        n.addKnob(mmButton)
        n.addKnob(pos1)
        n['pos1'].setEnabled(False)
        n.addKnob(pos2)
        n['pos2'].setEnabled(False)
        n.addKnob(pos3)
        n['pos3'].setEnabled(False)
        n.addKnob(pos4)
        n['pos4'].setEnabled(False)

        for number in range(4):
            curves = []
            for xy in range(2):
                curve = n['to'+str(number+1)].animation(xy)
                curves += [curve]
            n['pos'+str(number+1)].copyAnimations(curves)

        n['mm'].execute()

def stabil():
    n = nuke.thisNode()
    if ('CPStabilMM_Tab' not in n.knobs().keys()) or (n.Class() != 'CornerPin2D'):
        return False


    for number in range(4):
        n['to'+str(number+1)].setExpression('pos' + str(number + 1) + '(refFrame)')
        curves = []
        for xy in range(2):
            curve = n['pos'+str(number+1)].animation(xy)
            curves += [curve]
        n['from'+str(number+1)].copyAnimations(curves)

    n['label'].setValue('stabilize [knob refFrame]')

def mm():
    n = nuke.thisNode()
    if ('CPStabilMM_Tab' not in n.knobs().keys()) or (n.Class() != 'CornerPin2D'):
        return False


    for number in range(4):
        n['from'+str(number+1)].setExpression('pos' + str(number + 1) + '(refFrame)')
        curves = []
        for xy in range(2):
            curve = n['pos'+str(number+1)].animation(xy)
            curves += [curve]
        n['to'+str(number+1)].copyAnimations(curves)

    n['label'].setValue('match-move [knob refFrame]')
