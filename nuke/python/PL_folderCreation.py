from utils.csv_parser import projectDict
import os

def main():
	rootFolders = ['assetBuilds',
						'assetBuilds/art',
							'assetBuilds/art/concept',
							'assetBuilds/art/src',
							'assetBuilds/art/in',
							'assetBuilds/art/out',
						'assetBuilds/footages',
						'assetBuilds/fx', 
						'assetBuilds/hdri', 
						'assetBuilds/char',
						'assetBuilds/props',
				   		'assetBuilds/env',
					'in', 
					'out', 
					'dailies', 
					'edit', 
						'edit/src', 
						'edit/sound', 
						'edit/prProj',
					'preproduction', 
						'preproduction/storyboard', 
						'preproduction/script', 
						'preproduction/prProj', 
						'preproduction/previz',
					'ref']
	shotFolders = [ 'anim', 
					'art',
					'cache', 
						'cache/anim', 
							'cache/anim/!cachename', 
						'cache/fx', 
							'cache/fx/!fxName', 
								'cache/fx/!cacheName/v001', 	
						'cache/cam', 
					'comp',
						'comp/precomp',
					'fx',
					'light',
					'render',
						'render/!layerName',
							'render/!layerName/v001']
	drive = 'P:'
	project = 'rnd'
	projectPath = '%s/%s' % (drive, project)

	pd = projectDict(project)

	for rf in rootFolders:
		folder = '/'.join([projectPath, rf])
		#print path
		if not os.path.exists(folder): os.makedirs(folder)

	for seq in pd.getSequences():
		for shot in pd.getShots(seq):
			for f in shotFolders:
				folder = '/'.join([projectPath, 'sequences', seq, shot, f])
				#print folder
				if not os.path.exists(folder): os.makedirs(folder)

main()