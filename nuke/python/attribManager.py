import nuke


def addStringAttr(node, attrName, attrValue = '', enabled = True, visible = True):
	#root = nuke.root()
	if attrName not in node.knobs().keys():
		attr = nuke.EvalString_Knob(attrName, attrName)
		attr.setValue(attrValue)
		attr.setEnabled(enabled)
		#attr.setVisible(visible)
		node.addKnob(attr)
	else:
		attr = node[attrName]
		attr.setValue(str(attrValue))
		attr.setEnabled(enabled)

	return attr

def removeAttr(node, attrName):
	if attrName in node.knobs().keys():
		node.removeKnob(node[attrName])
	else:
		print 'There is no %s tab in %s node' % (attrName, node.name())


def addTab(node, tabName, visible = True):
	if tabName not in node.knobs().keys():
		t = nuke.Tab_Knob(tabName, tabName)
		if not visible:
			t.setFlag(nuke.INVISIBLE)
		node.addKnob(t)
	else:
		print 'There is one %s tab already. Dissmiss!' % tabName

	return node[tabName]

def removeTab(node, tabName):
	if tabName in node.knobs().keys():
		node.removeKnob(node[tabName])
	else:
		print 'There is no %s tab in %s node' % (tabName, node.name())