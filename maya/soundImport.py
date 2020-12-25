import os
import maya.cmds as cmds
from p_utils.csv_parser_bak import projectDict

def main():
    try:
        shot = os.environ['SHOT']
        project = shot.split('/')[1]
        seq = shot.split('/')[3]
        sh = shot.split('/')[4]

        audioFolder = '%s/sound' % shot
        audioFile = sorted(os.listdir(audioFolder))[-1]

        soundNodes = cmds.ls(type='audio')
        if soundNodes != []:
            sd = cmds.ls(type='audio')[-1]

            if sd == audioFile.strip('.wav'):
                cmds.confirmDialog(message='Latest sound is already in this scene')
                return

        config = projectDict(project)
        shot_data = config.getAllShotData(seq=seq,
                                          shot=sh)


        audioPath = '%s/%s' % (audioFolder, audioFile)
        print 'audioPath %s\nff %s' % (audioPath, shot_data["first_frame"])
        cmds.sound(offset=shot_data["first_frame"], file=audioPath)
    except KeyError:
        cmds.confirmDialog(message='Not in pipeline')