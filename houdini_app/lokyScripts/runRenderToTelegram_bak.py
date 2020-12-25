#print "aaaa"

import sys, hou

from telega import telegramReport
node = hou.pwd()
lastFrame = int(hou.parm(node.path()+"/f2").eval())
if int(hou.frame()) == lastFrame:
	path = "X:/app/win/Pipeline"
	if not path in sys.path:
		sys.path.append(path)
	from houdini_app.lokyScripts import houdiniTelegram
	reload(houdiniTelegram)
	a = houdiniTelegram.telegramRenderPath()
	telegramReport(filePath = a[0], tp = 'render', args = [a[1], a[2]])