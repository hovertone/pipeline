# CompactRenamer v1.0
# License: MIT Licence (See LICENSE.txt or https://choosealicense.com/licenses/mit/)
# Copyright (c) 2017 Erik Lehmann
# Date: 08/21/17
#
# Description: 
#	Rename selected object(s). 
#
# How to use:
#	1. Select object(s).
#   2. Choose operation (Prefix, Name, Suffix or execute All operations)
#   3. Enter text in the corresponding fields.
#   4. Run "Ren".
#	5. Search & Replace:
#		- When "Name" or "All" is selected
#		- Type '>>' in the "Name" field
#		- Type what you 'Search' in the "Prefix" field
#		- Type the 'Replacement' in the "Suffix" field
#		- Run "Ren"
#
# Installation: 
# 	1. 	Copy CompactRenamer.py to '\[USER]\Documents\maya\[MAYAVERSION]\prefs\scripts'
# 	2. 	Launch / Restart Maya
#	3.	Type into Script Editor (Python tab) and execute:
#       import CompactRenamer as ComRen
#       MCCR = ComRen.MainClassCompactRenamer()
#       MCCR.comRenUI()


import maya.cmds as cmds
import sys

class MainClassCompactRenamer:

	def __init__(self):
		self.comRenList = []
		self.comRenPadding = 3

	def comRenUI(self, _=False):

		# C H E C K  W I N D O W
										
		if (cmds.window("comRenWin", exists=True)):
			cmds.deleteUI("comRenWin", wnd=True)
			cmds.windowPref("comRenWin", r=True)

			
		# U I

		cmds.window("comRenWin", s=False, tlb=True, rtf=True, t="Compact Renamer")

		cmds.columnLayout(adj=True)


        # R A D I O  B U T T O N S
        
		cmds.rowLayout(numberOfColumns=5, columnWidth5=(100,150,50,100,50))

		comRenRC = cmds.radioCollection()
		cmds.radioButton('comRenPreRB', l="Prefix", cl=comRenRC)
		cmds.radioButton('comRenNamRB', l="Name", cl=comRenRC)
		cmds.text("Pad", align='left')
		cmds.radioButton('comRenSufRB', l="Suffix", cl=comRenRC)	
		cmds.radioButton('comRenAllRB', l="All", cl=comRenRC, select=True)

		cmds.setParent("..")


		# T E X T  F I E L D S

		cmds.rowLayout(numberOfColumns=5)

		cmds.textField("tFcR_Prefix", height=30, width=100)
		cmds.textField("tFcR_Name", height=30, width=150)
		cmds.optionMenu(cc = self.changePaddingMenuItem, w=50, h=28, ebg=False, bgc=(0.18, 0.18, 0.18))
		cmds.menuItem(l="3")
		cmds.menuItem(l="2", ia="")
		cmds.menuItem(l="1", ia="")				
		cmds.menuItem(l="4")
		cmds.menuItem(l="5")
		cmds.menuItem(l="6")
		cmds.menuItem(l="7")
		cmds.menuItem(l="8")
		cmds.menuItem(l="9")
		cmds.textField("tFcR_Suffix", height=30, width=100)
		cmds.button(l="Ren", bgc=(0.24, 0.72, 0.46), ebg=False, height=30, width=50, c = self.comRenRename)

		cmds.setParent("..")

		
		# S H O W  W I N D O W
		
		cmds.showWindow("comRenWin")



    # M E T H O D S
    
    # P R E F I X
    
	def comRenPrefix(self, _=False):
		comRenPreText = cmds.textField("tFcR_Prefix", q=True, text=True)
		for i in self.comRenList:
			cmds.rename(i, '%s%s' % (comRenPreText, i))


    # C H A N G E  P A D D I N G
    
	def changePaddingMenuItem(self, comRenMenuItem):
		self.comRenPadding = comRenMenuItem


	# N A M E  /  P A D D I N G  /  S E A R C H  A N D  R E P L A C E
    
	def comRenName(self, _=False):
		comRenCounter = 1
		comRenLine = ""
		comRenNameText = cmds.textField("tFcR_Name", q=True, text=True)
		
		if comRenNameText == ">>":
		    comRenSearch = cmds.textField("tFcR_Prefix", q=True, text=True)
		    comRenReplace = cmds.textField("tFcR_Suffix", q=True, text=True)
		    try:
				for i in self.comRenList:
					if "%s" % comRenSearch in i:
						comRenLine = i.split('|')[-1]
						comRenNewText = comRenLine.replace("%s" % comRenSearch, "%s" % comRenReplace)
						cmds.rename(i, '%s' % comRenNewText) 	
				sys.exit()
		        
		    except:
		        sys.exit()
		        
		elif len(self.comRenList) == 1:
		    cmds.rename(self.comRenList[0], '%s' % comRenNameText)
		
		else:
			try:
				for i in self.comRenList:
					comRenPadValue = ("%%0%si" % self.comRenPadding) % int(comRenCounter)
					cmds.rename(i, '%s%s' % (comRenNameText, comRenPadValue))
					comRenCounter += 1
      
			except:
				pass                               

	# S U F F I X
    
	def comRenSuffix(self, _=False):
		comRenSufText = cmds.textField("tFcR_Suffix", q=True, text=True)
		for i in self.comRenList:
			cmds.rename(i, '%s%s' % (i, comRenSufText))

    # R E O R D E R
    
	def comRenReorder(self, _=False):
		self.comRenList = cmds.ls(sl=True)

		sorted(self.comRenList)
		for i in reversed(self.comRenList):
			cmds.reorder(i, front=True)

	# R E N A M E

	def comRenRename(self, _=False):
        
		self.comRenList = cmds.ls(sl=True)
   
		if len(self.comRenList) == 0:
			print "Select Object(s)."
			sys.exit()
		else:
			pass
		    
		if cmds.radioButton('comRenPreRB', q=True, select=True):
			self.comRenPrefix()

		if cmds.radioButton('comRenNamRB', q=True, select=True):
			self.comRenName()
			self.comRenReorder()
			
		if cmds.radioButton('comRenSufRB', q=True, select=True):
			self.comRenSuffix()

		if cmds.radioButton('comRenAllRB', q=True, select=True):
			self.comRenName()
			self.comRenList = cmds.ls(sl=True)
			self.comRenPrefix()
			self.comRenList = cmds.ls(sl=True)
			self.comRenSuffix()
			self.comRenReorder()    
        
#MCCR = MainClassCompactRenamer()
#MCCR.comRenUI()