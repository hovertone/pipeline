import os
import shutil
from scripts import isNumber

def main():
	projectLabel = 'VIK SHORTS'
	project = 'vikingsShorts'
	configPath = "P:/%s/project_config.csv" % project
	hotboxAllPath = 'X:/app/win/nuke/hotbox/All'
	shotTemplate = 'X:/app/win/nuke/hotbox/All/_old/shotTemplate.py'

	file = open(configPath, "r")
	filedata = file.read()
	lines = filedata.split('\n')
	shotLines = [i.split(',')[0] for i in lines if 'sh_' in i]

	foldersList = sorted([i for i in os.listdir(hotboxAllPath) if '.' not in i and isNumber(i)])
	lastFolderNumber = int(foldersList[-1])
	#curFolderNumber = lastFolderNumber + 1
	curFolderNumber = 16
	curFolderPath = '%s/%s' % (hotboxAllPath, str(curFolderNumber).zfill(3))
	if not os.path.exists(curFolderPath): os.makedirs(curFolderPath)

	#JSON NAME
	with open('%s/_name.json' % curFolderPath, 'w') as f:
		f.write(projectLabel)

	# SHOT FILES 
	# for i, s in enumerate(shotLines):
	# 	s = s.strip('sh_')
	# 	targetFile = '%s/%s/%s.py' % (hotboxAllPath, str(curFolderNumber).zfill(3),str(i).zfill(3))
	# 	shutil.copy2(shotTemplate, targetFile)
	# 	f = open(targetFile, 'r')
	# 	lines = f.read().split('\n')
	# 	f.close()

	# 	# LABEL LINE REPLACING
	# 	lines[4] = lines[4].replace('000', str(s).zfill(3)).replace('vikingsPoker', project)
	# 	# SHOT LINE
	# 	lines[12] = lines[12].replace('000', str(s).zfill(3))
	# 	# PROJECT LINE
	# 	lines[13] = lines[13].replace('vikingsPoker', project)

	# 	data = '\n'.join(lines)
	# 	f = open(targetFile, 'w')
	# 	f.write(data)
	# 	f.close()

