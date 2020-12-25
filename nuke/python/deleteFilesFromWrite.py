import os
from nukescripts import replaceHashes
import nuke

def deleteFilesFromWritePath(node):
	if node.Class() != 'Write' and node.Class() != 'Read': 
		print 'Wrong node provided'
		return
	else:
		fullPath = node['file'].value()
		folder, file = os.path.split(fullPath)
		file = replaceHashes(file)
		fileNameToFind = file[:file.find('%')]
		fileNameExt = file[file.rfind('.'):]
		print '# Deleting:'
		totalCount = len(os.listdir(folder))
		try:
			for f in os.listdir(folder):
				if fileNameToFind in f and fileNameExt in f:
					file = os.path.join(folder, f).replace('\\', '/')
					os.remove(file)
					print '\t%s' % file

			nuke.message('%s files removed' % str(totalCount))
		except Exception as e:
			nuke.message(str(e))