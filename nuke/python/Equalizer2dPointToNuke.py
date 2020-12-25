'''
Equalizer 2D Point to Nuke Tracker node
__Last Edit 25.05.13

'''

import nuke, time
import os.path

def txtTodct(txtPath):
    '''
    Converts txt file to dctionary from provided .txt file
    dctionary looks like this:
        {'TrackerName': {'Frame': ('xpos', 'ypos'), '25': ('1152', '722'), '26': ('1163', '722')}}

    Arguments (txtPath)
        txtpath string type
    '''
    # Opening a .txt file and assigning it line by line to a variable
    try:
        f = open(txtPath, "r")
        try:
            # read all the lines into a list
            linesN = f.readlines()
        finally:
            f.close()
    except IOError:
        raise TypeError('Can not read file')

    # Removes all /n from each item of the list
    lines = []
    for l in linesN:
        lines.append(l.replace('\n', ''))

    # Gathering information of lines where the new tracker information begins
    firstLines = []
    for i in range(4, len(lines)):
        if len(lines[i]) > (len(lines[i-1])+2) and len(lines[i]) <= len(lines[i+1]):
            firstLines.append(i-3)

    lines.append('last')

    # Creating dctionary from the information above
    dct = {}
    for fl in firstLines:
        dct[lines[fl]] = {}
        i = fl + 3
        while True:
            dct[lines[fl]][lines[i].split()[0]] = (lines[i].split()[1], lines[i].split()[2])
            i += 1

            if len(lines[i]) + 2 < len(lines[i-1]):
                break

    return dct        

def createTracker(dct, ver, offset):
    '''
    Creates a tracker node with data from provided dctionary

    Arguments(dct, ver, offset)
        dct - dctionary type {'TrackerName': {'Frame': ('xpos', 'ypos'), '25': ('1152', '722'), '26': ('1163', '722')}}
        ver - integer type [3 | 4]
            3 - Maximum 4 trackers will be stored in tracker node
            4 - All of the trackers will be stored
        offset - integer type. Time offset

    '''
    # TRACKER 4
    if ver == 4:
        tr = nuke.createNode('Tracker4')
        tr['name'].setValue('3DEuqalizer_2D')

        for i in dct.keys():
            tr["add_track"].execute()

        # http://forums.thefoundry.co.uk/phpBB2/viewtopic.php?t=8130&sid=f5ab91f6ca6b188a858b32eae1af43ec
        k = tr['tracks'] 
        numColumns = 31 
        colTrackX = 2 
        colTrackY = 3 
        
        #loop through the all trackers in dctionary
        for trackeri in range(0, len(dct.keys())):
            trackIdx = trackeri
            k.setValue(1, numColumns*trackIdx + 6)
            k.setValue(1, numColumns*trackIdx + 7)
            k.setValue(1, numColumns*trackIdx + 8)
            # Loop throught all frames in each tracker from dct and assigning a xypos data to tracker node
            for frame in dct[dct.keys()[trackeri]]:
                k.setValueAt(float(dct[dct.keys()[trackeri]][frame][0]), int(frame) + offset, numColumns*trackIdx + colTrackX)
                k.setValueAt(float(dct[dct.keys()[trackeri]][frame][1]), int(frame) + offset, numColumns*trackIdx + colTrackY)

        tr['reference_frame'].setValue(nuke.frame())
        tr['transform'].setValue('match-move')

    elif ver == 3:
        tr = nuke.createNode('Tracker4')

        # If dctionary has more than 4 trackers nuke will proceed only 4 of them
        if len(dct.keys()) > 4:
            trackersAmount = 4
        else:
            trackersAmount = len(dct.keys())


        for i in range(trackersAmount):
            tr["add_track"].execute()

        # http://forums.thefoundry.co.uk/phpBB2/viewtopic.php?t=8130&sid=f5ab91f6ca6b188a858b32eae1af43ec
        k = tr['tracks'] 
        numColumns = 31 
        colTrackX = 2 
        colTrackY = 3            

        #loop through the all trackers in dctionary
        for trackeri in range(0, trackersAmount):
            trackIdx = trackeri
            k.setValue(1, numColumns*trackIdx + 6)
            k.setValue(1, numColumns*trackIdx + 7)
            k.setValue(1, numColumns*trackIdx + 8)
            # Loop throught all frames in each tracker from dct and assigning a xypos data to tracker node
            for frame in dct[dct.keys()[trackeri]]:
                k.setValueAt(float(dct[dct.keys()[trackeri]][frame][0]), int(frame) + offset, numColumns*trackIdx + colTrackX)
                k.setValueAt(float(dct[dct.keys()[trackeri]][frame][1]), int(frame) + offset, numColumns*trackIdx + colTrackY)

        tr['reference_frame'].setValue(nuke.frame())
        tr['transform'].setValue('match-move')

    else:
        nuke.message('Wrong version input')


def main(ver):
    '''
    Arguments(ver)
        ver [3 | 4]
            3 - Maximum 4 trackers will be stored in tracker node
            4 - All of the trackers will be stored

    '''
    # Searching for a default .txt file. And if it exists and was created less than 2 min ago then we will get the infomation from it
    for path in nuke.pluginPath():
        txtPath = path + '/Equalizer/EqualizerTemp2dPoints.txt'
        if os.path.exists(txtPath):
            if time.time() - os.path.getmtime(txtPath) < 120:
                noTxtFile = False
                break
        else:
            noTxtFile = True

    # If there is no default .txt file or it was modified long ago then lets get the file input
    if noTxtFile == True:
        txtPath = nuke.getFilename('Select 2D Points .txt file', '*.txt')

    # Parcing .txt path to make it dctionary to work with it further
    dct = txtTodct(txtPath)

    # Parcing dct data to create a tracker node.
    createTracker(dct, ver, nuke.root().firstFrame()-1)     # (dct of values, [tracker4 | tracker3 | transform], timeoffset)



