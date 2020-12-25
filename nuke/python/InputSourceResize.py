# hide input in dot node
def dotHideInput():
	nuke.createNode ("Dot")
	n = nuke.selectedNode()
	n["hide_input"].setValue(True)
	n["tile_color"].setValue(4278190335)
	n["note_font_size"].setValue(21)
	input = nuke.getInput("Dot name")
	n["label"].setValue(input)

# hotkey for menu.py
menuNodes = nuke.menu('Nodes')
ksumenu = menuNodes.addMenu('Ksu menu', 'Ksu menu')
ksumenu.addCommand('Dot hide input', 'ksucommands.dotHideInput()', 'shift+.')




# precomp setup

p = nuke.Panel('create precomp')
precomp_name = p.addSingleLineInput('precomp name', '')
file_type = p.addEnumerationPulldown('file type', 'exr dpx jpeg mov png tiff')
p.addButton('cancel')
p.addButton('render')
ret = p.show()
if ret:
    print p.value('precomp name')
else:
    print 'dismissed'




n = nuke.selectedNode()
nxpos = n['xpos'].value()
nypos = n['ypos'].value()

d0 = nuke.createNode ("Dot")
d0['xpos'].setValue( nxpos + 35)
d0['ypos'].setValue( nypos + 100)

d1 = nuke.createNode ("Dot")
d1['xpos'].setValue( nxpos + 200)
d1['ypos'].setValue( nypos + 100)

w = nuke.createNode ("Write")
w['xpos'].setValue( nxpos + 167)
w['ypos'].setValue( nypos + 170)
w["tile_color"].setValue(3741384703)
#file_path = 'C:\Users\%s\%s' % (project, date)
#w["file"].setValue('file_path + precomp_name')
#w["file_type"].setValue(file_type)

r = nuke.createNode ("Read")
r['xpos'].setValue( nxpos + 167)
r['ypos'].setValue( nypos + 300)
r["file"].setValue('file_path + precomp_name')

d2 = nuke.createNode ("Dot")
d2['xpos'].setValue( nxpos + 200)
d2['ypos'].setValue( nypos + 435)

s = nuke.createNode ("Switch")
s['xpos'].setValue( nxpos)
s['ypos'].setValue( nypos + 430)
s.setInput(0, d0)
s.setInput(1, d2)
s["tile_color"].setValue(4278190335)
s['which'].setValue(1)














def 5kMagic


a = nuke.allNodes()

if a.Class() == "Roto":



a["center"].setValue(0, 0)

if a.Class() == "RotoPaint":

	cKnob= a['curves']
	root = cKnob.rootLayer



# single Roto node
n = nuke.selectedNode()
cKnob = n['curves']
root = cKnob.rootLayer

lt = root.getTransform()
lt.getScaleAnimCurve(0).constantValue = 2.5
lt.getScaleAnimCurve(1).constantValue = 2.5
lt.getPivotPointAnimCurve(0).constantValue = 0
lt.getPivotPointAnimCurve(1).constantValue = 0
n['cliptype'].setValue('bbox')

cKnob.changed()


# multiple Roto nodes
n = nuke.selectedNodes()
for n in nuke.selectedNodes():
	cKnob = n['curves']
	root = cKnob.rootLayer

	lt = root.getTransform()
	lt.getScaleAnimCurve(0).constantValue = 1.66666
	lt.getScaleAnimCurve(1).constantValue = 1.66666
	lt.getPivotPointAnimCurve(0).constantValue = 0
	lt.getPivotPointAnimCurve(1).constantValue = 0
	n['cliptype'].setValue('bbox')

	cKnob.changed()

# multiple tracker nodes
n = nuke.selectedNodes()
for n in nuke.selectedNodes():
    k = n['translate']
    c = n['center']
    k.setExpression('curve * 1.66666')
    c.setExpression('curve * 1.66666')

#attempt for multiple Tracker nodes with CTRL node
n = nuke.selectedNodes()
for n in nuke.selectedNodes():
	t = n['translate']
	c = n['center']
	tcurve = n['translate'].value()
	ccurve = n['center'].value()
	ctrl = nuke.toNode( 'CTRL2' )
	t.setExpression('CTRL2.fiveK ? %s * CTRL2.multiplier : %s' % (tcurve, tcurve))
	c.setExpression('CTRL2.fiveK ? %s * CTRL2.multiplier : %s' % (ccurve, ccurve))

