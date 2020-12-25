import os
import nuke
import nukescripts

def createOutDir(file):
    dir = os.path.dirname(file)
    if not os.path.isdir(dir):
        if nuke.env['gui'] == True:
            if nuke.ask('Create directory?\n%s' % dir):
                os.makedirs(dir)
        else:
            print "dir made %s, no asks" % dir
            os.makedirs(dir)
            
def createOutDirMy(node):
    dir = os.path.dirname(node['file'].value())
    if not os.path.isdir(dir):
        if nuke.env['gui'] == True:
            if node['label'].value() == 'yes':
                os.makedirs(dir)
            else:
                if nuke.ask('Create directory?\n%s' % dir):
                    os.makedirs(dir)
        else:
            print "dir made %s, no asks" % dir
            os.makedirs(dir)
                
print "OhuIO imported"        
