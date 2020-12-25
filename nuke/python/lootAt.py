def makeAimConstrain(nodes):
	if len(nodes) != 2:
		nuke.message('Select correct number of nodes (2).')
		return
	else:
		for n in nodes:
			if 'translate' not in n.knobs() or 'rotate' not in n.knobs():
				nuke.message('Incorrect nodes. Only nodes with translate and rotate knobs are ')
				return
			else:
				if nuke.ask('You want make %s look at %s? (Yes)\nOr %s look at %s? (No)' % (nodes[0], nodes[], nodes[1], nodes[0])):
					aim, target = nodes[0], nodes[1]
				else:
					aim, target = nodes[1], nodes[0]
	print 'aim is %s, \ntarget is %s' % (aim.name(), target.name())

makeAimConstrain(nuke.selectedNodes())
