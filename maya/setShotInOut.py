import os
import maya.cmds as cmds
from playblastWithRV import getPipelineAttrs
import functools
import random
import shutil

#from PL_scripts import inPipeline, getPipelineAttrs
#from p_utils.csv_parser_bak import projectDict

#setShotInOut.createUI(setShotInOut.applyCallback)

def main():
    shotEnv = os.environ['SHOT']
    shotEnvSplitted = shotEnv.split('/')
    drive = shotEnvSplitted[0]
    project = shotEnvSplitted[1]
    seq = shotEnvSplitted[3]
    shot = shotEnvSplitted[4]

    csv = open('%s/%s/project_config.csv' % (drive, project), "r")
    lines = []
    for line in csv:
        lines.append(line)

    seqSwitch = False
    indexInterest = 0
    for i, line in enumerate(lines):
        if seq in line:
            seqSwitch = True
        if seqSwitch:
            if shot in line:
                indexInterest = i
                break

    curLine = lines[indexInterest]
    curLineSplitted = curLine.split(',')
    csvIn = curLineSplitted[1]
    csvOut = curLineSplitted[2]

    print csvIn, csvOut

def createUI(pApplyCallback):
    if not getPipelineAttrs():
        cmds.deleteUI('setInOut')
        cmds.confirmDialog(message='Not a pipeline scene.')
        return
    else:
        drive, project, seq, shot, version = getPipelineAttrs()

    windowID = 'setInOut'
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    #########
    csv = open('%s/%s/project_config.csv' % (drive, project), "r")
    lines = []
    for line in csv:
        lines.append(line)

    csv.close()

    seqSwitch = False
    indexInterest = 0
    for i, line in enumerate(lines):
        if seq in line:
            seqSwitch = True
        if seqSwitch:
            if shot in line:
                indexInterest = i
                break

    curLine = lines[indexInterest]
    curLineSplitted = curLine.split(',')
    csvIn = curLineSplitted[1]
    csvOut = curLineSplitted[2]

    #########
    start = int(cmds.playbackOptions(q=True, min=True))
    end = int(cmds.playbackOptions(q=True, max=True))

    cmds.window(windowID, title='Set Frames', height=50, width=50, resizeToFitChildren=True, sizeable=False)
    cmds.columnLayout(adj=True, width=400)

    label = cmds.text(label = 'Old in and outs: %s - %s' % (csvIn, csvOut))
    valueField = cmds.textFieldGrp(l="Set new In and Out:", editable=True, text='%s - %s' % (start, end))

    okOptions = ['YES!', 'Tochnayak', 'To chto nado', 'Ebash!', 'Segodnya mne povezet']
    cmds.button(label=okOptions[random.randrange(len(okOptions))], command=functools.partial(pApplyCallback, valueField))

    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

    cmds.button(label='Cancel', command=cancelCallback)
    cmds.showWindow()

def applyCallback(pValueField, *pArgs):
    value = cmds.textFieldGrp(pValueField, q=True, text=True)
    #print value
    cmds.deleteUI('setInOut')

    dumpInOutToCSV(value)

def dumpInOutToCSV(pValue):
    start, end = pValue.strip(' ').split('-')

    if not getPipelineAttrs():
        cmds.deleteUI('setInOut')
        cmds.confirmDialog(message='Not a pipeline scene.')
        return
    else:
        drive, project, seq, shot, version = getPipelineAttrs()

    csvToDump = '%s/%s/project_config.csv' % (drive, project)

    #########
    csv = open('%s/%s/project_config.csv' % (drive, project), "r")
    lines = []
    for line in csv:
        lines.append(line)

    csv.close()

    seqSwitch = False
    indexInterest = 0
    for i, line in enumerate(lines):
        if seq in line:
            seqSwitch = True
        if seqSwitch:
            if shot in line:
                indexInterest = i
                break

    curLine = lines[indexInterest]
    curLineSplitted = curLine.split(',')
    csvIn = curLineSplitted[1]
    csvOut = curLineSplitted[2]

    newLine = curLine.replace(csvIn, start.strip(' '))
    newLine = newLine.replace(csvOut, end.strip(' '))
    #print newLine
    lines[indexInterest] = newLine

    # COPY BACK UP
    backupFolder = '%s/%s/temp/backup_csv' % (drive, project)
    shutil.copy2(csvToDump, 'P:/Arena/temp/backup_csv' + '/' + 'backup_csv_%s.csv' % str(len(os.listdir(backupFolder))+1).zfill(4))

    try:
        fh = open(csvToDump, "w")
        fh.writelines(lines)
        fh.close()

        cmds.confirmDialog(message="SUCCESS!\nVse srabotalo. Oficiant, shampanskogo!")
    except:
        cmds.confirmDialog(message="EBANA!\nSsanaya oshibka. Zovi san'ka")


# def proceedToMov(pValue):
#     start, end = pValue.strip(' ').split('-')
#     #setPrePlaybackAttrs()
#     drive, project, seq, shot, version = getPipelineAttrs()
#
#     shotPath = '%s/%s/sequences/%s/%s/out/allDailies/%s_v%s.mov' % (drive, project, seq, shot, shot, str(version).zfill(3))
#     shotFtrackPath = '%s/%s/sequences/%s/%s/out/DAILIES_%s.mov' % (drive, project, seq, shot, shot)
#     previzMontagePath = '%s/%s/preproduction/previz/out/%s_v%s.mov' % (drive, project, shot, str(version).zfill(3))
#
#     for i in (shotPath, shotFtrackPath, previzMontagePath):
#         #print i
#         if not os.path.exists(os.path.dirname(i)):
#             os.makedirs(os.path.dirname(i))
#             #print '%s folder created' % os.path.dirname(i)
#
#     try:
#         cmds.playblast(f=previzMontagePath, format='qt', percent=100, quality=90, width=1280, height=720, startTime = int(start), endTime = int(end), forceOverwrite=True)
#         shutil.copy2(previzMontagePath, shotFtrackPath)
#         shutil.copy2(previzMontagePath, shotPath)
#         cmds.confirmDialog(message='Daily done!\n%s' % shotFtrackPath.replace('/', '\\'))
#     except:
#         cmds.confirmDialog(message='SANEK NAPISAL KAKAYU-TO HUJNYU V CODE)))')

# sh = 'sh060'
# seq = 'SQA'
#
# csv = open('P:/Arena/project_config.csv', "r")
#
# lines = []
# for line in csv:
#     lines.append(line)
#
# seqSwitch = False
# for i, line in enumerate(csv):
#     if seq in line:
#         seqSwitch = True
#     if seqSwitch:
#         if sh in line:
#             # print i, line.strip('\n')
#             break
#
# lines[i] = 'afafaf'
# # print lines[i]
#
# fh = open('P:/Arena/project_config_test.csv', "w")
# fh.writelines(lines)
# fh.close()