# Blur and Erode nodes

n = nuke.selectedNodes()
for n in nuke.selectedNodes():
    s = n['size']
    s_value = n['size'].value()
    ctrl = nuke.toNode( 'CTRL2' )
    multiplier = ctrl['multiplier'].value()
    s.setValue(multiplier*s_value)
    s.setExpression('CTRL2.fiveK ? %s * CTRL2.multiplier : %s' % (s_value, s_value))

# Brush size for rotopain nodes
import nuke.rotopaint as rp

rp_node = nuke.selectedNode()
rp_curves_knob = rp_node['curves']

for element in rp_curves_knob.rootLayer:
    if isinstance(element, nuke.rotopaint.Stroke):
        attr = element.getAttributes()
        bs = attr.getValue(1, attr.kBrushSizeAttribute)
        attr.set(attr.kBrushSizeAttribute, bs*1.666666)        

rp_curves_knob.changed()


# Switch nodes
n = nuke.selectedNodes()
for n in nuke.selectedNodes():
    w = n['which']
    w_value = n['which'].value()
    ctrl = nuke.toNode( 'Switch_controller_5k' )
    w.setValue(multiplier*s_value)
    w.setExpression('Switch_controller_5k.fiveK ? %s : %s' % (1, 0))


# Transform nodes
n = nuke.selectedNodes()
for n in nuke.selectedNodes():
    s = n['scale']
    c = n['center']
    s.setExpression('curve * 2.5')
    c.setExpression('0')

























