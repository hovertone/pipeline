import nuke
try:
    from CUF import selectOnly
except:
    from scripts import selectOnly

def positionNodeCreate():
    node = nuke.selectedNode()
    if not node:
    	nuke.message('Select a node with point position pass')
    	return
    selectOnly(node)
    pointSelector = nuke.createNode('NoOp', 'name PointCreator')
    kButtonAdd = nuke.PyScript_Knob('addPos', 'Add Point')
    kButtonAdd.setValue("n = nuke.thisNode()\nposKnobs = [x for x in n.knobs().values() if 'position' in x.name()]\nif len(posKnobs) < 4:\n    i = 1\n    for k in posKnobs:\n        if int(k.name()[-1]) > i: i = int(k.name()[-1])\n\n    kPos = nuke.XY_Knob('position%s' % str(i+1), 'Position%s' % str(i+1))\n    n.addKnob(kPos)\n")
    kButtonRec = nuke.PyScript_Knob('reconcile', 'Reconcile!')
    kButtonRec.setValue('Pto2dTrack.reconcilePositsionKnobs()')
    kPos1 = nuke.XY_Knob('position1', 'Position1')
    kPos1.setFlag(nuke.STARTLINE)

    for i in (kButtonAdd, kButtonRec, kPos1):
        pointSelector.addKnob(i)


def reconcilePositsionKnobs():
	n = nuke.thisNode()
	posKnobs = [x for x in n.knobs().values() if 'position' in x.name()]
	positions2d = []
	for k in posKnobs:
		positions2d.append(k.value())

	#print positions2d
	layers = list(set([x.split('.')[0] for x in n.channels()]))
	#print layers
	if 'P' in layers:
		sh = nuke.createNode('Shuffle', 'in P')
	else:		
		p = nuke.Panel("Select Position pass", 450)
		p.addEnumerationPulldown('Passes', '%s' % ' '.join(layers))
		result = p.show()
		if not result: return
		#print p.value('Passes')
		sh = nuke.createNode('Shuffle', 'in %s' % p.value('Passes'))
		#return

	sh.setInput(0, n)
	selectOnly()

	axisPos = []
	#print len(positions2d)
	for p in positions2d:
		x, y, z = 0, 0, 0
		x = nuke.sample(sh, 'r', p[0], p[1])
		y = nuke.sample(sh, 'g', p[0], p[1])
		z = nuke.sample(sh, 'b', p[0], p[1])
		axisPos.append((x, y, z))

	#print axisPos
	#return
	nuke.delete(sh)


	axisNodes = []
	for pos in axisPos:
		a = nuke.createNode('Axis2')
		selectOnly()
		a['translate'].setValue((pos[0], pos[1], pos[2]))
		axisNodes.append(a)


	for i in range(len(axisNodes)):
		axisNodes[i].setXYpos(n.xpos() + 110*i, n.ypos() + 80)

	nuke.delete(n)



#positionNodeCreate()




################################
# n = nuke.thisNode()
# posKnobs = [x for x in n.knobs().values() if 'position' in x.name()]
# if len(posKnobs) < 4:
#     i = 1
#     for k in posKnobs:
#         if int(k.name()[-1]) > i: i = int(k.name()[-1])

#     kPos = nuke.XY_Knob('position%s' % str(i+1), 'Position%s' % str(i+1))
#     n.addKnob(kPos)
