print 'in movie maker'
import os
import subprocess
import csv_parser
from houdini_app.Loader import loader_preferences as prefs

class produce_daily(object):
    def __init__(self, sq, out_path, fps=24, resolution=[1920, 1080], comment=''):
        #pipe_root = os.environ['PIPELINE_ROOT']
        pipe_root = 'D:/my/git/pipeline'
        mpg = '%s/modules/ffmpeg/bin/ffmpeg' % pipe_root

        folder = os.path.dirname(sq)
        if not os.path.exists(folder):
            raise OSError("Sequence folder does not exist (%s)!" % (folder))

        # GETTING FIRST FRAME NUMBER
        split = sq.split('/')
        drive = prefs.LoaderPrefs().load()['storage']['projects']
        project = split[1]
        seq = split[3]
        shot = split[4]

        # GETTING FIRST FRAME
        csv = csv_parser.projectDict(project)
        ff = csv.getAllShotData(seq, shot)['first_frame']
        #print 'first frame %s' % ff

        # PROPER SEQUENCE SYNTAX CHECK
        if '%' in sq:
            #print 'percentage in sq'
            padd = sq[sq.find('%'):sq.find('%')+4]
        elif '#' in sq:
            #print 'hash in sq'
            padd = sq[sq.find('#'):sq.rfind('#')+1]
            newPadd = '%' + (str(len(padd)).zfill(2)) + 'd'
            sq = sq.replace(padd, newPadd)
            padd = newPadd
            #print 'SQWSQSS %s' % sq
        else:
            raise ValueError('SQ must contain #### or %04d type of syntax')

        # SQ FILES EXISTENCE CHECK
        print sq
        print padd, ff
        first_frame_path = sq.replace(padd, ff)
        if not os.path.exists(first_frame_path):
            raise OSError("First frame not exists (%s)!" % first_frame_path)

        # FIND LAST SOUND
        soundFolder = '%s/%s/sequences/%s/%s/sound' % (drive, project, seq, shot)
        last_tweak = 0
        if os.path.exists(soundFolder) and len(os.listdir(soundFolder)) > 0:
            for s in os.listdir(soundFolder):
                full_file_path = '%s/%s' % (soundFolder, s)
                #help(os.stat('%s/%s' % (soundFolder, s)))
                if os.stat(full_file_path).st_atime > last_tweak:
                    #soundExists = True
                    last_tweak = os.stat(full_file_path).st_atime
                    sound = '%s/%s' % (soundFolder, s)
            #print 'last modified file is %s' % most_recent
            sound_line = ' -i %s' % sound
        else:
            sound_line = ''
            print 'WARNING :: SOUND NOT FOUND'
            #soundExists = False

        #sound = 'P:/Raid/sequences/serenade/sh120/sound/audio.wav'
        #shotName = 'sh120'
        #s = '1001'

        # CMD FORMATING
        cmd = mpg + " -threads 8 -r " + str(fps) + sound_line + " -start_number " + ff + " -i " + sq + \
              ''' -vf "drawtext=fontfile=c\:/Windows/Fonts/courbd.ttf: \
              text=''' + shot + ''''       Frame\: %{eif\:n+1001\:d}'    ''' + comment + '''': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: \
                                    boxborderw=5: x=50: y=(h-text_h)-25" ''' + \
              " -threads 8 -y -c:v libx264 -s " + str('%sx%s' % (resolution[0], resolution[1])) + " -r " + str(fps) + " -pix_fmt " \
              "yuv420p -preset ultrafast -crf 23 " + out_path

        print 'CMD %s' % cmd

        result = subprocess.call(cmd, shell=True)
        if result==0:
            print 'Done!'
        else:
            raise ValueError('ERROR :: problem subproccess.call(cmd)')


if __name__ == '__main__':
    p = produce_daily(sq='P:/Raid/sequences/serenade/sh120/comp/mainComp/precomp/forDaily/serenade_sh120_forDaily.#####.exr', out_path='D:/temp/test_mov_v10.mov', resolution=[3200, 1800])