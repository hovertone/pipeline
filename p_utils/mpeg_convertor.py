




import subprocess


def check_resolution(file_path):
    mpg = "X:/app/win/Pipeline/modules/ffmpeg/bin/ffprobe"
    cmd = mpg + " -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 " + file_path
    return subprocess.check_output(cmd, shell=True)

def make_dailies(sequence):
    pass