set cut_paste_input [stack 0]
version 10.0 v2
push $cut_paste_input
NoOp {
name CTRL
selected true
xpos 448
ypos 36
addUserKnob {20 User}
addUserKnob {6 fiveK l "5k (for switch nodes)" +STARTLINE}
fiveK true
addUserKnob {22 Switch_nodes l "Switch nodes" t "select Switch nodes and push this button once" T "n = nuke.selectedNodes()\nfor n in nuke.selectedNodes():\n    w = n\['which']\n    w_value = n\['which'].value()\n    ctrl = nuke.toNode( 'CTRL' )\n#    w.setValue(multiplier*s_value)\n    w.setExpression('CTRL.fiveK ? %s : %s' % (1, 0))" +STARTLINE}
addUserKnob {16 multiplier_for_blur_and_erode l "multiplier for blur/erode"}
multiplier_for_blur_and_erode 2.5
addUserKnob {6 blur_erode_to_5k l "blur/erode to 5k" +STARTLINE}
blur_erode_to_5k true
addUserKnob {22 Blur_and_erode_nodes l "Blur and erode nodes" t "select Blur and Erode nodes that need to be transformed to 5K and push this button once" T "n = nuke.selectedNodes()\nfor n in nuke.selectedNodes():\n    s = n\['size']\n    s_value = n\['size'].value()\n    ctrl = nuke.toNode( 'CTRL' )\n    multiplier = ctrl\['multiplier_for_blur_and_erode'].value()\n    s.setValue(multiplier*s_value)\n    s.setExpression('CTRL.blur_erode_to_5k ? %s * CTRL.multiplier_for_blur_and_erode : %s' % (s_value, s_value))" +STARTLINE}
addUserKnob {16 multiplier_for_roto l "multiplier for roto"}
addUserKnob {6 roto_to_5k l "roto to 5k" +STARTLINE}
addUserKnob {22 Roto_nodes l "Roto nodes" t "select Roto nodes that need to be transformed to 5K and push this button once" T "n = nuke.selectedNodes()\nfor n in nuke.selectedNodes():\n    cKnob = n\['curves']\n    root = cKnob.rootLayer\n\n    lt = root.getTransform()\n    ctrl = nuke.toNode( 'CTRL' )\n    multiplier = ctrl\['multiplier_for_roto'].value()\n    if CTRL.roto_to_5k:\n        lt.getScaleAnimCurve(0).constantValue = 2.5\n        lt.getScaleAnimCurve(1).constantValue = 2.5\n        lt.getPivotPointAnimCurve(0).constantValue = 0\n        lt.getPivotPointAnimCurve(1).constantValue = 0\n        n\['cliptype'].setValue('bbox')\n        cKnob.changed()\n    else None" +STARTLINE}
addUserKnob {16 multiplier_for_rotopaint l "multiplier for rotopaint"}
addUserKnob {6 rotopaint_to_5k l "rotopaint to 5k" +STARTLINE}
addUserKnob {22 Rotopaint_nodes l "Rotopaint nodes" t "select Rotopaint nodes that need to be transformed to 5K and push this button once" T "import nuke.rotopaint as rp\n\n\nn = nuke.selectedNodes()\nfor n in nuke.selectedNodes():\n\n    rp_node = n\n    rp_curves_knob = rp_node\['curves']\n    \n    # Layer creation\n    \n    layer = rp.Layer(rp_curves_knob)\n    layer.name = 'a new name'\n    rp_curves_knob.rootLayer.append(layer)\n    rp_curves_knob.changed()\n    \n    # simple roto case\n    lt = layer.getTransform()\n    lt.getScaleAnimCurve(0).constantValue = 2.5\n    lt.getScaleAnimCurve(1).constantValue = 2.5\n    \n    \n    # Brush sizes\n    for element in rp_curves_knob.rootLayer:\n        if isinstance(element, nuke.rotopaint.Stroke):\n            attr = element.getAttributes()\n            bs = attr.getValue(1, attr.kBrushSizeAttribute)\n            attr.set(attr.kBrushSizeAttribute, bs*2.5)        \n    \n    rp_curves_knob.changed()\n    \n    \n    ## clip to bbox\n    rp_node\['cliptype'].setValue('bbox')" +STARTLINE}
addUserKnob {16 multiplier_for_tracker l "multiplier for tracker"}
multiplier_for_tracker 2.5
addUserKnob {6 tracker_to_5k l "tracker to 5k" +STARTLINE}
tracker_to_5k true
addUserKnob {22 Tracker_nodes l "Tracker nodes" t "select Tracker nodes that need to be transformed to 5K and push this button once" T "n = nuke.selectedNodes()\nfor n in nuke.selectedNodes():\n    t = n\['translate']\n    c = n\['center']\n    tcurve = n\['translate'].value()\n    ccurve = n\['center'].value()\n    ctrl = nuke.toNode( 'CTRL' )\n    multiplier = ctrl\['multiplier_for_tracker'].value()\n    t.setExpression('CTRL.tracker_to_5k ? %s * %s : %s' % ('curve', multiplier, 'curve'))\n    c.setExpression('CTRL.tracker_to_5k ? %s * %s : %s' % ('curve', multiplier, 'curve'))" +STARTLINE}
addUserKnob {7 multiplier_for_transform l "multiplier for transform"}
multiplier_for_transform 2.5
addUserKnob {6 transform_to_5K l "transform to 5K" +STARTLINE}
addUserKnob {22 Transform_nodes l "Transform nodes" t "select Transform nodes that need to be transformed to 5K and push this button once" T "n = nuke.selectedNodes()\nfor n in nuke.selectedNodes():\n    s = n\['scale']\n    c = n\['center']\n    ctrl = nuke.toNode( 'CTRL' )\n    multiplier = ctrl\['multiplier_for_transform'].value()\n    s.setExpression('CTRL.transform_to_5k ? %s * %s : %s' % ('curve', multiplier, 'curve'))\n    c.setExpression('0')" +STARTLINE}
}


























































#Noop with a button
n = nuke.createNode ("NoOp")
n["hide_input"].setValue(True)
n["tile_color"].setValue(4278190335)
n["name"].setValue('Hi there')
n["note_font_size"].setValue(15)

btn1 = nuke.PyScript_Knob("push me if you want to know a secret")
btn1.setTooltip('if you dare')
n.addKnob(btn1)
btn1.setCommand("nuke.message('everything is going to be amazing :) but tssss!')")


#Noop with a button
n = nuke.createNode ("NoOp")
n["hide_input"].setValue(True)
n["tile_color"].setValue(4278190335)
n["name"].setValue('Hi there')
n["note_font_size"].setValue(15)

