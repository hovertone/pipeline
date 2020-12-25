try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os
import hou
import shutil

def main(src, dest, paths, tx = False, nonTx = False):
    shop = hou.node('/obj/ElvenFemale_Shading6/geometry/ElvenFemale_Shader1/shopnet1')
    pp = []
    for p in paths:
        oldVal = p
        # print '\t%s' % oldVal
        if '<UDIM>' in oldVal:
            pp.append(oldVal[:oldVal.find('<UDIM>')])
        else:
            pp.append(oldVal)

    print 'PP'
    for i, p in enumerate(sorted(pp)):
        print '%s :: %s' % (i, p)

    toCopy = list()
    for rootDir, subdirs, filenames in os.walk(src):
        if filenames:
            for f in filenames:
                fullPath = '%s/%s' % (rootDir, f)
                fullPath = fullPath.replace('\\', '/')
                for p in pp:
                    if p in fullPath:
                        # print "MATCH"
                        # print '\t' + p + '\n\t' + fullPath
                        toCopy.append(fullPath)
                        break

    print 'TO COPY'
    for tc in toCopy:
        print tc

    print 'starting to copy...'

    # Create an interruptable operation.
    operation = hou.InterruptableOperation('Doing Work', long_operation_name ='Starting Tasks', open_interrupt_dialog = True)
    operation.__enter__()


    counter = 0
    num_tasks = len(toCopy)
    print '%s in total' % num_tasks
    for i, tc in enumerate(toCopy):
        percent = float(i) / float(num_tasks)
        destPath = tc.replace(src, dest)
        try:
            operation.updateLongProgress(percent, '%s' % destPath)
        except hou.OperationInterrupted:
            print 'ABORTED BY USER'
            operation.__exit__(None, None, None)
            return # EXIT

        ext = []
        if tx: ext.append('.tx')
        if nonTx: ext += ['.exr', '.jpg', '.png', '.tga', '.tif']

        for e in ext:
            if e in destPath:
                folder = os.path.dirname(destPath)
                if not os.path.exists(folder):
                    os.makedirs(folder)

                if os.path.exists(destPath):
                    print 'LOCATED :: %s' % destPath
                else:
                    print 'MISSING :: %s' % destPath

                    try:
                        shutil.copy2(tc, destPath)
                        pass
                    except Exception as e:
                        # print 'FOUND :: %s' % tc
                        # print 'DEST :: %s' % destPath
                        print(e)



    # Stop the operation. This closes the progress bar dialog.
    operation.__exit__(None, None, None)

