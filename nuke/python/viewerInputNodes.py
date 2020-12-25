### Creates presets for VIEWER_INPUT nodes 
# written by Howard Jones 2012
# modified 20th April 2013 - added HSV and Auo Shuffle.
# Normalize thanks to Diogo and Ivan for the method.
# version 1.3 - fixed default font path in Auto Shuffle's text node - shouldn't be required though
# version 1.4 - added archive option for existing Viewer_Input nodes, and picks up activeViewers input node name. handles shuffle nodes
# version 1.5 - added mergeExpression, Expression and ShuffleCopy


def IPNodesList():
  IPNodes=['Auto Shuffle', 'Grid', 'HSV', 'Mirror', 'Normalize', 'Over Checkerboard', 'Over 18% Grey', 'Saturation']
  return IPNodes

def getActiveViewerNode():
  return nuke.activeViewer().node().knob('input_process_node').getValue()

def viewerInput(ipNode=None, openPanel=False): 
  '''Creates or deletes a VIEWER_INPUT node and sets the active viewer to it'''
  IPNodes=IPNodesList()
  IPName=getActiveViewerNode()

  IPList = ['{%s}' % l for l in IPNodes]
  if not ipNode: # panel to select the appropriate IP mode if ipNode not set via menu.py
    p=nuke.Panel('Input Process',300)
    p.addEnumerationPulldown('IP node',' '.join(IPList))
    p.addBooleanCheckBox('open panel', False)
    pp=p.show()
    if pp:
      ipNode=p.value('IP node')
      openPanel=p.value('open panel')
    else:
      return
  if 'Remove'==ipNode:
    removeExistingNode(IPName)
    restoreArchivedNode(IPName)
    return

  makeViewerNode(ipNode, openPanel, IPName=IPName)
  nuke.activeViewer().node().knob('input_process').setValue(True)
  

def makeViewerNode(ipNode, openPanel, IPName=''): # select which VIEWER_INPUT to create from either the panel above or via menu.py
    removeExistingNode(IPName)
    if 'Mirror'== ipNode:
      n=mirrorIP(openPanel)
    elif 'Normalize'== ipNode:
      n=normalizeIP(openPanel)
    elif 'Grid'== ipNode:
      n=gridIP(openPanel)
    elif 'Saturation'== ipNode:
      n=saturationIP(openPanel)
    elif 'HSV'== ipNode:
      n=hsvIP(openPanel)
    elif 'Over Checkerboard'== ipNode:
      bg='CheckerBoard2'
      n=overIP(bg, openPanel)
    elif 'Over 18% Grey'== ipNode:
      bg='Constant'
      n=overIP(bg, openPanel)
    elif 'Auto Shuffle'== ipNode:
      n=autoShuffleIP(openPanel)

    n['name'].setValue(IPName)
    n['label'].setValue(ipNode)
    n.setXYpos(nuke.activeViewer().node().xpos()+100, nuke.activeViewer().node().ypos()+100)
    return

def removeExistingNode(IPName):
    IPNodes=IPNodesList()
    for i in nuke.allNodes():
        i['selected'].setValue(False)
        if IPName == i['name'].value():
            if i['label'].value() not in IPNodes:
              i['name'].setValue('ARCHIVED_'+IPName)
              print 'found existing IP node - archiving'
              return
            print 'deleting old viewer input node'
            if 'Auto Shuffle' in i['label'].value():
              removeViewerKnobChanged()
            i['selected'].setValue(True)
            nukescripts.node_delete(popupOnError=True)
    return

def restoreArchivedNode(IPName):
    for i in nuke.allNodes():
        if 'ARCHIVED_'+IPName == i['name'].value():
          print 'resoring archived IP node'
          i['name'].setValue(IPName)
          nuke.activeViewer().node().knob('input_process').setValue(False)

    return

def mirrorIP(openPanel=False):
  n=nuke.createNode('Mirror', inpanel=openPanel)
  n['Horizontal'].setValue(True)
  return n

def gridIP(openPanel=False):
  n=nuke.createNode('Grid', inpanel=openPanel)
  return n
  
def saturationIP(openPanel=False):
  hsv=nuke.createNode('Colorspace', inpanel=False)
  shuf=nuke.createNode('Shuffle', inpanel=False)
  
  hsv['colorspace_out'].setValue('HSV')
  hsv['selected'].setValue(True)
  
  shuf['red'].setValue('green')
  shuf['green'].setValue('green')
  shuf['blue'].setValue('green')

  hsv['selected'].setValue(True)
  shuf['selected'].setValue(True)
  
  n=nuke.collapseToGroup(show=openPanel)
  return n

def hsvIP(openPanel=False):
  hsv=nuke.createNode('Colorspace', inpanel=False)
  
  hsv['colorspace_out'].setValue('HSV')
  hsv['selected'].setValue(True)
  hsv['selected'].setValue(True)
  
  n=nuke.collapseToGroup(show=openPanel)
  return n
  
