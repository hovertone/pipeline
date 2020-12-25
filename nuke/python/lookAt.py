import nuke

def makeAimConstrain(nodes):
	if len(nodes) != 2:
		nuke.message('Select correct number of nodes (2).')
		return
	else:
		for n in nodes:
			if 'translate' not in n.knobs() or 'rotate' not in n.knobs():
				nuke.message('Incorrect nodes. Only nodes with translate and rotate knobs are ')
				return

		if nuke.ask('You want make %s look at %s? (Yes)\nOr %s look at %s? (No)' % (nodes[1].name(), nodes[0].name(), nodes[0].name(), nodes[1].name())):
			aim, target = nodes[1], nodes[0]
		else:
			aim, target = nodes[0], nodes[1]


	rk = aim['rotate']
	if rk.isAnimated():
		rk.clearAnimated()

	print 'Aim is %s, Target is %s' % (aim.name(), target.name())
	rk.setExpression("-degrees(atan2 ((%s.translate.y - %s.translate.y), sqrt(pow2(%s.translate.z - %s.translate.z) + pow2(%s.translate.x - %s.translate.x))))" % (aim.name(), target.name(), aim.name(), target.name(), aim.name(), target.name()), 0)

	rk.setExpression("(%s.translate.z - %s.translate.z)<=0?180 -degrees(atan2 ((%s.translate.x - %s.translate.x), abs(%s.translate.z - %s.translate.z))):-degrees(atan2 ((%s.translate.x - %s.translate.x), abs(%s.translate.z - %s.translate.z)))" % (aim.name(), target.name(), aim.name(), target.name(), aim.name(), target.name(), target.name(), aim.name(), aim.name(), target.name()), 1)

#makeAimConstrain(nuke.selectedNodes())
