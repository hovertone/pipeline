###########################################################################################################
#
#  renderInc
#  
#  @author simon jokuschies
#  @version 1.0
#  @contact info@leafpictures.de
#  @website www.leafpictures.de/renderInc
#
#  description:
#  render out frame range with increment steps. Good for checking the overall animation of
#  the comp without having to render every frame, so that renderInc resutls in faster feedback. You have 2 methods:
#
#  increment: renders every Xth frame
#		options:
#			from: render from (default set to first frame in project settings)
#			to: render to (default set to last frame in project settings)
#			increment: render every Xth frame
#			auto read node: create read node from write after render is finished ("missing frames" mode set to nearest existing frame)
#
#  fill: render every frame which has not been rendered yet, mening fill in all non existent frames. Existing frames will be skipped
#		options:
#			auto read node: create read node from write after render is finished ("missing frames" mode set to nearest existing frame)
#
#  instalation:
#  put renderInc folder inside nuke home directory. In your int.py write (without the '#'):
#  import renderInc
#
##########################################################################################################

#no need to change anything from here. Edit only if you exactly know what you're doing.

import nuke
import os
import sys
import nukescripts

class RenderIncPanel(nukescripts.PythonPanel):

	'''
	RenderIncPanel
	'''
	def __init__( self ):
           
		nukescripts.PythonPanel.__init__(self, "renderInc", "renderInc")
		self.setMinimumSize(300,120)
    
		#elements
		self.method=nuke.Enumeration_Knob("method","method",["increment","fill"])
		self.start=nuke.String_Knob('from','from')
		self.start.setValue ( str (int ( nuke.root()["first_frame"].getValue() ) ) )
		self.to=nuke.String_Knob('to','to')
		self.to.setValue ( str (int( (nuke.root()["last_frame"].getValue() ) ) ) )
		self.increment=nuke.String_Knob('increment','increment')
		self.increment.setValue( "10" )
		self.autoRead = nuke.Boolean_Knob("auto read node","auto read node",1)
		self.autoRead.setFlag(nuke.STARTLINE)

		#add
		self.addKnob(self.method)
		self.addKnob(self.start)
		self.addKnob(self.to)
		self.addKnob(self.increment)
		self.addKnob(self.autoRead)

	def show( self ):
		'''
		action performed when pressed ok
		'''
		result = nukescripts.PythonPanel.showModalDialog(self)
        
		if result:
			incrementRender(int ( self.method.getValue() ) , int(self.start.getValue()), int(self.to.getValue()), int(self.increment.getValue()), int (self.autoRead.getValue()) )
			
	def knobChanged( self, knob ): 
		'''
		panel knob changed actions
		'''
		if knob.name() == "method":
			if knob.value()=="fill":
				self.start.setVisible(False)
				self.to.setVisible(False)
				self.increment.setVisible(False)
			else:
				self.start.setVisible(True)
				self.to.setVisible(True)
				self.increment.setVisible(True)

def incrementRender(method, start, to, increment, autoRead):
	'''
	increment render method and fill render method
	'''

	sel = nuke.selectedNode()

	#increment
	if method==0: 
		try:
			nuke.execute( sel, start, to , increment )
		except:
			nuke.message("error processing")
	#fill
	if method==1: 
		try:
			framesToRender=[]
			for frame in range ( int(nuke.root()["first_frame"].getValue()), int(nuke.root()["last_frame"].getValue() + 1) ):
				nuke.frame(frame)
				renderFrame=nuke.filename (sel, nuke.REPLACE)
				if not os.path.isfile(renderFrame):
					framesToRender.append(frame)
			rangeArr=[]
			for i in framesToRender:
				rangeArr.append([i,i,1])
			if len(framesToRender)>0:
				nuke.executeMultiple([sel], (rangeArr))
		except:
			pass

	#create autoRead
	if autoRead==1.0:
		#delete old read node if exists
		for node in nuke.allNodes():
			if node.name()=="autoRead_%s" % sel.name():
				nuke.delete(node)
		read = nuke.createNode("Read")
		read.setName("autoRead_%s" % sel.name())
		read.setXpos(int(sel["xpos"].getValue()))
		read.setYpos(int(sel["ypos"].getValue()+50))
		read["file"].setValue(sel["file"].getValue())
		read["first"].setValue(int(nuke.Root()['first_frame'].getValue() ))
		read["last"].setValue(int(nuke.Root()['last_frame'].getValue() ))
		read["origfirst"].setValue(int(nuke.Root()['first_frame'].getValue() ))
		read["origlast"].setValue(int(nuke.Root()['last_frame'].getValue() ))
		read["colorspace"].setValue(int(sel["colorspace"].getValue()))
		read["on_error"].setValue("nearest frame")
		read["reload"].execute

def renderInc():
	'''
	execute render Inc, create panel
	'''

	sel=None
	try:
		sel=nuke.selectedNode()
	except:
		return

	if sel.Class()=="Write":
		#check if render path is set
		if sel["file"].getValue() != "":
			RenderIncPanel().show()
		else:
			nuke.message("Please set a render location")

