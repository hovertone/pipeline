# Autolife v1.0
# Autolife is based on SetRotoLifetimeAll by Marc Gutowski (http://www.nukepedia.com/python/nodegraph/setrotolifetimeall/)

# Instructions
# Put autolife.py in your .nuke directory or path
# Put "import autolife" in your menu.py file

# This python script adds an 'autolife!' button to a 'user' tab on all Roto and Rotopaint nodes
# When clicked, all shapes or strokes that are locked, will have the lifetime automatically set
# to their first and last keyframe. I found myself setting the frame range manually for this a lot,
# especially when roto'ing objects that need new shapes very often, so I made Autolife to speed the
# workflow up.

# Please let me know if you come across any bugs or have suggestions, and I'll try fix or add them!

import nuke

elements = []

def addAutoLife():
  n = nuke.thisNode()
  n.addKnob(nuke.PyScript_Knob('autolife', 'autolife!', 'autolife.autoLife()'))

def getElements(layer): 
  for element in layer: 
    if isinstance(element, nuke.rotopaint.Layer): 
      getElements(element)
    elif isinstance(element, nuke.rotopaint.Stroke) or isinstance(element, nuke.rotopaint.Shape):
      elements.append(element)

  return elements

def autoLife():
  n = nuke.thisNode()
  
  nodec = n['curves']
  nlayer = nodec.rootLayer
  
  global elements
  # Clear global elements array so that only the current Roto/Rotopaint node's elements are 'autolifed'
  elements = []
  getElements(nlayer)
  
  for element in elements:
    if element.locked:
      element.locked = False
      
      # Get keyframes for the 0-indexed control point
      if isinstance(element, nuke.rotopaint.Stroke):
	keys = element[0].getControlPointKeyTimes()
      elif isinstance(element, nuke.rotopaint.Shape):
	keys = element[0].center.getControlPointKeyTimes()
      
      firstKey = keys[0]
      lastKey = keys[-1]
      
      attrs = element.getAttributes()
      attrs.set('ltn', firstKey) # frame range 'from' value
      attrs.set('ltm', lastKey) # frame range 'to' value
      attrs.set('ltt', 4) # set 'lifetime type' of element to 'frame range' - index 4 in combobox
      
      element.locked = True
      nodec.changed()


def autolifeSelectedShape():
  if nuke.selectedNode().Class() != 'Roto' and nuke.selectedNode().Class() != 'RotoPaint':
    nuke.message('Select Roto or RotoPaint Node')
  else:
    node = nuke.selectedNode()
    curves = node['curves']
    selectedShapes = curves.getSelected()
    for element in selectedShapes:
      # Get keyframes for the 0-indexed control point
      if isinstance(element, nuke.rotopaint.Stroke):
        keys = element[0].getControlPointKeyTimes()
      elif isinstance(element, nuke.rotopaint.Shape):
        keys = element[0].center.getControlPointKeyTimes()
      
      firstKey = keys[0]
      lastKey = keys[-1]
      
      attrs = element.getAttributes()
      attrs.set('ltn', firstKey) # frame range 'from' value
      attrs.set('ltm', lastKey) # frame range 'to' value
      attrs.set('ltt', 4) # set 'lifetime type' of element to 'frame range' - index 4 in combobox
      
      curves.changed()

      print '%s shape locked [%s %s]' % (element.name, int(firstKey), int(lastKey))


nuke.addOnCreate(addAutoLife, nodeClass='Roto')
nuke.addOnCreate(addAutoLife, nodeClass='RotoPaint')
