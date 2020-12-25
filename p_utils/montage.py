from moviepy.editor import *
import os, sys

sys.path.append("X:/app/win")



v1 = VideoFileClip(r"P:\Raid\sequences\xmas\sh005\out\DAILIES_sh005_comp.mov")
v2 = VideoFileClip(r"P:\Raid\sequences\xmas\sh010\out\DAILIES_sh010_comp.mov")
v = [v1, v2]

final_clip = concatenate_videoclips(v)
final_clip.to_videofile("D:/output.mp4", fps=24, remove_temp=False)