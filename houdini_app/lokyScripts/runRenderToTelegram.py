#print "aaaa"

import sys, hou

if not hou.isUIAvailable():
	node = hou.pwd()
	lastFrame = int(hou.parm(node.path()+"/f2").eval())
	if int(hou.frame()) == lastFrame:
		path = "X:/app/win/Pipeline/p_utils"
		if not path in sys.path:
			sys.path.append(path)
		import telega
		reload(telega)
		a = telega.telegramRenderPath()
		print 'args are %s' % str(a)
		telega.telegramReport(filePath = a[0], tp = 'render', args = [a[1], a[2], a[3]])
else:
	pass
	# DEV
	# from p_utils import telega
	# reload(telega)
	# a = telega.telegramRenderPath()
	# print 'args are %s' % str(a)
	# telega.telegramReport(filePath=a[0], tp='render', args=[a[1], a[2], a[3]])