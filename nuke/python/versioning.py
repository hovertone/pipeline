'''
Versioning of write nodes.
_Last Edit 03.02.2015
'''
# ==================== Need to be added to menu.py
#menubar = nuke.menu("Nuke");
#m = menubar.addMenu("&File")
#m.addCommand("Save &As...", "versioning.new_scriptSave()", "ctrl+S")
#m.addCommand("Save New &Version", "versioning.new_script_version_up()", "#+S")  
# ============================================================================

# ==================== Need to be added to init.py
#import versioning
# ============================================================================


import os.path, nuke, re, datetime
#from incrementalSave import incrementalSave

from CUF import isNumber
from nukescripts import script_version_up

# =====================================================================================

def findVersion(s):
	'''
	Returns whole number of version from provided path (if path has a v## in it; returns False if not), index of the first number in string and the last one


	Arguments (s)
		s - string form of path
	'''
	ln = len(s)
	oldIndexV = 0
	while s.find('v', oldIndexV) != -1:
		indexV = s.find('v', oldIndexV)
		if isNumber(s[indexV + 1]):
		    for i in range(indexV+1, ln):
		        #if nuke.ask(str(i) +  ' character ' + str(s[i]) + '\n' + 'i is '+ str(i) + ', ln is ' + str(ln)):
		        if not isNumber(s[i]) or i == ln - 1: 
		        	if '.' in os.path.split(s)[-1]: 
		        		ext = True
		        	else:
		        		ext = False

		        	if i == ln - 1:
		        		return s[indexV+1:i+1], indexV + 1, i, ext # returns whole number with padding, index of the first number in string and the last one, bool if path contains an extension
		        	else:
		        		return s[indexV+1:i], indexV + 1, i - 1, ext # returns whole number with padding, index of the first number in string and the last one, bool if path contains an extension
			    #else:
			       	#return

		else:
			oldIndexV = indexV + 1
	return False

# =====================================================================================

def addOhuIO(node):
	if node['beforeRender'].value() == "":
		node['beforeRender'].setValue("OhuIO.createOutDirMy( nuke.thisNode() )")

# =====================================================================================

def changeDaily(n):
    return
    # k = n['file']
	# path = k.value()
	# if re.match(r'.*[0-9]{2}.[0-9]{1,2}.[0-9]{1,2}.*', path) != None:
	# 	curDate = str(datetime.datetime.now())[2:10].replace('-', '.')
	# 	k.setValue(re.sub(r'[0-9]{2}.[0-9]{1,2}.[0-9]{1,2}', curDate, path))

# =====================================================================================

def changeWriteVersion():
	'''
	Changes versioning of all write nodes (if versioning exists in write node) dependent on version of the script

	Arguments ()
	'''
	scriptSave = os.path.split(nuke.root().knob('name').value())[-1]
	try:
		scriptVersion = findVersion(scriptSave)[0]
		for w in nuke.allNodes('Write'):
			if findVersion(w['file'].value()) != False and w['reading'].value() != True and 'prerender' not in w.name():
				w['file'].setValue(w['file'].value().replace('v' + findVersion(w['file'].value())[0], 'v' + scriptVersion))
				addOhuIO(w)
				changeDaily(w)
	except:
		pass

# =====================================================================================

def new_script_version_up():
	script_version_up()
	changeWriteVersion()
	nuke.scriptSave()

# =====================================================================================

def new_scriptSave():
	changeWriteVersion()	
	nuke.scriptSave()

 