def overIP(bg, openPanel=False):
  BG=nuke.createNode(bg, inpanel=False)
  MG=nuke.createNode('Merge2', inpanel=False)
  MG.setInput(1,None)
  MG.setInput(0, BG)
  
  if 'Constant'==bg:
    BG['color'].setValue((0.18,0.18,0.18,0))

  BG['selected'].setValue(True)
  MG['selected'].setValue(True)
  n=nuke.collapseToGroup(show=openPanel)

  return n



def normalizeIP(openPanel=False):
  nDot=nuke.createNode('Dot', inpanel=False)
  maxD=nuke.createNode('Dilate', inpanel=False)
  minD=nuke.createNode('Dilate', inpanel=False)
  maxBB=nuke.createNode('CopyBBox', inpanel=False)
  minBB=nuke.createNode('CopyBBox', inpanel=False)
  fromMinMax=nuke.createNode('Merge2', inpanel=False)
  fromMinIn=nuke.createNode('Merge2', inpanel=False)
  mDivide=nuke.createNode('Merge2', inpanel=False)

  maxD.setInput(0,nDot)
  minD.setInput(0,nDot)
  maxBB.setInput(0,maxD)
  maxBB.setInput(1,nDot)
  minBB.setInput(0,minD)
  minBB.setInput(1,nDot)
  fromMinMax.setInput(0,maxBB)
  fromMinMax.setInput(1,minBB)
  fromMinIn.setInput(0,nDot)
  fromMinIn.setInput(1,minBB)
  mDivide.setInput(0,fromMinMax)
  mDivide.setInput(1,fromMinIn)

  maxD.setName('DilateMax')
  maxD['size'].setExpression('max(input.format.w, input.format.h)')
  minD.setName('DilateMin')
  minD['size'].setExpression('-max(input.format.w, input.format.h)')
  fromMinMax['operation'].setValue('from')
  fromMinIn['operation'].setValue('from')
  mDivide['operation'].setValue('divide')


  nDot['selected'].setValue(True)
  maxD['selected'].setValue(True)
  minD['selected'].setValue(True)
  maxBB['selected'].setValue(True)
  minBB['selected'].setValue(True)
  fromMinMax['selected'].setValue(True)
  fromMinIn['selected'].setValue(True)
  mDivide['selected'].setValue(True)

  n=nuke.collapseToGroup(show=openPanel)

  return n


def autoShuffleIP(openPanel=False):

  # find active viewer and set knobChanged
  try:
    v = nuke.ViewerWindow.node(nuke.activeViewer())
  except:
    v = nuke.createNode('Viewer')




  sc='''n=nuke.toNode('VIEWER_INPUT.ChannelShuffler')
activeVin=nuke.activeViewer().activeInput()
nodeName=nuke.activeViewer().node().input(activeVin).name()
i=nuke.toNode(nodeName)
k=nuke.thisKnob()
#print (k.name())
if k.name()=='input_number' or k.name()=='inputChange':
  #print 'knob recognised'
  # check nodes for certain available outputs and set knob2Use to the best guess.
  if i.Class() not in ('Shuffle', 'ShuffleCopy', 'MergeExpression', 'Expression'):
    try:
      if i['channels']:
        knob2Use='channels'
    except:
      knob2Use='output'

  else:
    if i.Class() in ('Shuffle', 'ShuffleCopy') :
      knob2Use='out'
    elif i.Class() in ('MergeExpression', 'Expression') :
      knob2Use='channel0'

  try:

    if not i[knob2Use].value() in ('all', 'none') :
        ch= i[knob2Use].value()
        n['in'].setValue(ch)
    else:
        n['in'].setValue('rgba')
  except:
       n['in'].setValue('rgba')
'''
 
  v['knobChanged'].setValue(sc)

  #createNodes for VIEWER_INPUT
  nShuffle=nuke.createNode('Shuffle', inpanel=False)
  nMerge=nuke.createNode('Merge2', inpanel=False)
  nText=nuke.createNode('Text', inpanel=False)

  #set parameters
  nShuffle['name'].setValue('ChannelShuffler')

  nText['name'].setValue('channelText')
  nText['replace'].setValue(True)
  nText['box'].setValue((0,0,1000,100))
  nText['yjustify'].setValue('bottom')
  nText['message'].setValue('[value ChannelShuffler.in]')
  nText['font'].setValue('[python nuke.defaultFontPathname()]')
  nText['disable'].setExpression('!showText')

  nMerge['operation'].setValue('exclusion') 
  nMerge['disable'].setExpression('!showText')

  #join
  nText.setInput(0,nShuffle)
  nMerge.setInput(0,nShuffle)
  nMerge.setInput(1,nText)

  #selectAll then group
  nShuffle['selected'].setValue(True)
  nText['selected'].setValue(True)
  nMerge['selected'].setValue(True)

  n=nuke.collapseToGroup(show=openPanel)
  #disconnect text node now it's collapsed
  txt=nuke.toNode(n.name()+'.channelText')
  txt.setInput(0,None)
  #add text option to viewer input group
  bk = nuke.Boolean_Knob("showText", "show text")
  n.addKnob(bk)
  n[bk.name()].setValue(True)

  return n


def removeViewerKnobChanged():
  for i in nuke.allNodes('Viewer'):
    i['knobChanged'].setValue('')
  return





















