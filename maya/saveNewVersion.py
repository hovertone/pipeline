import maya.cmds as cmds
import os
import re

class save(object):
    def __init__(self):
        self.curName = cmds.file(query=True, sn=True)
        folder, scriptName = os.path.split(self.curName)
        #print folder, scriptName

        try:
            self.match = re.match(r'(.*)_v(\d{3})', scriptName)
        except:
            cmds.confirmDialog(message='Something is wrong with scene filename.')
            return

        self.name = self.match.group(1)
        self.version = int(self.match.group(2))

        similarFiles = sorted([i for i in os.listdir(folder) if self.name in i])
        newestFile = similarFiles[-1]
        self.newestFileVersion = int(re.match(r'(.*)_v(\d{3})', newestFile).group(2))

        if self.newestFileVersion > self.version:
            self.saveVersion(self.newestFileVersion + 1)
        else:
            self.saveVersion(self.version + 1)

    def saveVersion(self, ver):
        saveName = self.curName.replace('_v%s' % str(self.version).zfill(3), '_v%s' % str(ver).zfill(3))
        #print saveName
        cmds.file(rename= saveName)
        cmds.file(save=True, type="mayaBinary")
        print 'Saved to %s' % saveName