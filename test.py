mpg = "X:/app/win/Pipeline/modules/ffmpeg/bin/ffmpeg"
sound = "P:/Raid/sequences/Delivery/sh010/sound/audio.wav"
fstart = "1001"
sequence_image = "P:/Raid/sequences/Delivery/sh010/comp/mainComp/precomp/forDaily/Delivery_sh010_forDaily.%04d.exr"
out_path = "D:/soundTest.mov"
cmd =  "//10.10.10.100/repository/app/win/Pipeline/modules/ffmpeg/bin/ffmpeg -threads 8 -r 24 -start_number 1001 -i C:/Users/Admin/Documents/maya/2019/temp/Raid-Delivery-sh010/Raid-Delivery-sh010-tempPlayblast.%04d.jpg -i  -i P:/Raid/sequences/Delivery/sh010/sound/audio.wav -vf -threads 8 -y -c:v libx264 -s 1920x1080 -r 24 -pix_fmt yuv420p -preset ultrafast -crf 23 P:/Raid/sequences/Delivery/sh010/out/allDailies/sh010_previz_v001_2021-03-02_17-09-41.mov"



import  subprocess as sp

cmd2 = mpg + " -start_number " + fstart + " -i " + sequence_image + " -i " + sound + " -c:v libx264 -preset slow -profile:v high -coder 1 -pix_fmt yuv420p -movflags +write_colr -bf 2 -bsf:v h264_metadata=video_full_range_flag=0 -crf 25 -framerate 24 " + out_path

sp.call(cmd)