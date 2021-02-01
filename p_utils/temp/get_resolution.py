import subprocess as sp
import sys
import os

def main():
    pipe_root = os.environ['PIPELINE_ROOT'].replace('\\', '/')
    probe = '%s/modules/ffmpeg/bin/ffprobe' % pipe_root
    file_path = "D:/my/progress_bar_tests/start/v001/sh010_floor_v005.1001.exr"
    cmd = '%s -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 %s' % (probe, file_path)
    arg = '-v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 %s' % file_path

    print cmd
    #res = sp.call(cmd, shell=True)
    #print 'RES %s' % res
    p = sp.check_output(cmd)
    #p.help()

    #output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    #rc = p.returncode
    print 'P %s' % str(p)

if __name__ == '__main__':
    main()