import os.path, nuke
from CUF import isNumber
import re

def getPadding(path):
    '''
    Takes path to a file and returns a padding itselft and first and last index of padding 

    Arguments (path)
        path - path to a file. String format
    '''

    if '#' in path:
        firstDigit = path.find('#')
        lastDigit = path.rfind('#')

        return path[firstDigit:lastDigit+1], firstDigit, lastDigit
    elif '%' in path:
        firstDigit = path.find('%')
        lastDigit = path.rfind('%') + 3

        return path[firstDigit:lastDigit+1], firstDigit, lastDigit
    else:

        ln = len(path)
        # if path contains {}
        if re.search(r'[\._-]*\d+\.\w{3,4}$', os.path.split(path)[-1]):
            # Loops through each character of the string and breaks on a first non-numeric symbol from the end
            for i in range(5, ln + 1):
                if not isNumber(path[i*-1]): break

            return path[i*-1+1: -4], i*-1+1, -5 # padding number, index of the first number of padding, index of the last number of padding
        else:
            return False

def getSequenceRange(path):
    folder = os.path.split(path)[0] + '/'
    try:
        files = sorted(os.listdir(folder))
    except WindowsError:
        return False

    getPaddingResult = getPadding(path)
    filename = os.path.split(path[:getPaddingResult[1]-1])[1]
    paddingNumber = getPaddingResult[0]

    for f in files:
        if re.search(r'.*[\_\.]*\d+\.\w{3,4}$', f):
            pass
        else:
            files.pop(files.index(f))

    return int(getPadding(files[0])[0]), int(getPadding(files[-1])[0])


def createReadFromWrite():
    w = nuke.thisNode()
    if getSequenceRange(w['file'].value()) == False:
        nuke.message('There no such path (folder empty)')
        del(w)
        return

    if nuke.thisNode().Class() == 'Write':
        r = nuke.createNode('Read')
        r.setXYpos(w.xpos(), w.ypos() + 72)
        knobs = ['file', 'colorspace']
        for k in knobs:
            r[k].setValue(w[k].value())
            if k == 'file':
                if getPadding(r[k].value()) != False:
                    r['first'].setValue(getSequenceRange(w[k].value())[0])
                    r['last'].setValue(getSequenceRange(w[k].value())[1])
                else:
                    w[k].setValue(r[k].value())