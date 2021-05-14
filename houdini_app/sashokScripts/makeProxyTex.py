import hou
import os
import subprocess as sp

def main():
    pipe_root = os.environ['PIPELINE_ROOT'].replace('\\', '/')
    mpg = '%s/modules/ffmpeg/bin/ffmpeg' % pipe_root

    nodes = hou.selectedNodes()
    for n in nodes:
        if n.type().name()=='arnold::image':
            filepath = n.parm('filename').eval()
            folder, file = os.path.split(filepath)
            pat = file[:file.index('<') - 1]
            ext = os.path.splitext(file)[-1]
            proxy_folder = '%s/proxy' % folder
            if not os.path.exists(proxy_folder): os.makedirs(proxy_folder)
            if ext == '.tx':
                for f in os.listdir(folder):
                    if pat in f and f[f.rfind('.'):] != '.tx':
                        ext = f[f.rfind('.'):]
                        break

            if '<UDIM>' in file:
                udims = list()
                for f in os.listdir(folder):
                    if pat in f:
                        udim = f[f.index('.')+1:f.index('.')+5]
                        if udim not in udims:
                            udims.append(udim)

                for u in udims:
                    file = '%s.%s%s' % (pat, u, ext)
                    proxy_file = '%s_proxy.%s.%s' % (pat, u, 'jpg')
                    cmd = 'X:/app/win/ffmpeg/bin/ffmpeg -i ' + folder + '/' + file + ' -n -s 512x512 ' + proxy_folder + '/' + proxy_file
                    #print 'cmd %s' % cmd
                    sp.call(cmd, shell=True)