btn1 = nuke.PyScript_Knob("push me if you want to know a secret")
btn1.setTooltip('if you dare')
n.addKnob(btn1)
btn1.setCommand("nuke.message('everything is going to be amazing :) but tssss!')")


























# JPEGs for Lena

from CUF import selectOnly

def createThumbs(path, nodes = '', scaleValue = 0.2, jpegQuality = 90):
    if nodes == '':
        nodes = nuke.selectedNodes()

    #print nodes
    for n in nodes:
        fr = n
        n = n.dependencies()[0]
        #print n.name()
        fileName = n['file'].value().split('/')[-1]
        shot = fileName[:9]
        seq = n['file'].value().split('/')[-2][-1]
        #lenght = n['last'].value() - n['first'].value() + 1

        #print '%s %s' % (seq, shot), lenght

        selectOnly(fr)
        ref = nuke.createNode('Reformat')
        ref['type'].setValue('scale')
        ref['scale'].setValue(scaleValue)

        selectOnly(ref)
            
        w = nuke.createNode('Write')
        wpath = os.path.join(path + seq, '%s.jpg' % shot) 


        w['file'].setValue(wpath)
        # w['label'].setValue('yes')
        w['_jpeg_quality'].setValue(90)
        nuke.execute(w['name'].value(), w.firstFrame(), w.firstFrame())
    
        nukescripts.cache_clear("")

createThumbs('/mnt/projects/temp/Elena Mas/Beatus/reel_0', nodes = nuke.selectedNodes(), scaleValue = 0.0929)





# Zastava attempt



def selectOnly(nodes = []):
    '''
    Deselects all nodes, and selects nodes from provided list of nodes
    
    Arguments(nodes)
        {nodes} list of the nodes to select ([ by default])
    =======================================================
    '''
    nuke.selectAll()
    nuke.invertSelection()
    if type(nodes) == list:
        for n in nodes:
            n.setSelected(True)
    else:
        nodes.setSelected(True)


def createThumbs(path, nodes = '', scaleValue = 0.2, jpegQuality = 90):
    if nodes == '':
        nodes = nuke.selectedNodes()

    #print nodes
    for n in nodes:
        fr = n
        n = n.dependencies()[0]
        #print n.name()
        fileName = n['file'].value().split('/')[-1]
        shot = fileName[:9]
        seq = n['file'].value().split('/')[-2][-1]
        #lenght = n['last'].value() - n['first'].value() + 1

        #print '%s %s' % (seq, shot), lenght

        selectOnly(fr)
        ref = nuke.createNode('Reformat')
        ref['type'].setValue('scale')
        ref['scale'].setValue(scaleValue)

        selectOnly(ref)
            
        w = nuke.createNode('Write')
        wpath = os.path.join(path + seq, '%s.jpg' % shot) 


        w['file'].setValue(wpath)
        # w['label'].setValue('yes')
        w['_jpeg_quality'].setValue(90)
        nuke.execute(w['name'].value(), w.firstFrame(), w.firstFrame())
    
        nukescripts.cache_clear("")

createThumbs('/mnt/projects/temp/Reva/Zastava/reel_0', nodes = nuke.selectedNodes(), scaleValue = 0.0929)











# Reload all Read nodes in the script (inside Noop node)
set cut_paste_input [stack 0]
version 10.0 v2
push $cut_paste_input
NoOp {
 name Read_nodes_reload
 tile_color 0xaa55ffff
 selected true
 xpos -580
 ypos 2346
 addUserKnob {20 User}
 addUserKnob {22 Reload l "Reload all Read nodes" t "push the button ;)" T "nodes = nuke.allNodes()\nfor node in nodes:\n    if node.Class() == 'Read' and n != None:\n        node.knob('selected').setValue(True)\n        node.knob(\"reload\").execute()" +STARTLINE}
}



# Select a node from its Class
nodes = nuke.allNodes()
for node in nodes:
    if node.Class() == 'OFXcom.absoft.neatvideo4_v4' and n != None:
        node.knob('selected').setValue(True)



# Roto node default settings (for Lesha)
nuke.knobDefault('Roto.toolbox','createBSpline')
nuke.knobDefault('Roto.cliptype', 'no_clip')
nuke.knobDefault('Roto.output', 'alpha')