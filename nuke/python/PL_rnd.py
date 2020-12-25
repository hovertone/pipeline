import os
import re
import nuke

def openNetworkShot():
	print os.environ['SHOT']

def getVars():
	pathSplitted = os.environ['SHOT'].split('/')
	print pathSplitted

def casualSave():
	curPath = nuke.root().name()
	lv = int(curPath.split('.')[-2].strip('v'))
	nv = int(curPath.split('.')[0].split('_')[-1].strip('v'))
	#print lv, nv

	getVars()

