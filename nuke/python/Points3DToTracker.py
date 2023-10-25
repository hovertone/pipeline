from __future__ import with_statement 
import nuke
import os

if os.name == 'nt':
    from scripts import autoplace
if os.name == 'posix':
	pass
#    TFXMenu.addCommand("Create Axis From Selected 3d Point", 'createAxis()', 'shift+a',icon='createAxis.png')
#    TFXMenu.addCommand("Create Tracker from 3d Points", 'reconcileFrom_4_Axis()', 'ctrl+b', icon='reconcileFrom_4_Axis.png')
#    TFXMenu.addCommand("Create Many trackers from every 3d point", 'reconcileAllAxis', icon='reconcileFrom_4_Axis.png')
#    TFXMenu.addCommand("Copy Traking Data to Roto", 'copyTrackingToRoto()', 'shift+b',icon='copyTrackingToRoto.png')
#    TFXMenu.addCommand("Tracker iz proshlogo", 'nuke.createNode("Tracker3")', icon='Tracker.png')


def removeInputs(node):
    for j in range(node.inputs()): 
        node.setInput(j, None)

def getXpos(n):
    return n.xpos()

def autoplace():
    nodes = sorted(nuke.selectedNodes(),key=getXpos)
    
    for i in range(len(nodes)):
        nodes[i].setXYpos(nodes[0].xpos() + i*110,nodes[0].ypos())

def returnAxisPos(groupNodeName = 'Trackers'):
    grp = nuke.toNode(groupNodeName)

    with grp:
        selNodes = nuke.selectedNodes()
        trackers = []
        for i in range(len(selNodes)):
            if selNodes[i].Class() == 'Sphere' or selNodes[i].Class() == 'SphereObj': trackers.append(selNodes[i])

        if len(trackers) == 0:
            return []
        pos = []

        for tr in trackers:
            pos.append(tr['translate'].value())

    return pos


def createAxis(nodes = []):
	if nodes == []: nodes = nuke.selectedNodes()
	selNodes = nodes
	print(nodes)
	for n in nodes:
		if n.Class() == 'Group':
			groupNode = n
			break

	if 'groupNode' not in locals():
		if nuke.exists('Trackers'):
			groupNode = nuke.toNode('Trackers')
		else:
			nuke.message('There is no group node exists')
			return

	pos = returnAxisPos(groupNode.name())
	axiss = []
	for i in range(len(pos)):
		a = nuke.createNode('Axis')
		removeInputs(a)
		a.setXYpos(groupNode.xpos() + (i+1) * 110, groupNode.ypos())
		a['translate'].setValue(pos[i])
		axiss.append(a)

	nuke.selectAll()
	nuke.invertSelection()
	for n in selNodes:
		n.setSelected(True)

	return axiss

def reconcileFrom_4_Axis(nodes = []):
	if nodes == []: nodes = nuke.selectedNodes()
	axiss = []
	#print nodes
	warpedLens = False
	for n in nodes:
		#print "%s is a %s type node" % (n.name(), n.Class())
		if n.Class() == 'Camera2' or n.Class() == 'Camera':
			camera = n
		elif n.Class() == 'Reformat' or n.Class() == 'Read':
			ref = n
		elif n.Class() == 'Axis2' or n.Class() == 'Axis' or n.Class() == 'Axis4':
			axiss.append(n)
		elif n.Class() == 'LensDistortion':
			lensDist = n
			warpedLens = True
			
	#print camera.name(), ref.name(), axiss

	if len(axiss) == 0:
		axiss = createAxis()

	if 'camera' not in locals():
		nuke.message('No camera node has been selected.')
		return
	if 'ref' not in locals():
		nuke.message('No background node has been selected.')
		return
	if len(axiss) == 0:
		nuke.message('No axis node has been selected.')
		return

	if len(axiss) > 4: 
		axiss = axiss[:4]

	nuke.selectAll()
	nuke.invertSelection()
	rec3d = nuke.createNode('Reconcile3D')

	rec3d.setXYpos(axiss[0].xpos(), axiss[0].ypos() - 80)

	if ref.Class() == 'Read':
		frtFrame = ref.firstFrame()
		lstFrame = ref.lastFrame()
	else:
		frtFrame = nuke.root()['first_frame'].value()
		lstFrame = nuke.root()['last_frame'].value()

	out = nuke.getFramesAndViews('frame range', '%s-%s' % (int(frtFrame), int(lstFrame)))
	if out == None: return

	frtFrame = int(float(out[0][:out[0].index('-')]))
	lstFrame = int(float(out[0][out[0].index('-') + 1:]))

	outTracker = nuke.createNode('Tracker3')	
	outTracker.setXYpos(rec3d.xpos() + 110, rec3d.ypos())
	removeInputs(outTracker)
	for i in range(len(axiss)):
		rec3d.setInput(2, axiss[i])
		rec3d.setInput(1, camera)
		rec3d.setInput(0, ref)

		nuke.execute(rec3d.name(), frtFrame, lstFrame)
		outTracker['enable' + str(i+1)].setValue(True)
		outTracker['use_for' + str(i+1)].setValue('all')
		print('warpedLens %s' % warpedLens)
		if warpedLens == True:
			distTrack = nuke.createNode('DistortTracks', inpanel = False)
			distTrack.setInput(0, lensDist)
			distTrack['add_track'].execute()
			distTrack['track_0'].fromScript(rec3d['output'].toScript())
			distTrack['execute'].execute()
			outTracker['track' + str(i+1)].fromScript(distTrack['trk_out_0'].toScript())
			nuke.delete(distTrack)
		else:
			outTracker['track' + str(i+1)].fromScript(rec3d['output'].toScript())

	outTracker['transform'].setValue('match-move')
	outTracker['reference_frame'].setValue(nuke.frame())

	for n in axiss:
		pass
		#nuke.delete(n)
	nuke.delete(rec3d)


