import nuke, os
from getpass import getuser
from CUF import selectOnly
username = getuser()

def createSubset():
	global username	
	#find a very low node - last one and connect to it
	try:
		n = nuke.selectedNode()
		selectOnly(n)
	except:
		pass
	
	if os.name == 'posix':
		path = '/home/%s/ns/ToolSets/mask.nk' % (username)
	else:
		path = 'C:/Users/%s/ns/ToolSets/mask.nk' % (username)
	m = nuke.loadToolset(path)

	m['bbox'].setValue('A')
	selectOnly()

	r = nuke.createNode('Roto')
	r.setXYpos(m.xpos() - 110, m.ypos() - 6)
	m.setInput(1, r)

	r['cliptype'].setValue('bbox')


def cornerPinFromBBox(node=None):
	try:
		if node == None:
			if len(nuke.selectedNodes()) < 1:
				nuke.message("Select at least one node to take BBox from.")
				return
			else:
				node = nuke.selectedNode()
	except:
		print 'Shitty error. Jump out of the widndow!'
			

	l = ['.bbox.x', '.bbox.y', '.bbox.w', '.bbox.h']
	BBoxValues = []
	for i in l:
	    BBoxValues.append(nuke.value(node.name() + i))

	x,y,w,h = int(BBoxValues[0]), int(BBoxValues[1]), int(BBoxValues[2]), int(BBoxValues[3])
	#print x,y,w,h
	from1 = (x, y)
	from2 = (x+w, y)
	from3 = (x+w, y+h)
	from4 = (x, y+h)
	#print from1, from2, from3, from4


	selectOnly(node)
	cp = nuke.createNode("CornerPin2D")
	cp['from1'].setValue(from1)
	cp['from2'].setValue(from2)
	cp['from3'].setValue(from3)
	cp['from4'].setValue(from4)
	#cp['copy_from_to'].execute()
