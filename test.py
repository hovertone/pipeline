# coding=utf-8

import sys, os
path = os.environ['PIPELINE_ROOT'] + "/modules"
if not path in sys.path:
    sys.path.append(path)
    sys.path.append(path+"/moviepy")

import subprocess as sp
from modules.moviepy.editor import *

v1 = "P:/Raid/sequences/serenade/sh010/out/DAILIES_sh010_nosound.mp4"
sound = "P:/Raid/sequences/serenade/sh010/sound/sh010_sound_v001.wav"
out = "P:/Raid/sequences/serenade/sh010/out/DAILIES_sh010_sound.mp4"
sq = "P:/Raid/sequences/serenade/sh010/comp/mainComp/precomp/forDaily/serenade_sh010_forDaily.%04d.exr"



cmd = "X:/app/win/Pipeline/modules/ffmpeg/bin/ffmpeg -r 24 -start_number 1001 -i " + sq + " -r:a 24 -c:v libx264 -vf fps=24 -pix_fmt yuv420p -vsync 0 -y P:/Raid/sequences/serenade/sh010/out/DAILIES_sh010_nosound.mp4"
cmd2 = "X:/app/win/Pipeline/modules/ffmpeg/bin/ffmpeg -i " + v1 + " -i " + sound + " -c:v copy -c:a aac " + out

sp.call(cmd2)


#videoclip = VideoFileClip("P:/Raid/sequences/serenade/sh010/out/DAILIES_sh010_nosound.mp4")
#audioclip  = AudioFileClip("P:/Raid/sequences/serenade/sh010/sound/sh010_sound_v001.wav")
#new_audioclip = CompositeAudioClip([audioclip])
#videoclip.audio = audioclip


#videoclip.to_videofile("P:/Raid/sequences/serenade/sh010/out/DAILIES_sh010_sound.mp4")

#clip = VideoFileClip("P:/Raid/sequences/serenade/sh010/out/DAILIES_sh010_sound.mp4")

#final = concatenate_videoclips([clip])
#final.to_videofile("D:/AZAZA.mp4", fps=25, remove_temp=False, temp_audiofile=os.path.expanduser("~")+"/montage_temp.wav")