def reconcileAllAxis(nodes = []):
	if nodes == []: nodes = nuke.selectedNodes()
	axiss = []
	#print nodes
	for n in nodes:
		#print "%s is a %s type node" % (n.name(), n.Class())
		if n.Class() == 'Camera2' or n.Class() == 'Camera':
			camera = n
		elif n.Class() == 'Reformat' or n.Class() == 'Read':
			ref = n
		elif n.Class() == 'Axis':
			axiss.append(n)

	#print camera.name(), ref.name(), axiss

	if len(axiss) == 0:
		axiss = createAxis()

	if len(axiss) == 0:
		nuke.message('Select axis nodes or trackers in viewport.')
		return

	if 'camera' not in locals():
		nuke.message('No camera node has been selected.')
		return
	if 'ref' not in locals():
		nuke.message('No background node has been selected.')
		return
	if len(axiss) == 0:
		nuke.message('No axis node has been selected.')
		return

	nuke.selectAll()
	nuke.invertSelection()

	rec3d = nuke.createNode('Reconcile3D')
	rec3d.setXYpos(axiss[0].xpos(), axiss[0].ypos() - 80)

	frtFrame = ref.firstFrame()
	lstFrame = ref.lastFrame()

	trackers = []

	for i in range(len(axiss)):
		outTracker = nuke.createNode('Tracker3')	
		outTracker.setXYpos(rec3d.xpos() + 110, rec3d.ypos())
		trackers.append(outTracker)

		removeInputs(outTracker)

		rec3d.setInput(2, axiss[i])
		rec3d.setInput(1, camera)
		rec3d.setInput(0, ref)

		nuke.execute(rec3d.name(), frtFrame, lstFrame)
		outTracker['enable1'].setValue(True)
		outTracker['use_for1'].setValue(1)
		outTracker['track1'].fromScript(rec3d['output'].toScript())

		outTracker['transform'].setValue('match-move')
		outTracker['reference_frame'].setValue(nuke.frame())

	for n in axiss:
		pass
		#nuke.delete(n)
	nuke.delete(rec3d)

	nuke.selectAll()
	nuke.invertSelection()
	for t in trackers:
		t.setSelected(True)

	autoplace()


def copyTrackingToRoto(linkinp = False):
    nodes = nuke.selectedNodes()
    if linkinp == True:
      link = True
    else:
      link = False
        
    for n in nodes:
        #print n.Class()
        if n.Class() == 'Roto' or n.Class() == 'RotoPaint' or n.Class() == 'Bezier': roto = n
        elif n.Class() == 'Tracker3' or n.Class() == 'Tracker4' or n.Class() == 'Transform': tr = n
        elif n.Class() == 'Dot': 
        	link = True
        	dot = n

    print(tr.name(), roto.name())
    if 'roto' not in locals() or 'tr' not in locals():
        nuke.message('Select proper nodes')
        return

    knobsTemplate = ['translate', 'rotate', 'scale', 'center']
    for i in knobsTemplate:
        if tr.knobs()[i].isAnimated:
          if link:
              trName = tr.name()
              roto[i].setExpression('parent.' + trName + '.' +  i)
          else:
              roto[i].fromScript(tr[i].toScript())

    if 'dot' in locals():
    	nuke.delete(dot)

    if tr.Class() != 'Transform':
    	if roto['label'].value() != '':
    		oldRotoLabel = roto['label'].value()
    		roto['label'].setValue('%s\n' % oldRotoLabel + 'frame ' + str(tr['reference_frame'].value()))
    	else:
    		roto['label'].setValue('frame ' + str(tr['reference_frame'].value()))
