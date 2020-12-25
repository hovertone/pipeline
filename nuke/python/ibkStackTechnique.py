import nuke, nukescripts

def nodeCopyPaste():
    nuke.nodeCopy("%clipboard%")    
    return  nuke.nodePaste("%clipboard%")

def ibkStackDuplicate():
	n = nuke.selectedNode()
	firstIBKcolour = False
	if 'IBKColourV' not in n.dependencies()[0].Class():
		firstIBKcolour = True

	print firstIBKcolour

	if firstIBKcolour == True:
		n1 = n
		n2 = nodeCopyPaste()

		exprOff = 'parent.%s.off' % (n1.name())
		exprMult = 'parent.%s.mult' % (n1.name())
		n2['off'].setExpression(exprOff)
		n2['mult'].setExpression(exprMult)

		n2['multi'].setValue('1')
	else:
		n1 = n
		if n1['off'].hasExpression() and n1['mult'].hasExpression():
			n2 = nodeCopyPaste()

			exprOff = n1['off'].animation(0).expression()
			exprMult = n1['mult'].animation(0).expression()
			n2['off'].setExpression(exprOff)
			n2['mult'].setExpression(exprMult)

		else:
			n2 = nodeCopyPaste()


		print n2.name()
		n2['multi'].setValue(n2.dependencies()[0]['multi'].value()*2)

	nuke.selectAll()
	nuke.invertSelection()

	n2.setSelected(True)