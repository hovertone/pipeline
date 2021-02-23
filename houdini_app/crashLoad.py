import os
import getpass
import glob
import hou
import datetime
import time
import stat
import re

def main(save = True):
    usr = getpass.getuser()
    if usr == 'sashok': usr = 'Admin'
    my_local_machine_name = 'desktop-p247okt'
    houdini_local_folder = 'G:/houdini'
    temp = 'C:/Users/%s/AppData/Local/Temp/houdini_temp/' % usr
    files = list(filter(os.path.isfile, glob.glob(temp + "*.hip")))
    files.sort(key=lambda x: os.path.getmtime(x))
    print 'FILES %s' % str(files)
    last_file = files[-1]

    fileStatsObj = os.stat(last_file)
    modificationTime = time.ctime(fileStatsObj[stat.ST_MTIME])

    print os.path.getctime(last_file)
    print datetime.datetime.now()
    #res = hou.ui.displayMessage('Load %s?\nFrom %s' % (os.path.split(last_file)[-1], modificationTime), buttons=('Da, spasibo!', 'Net, ya peredumal(a)'))
    #if res == 0:
    print 'OPENING %s' % last_file
    hou.hipFile.load(last_file)


    # ZHEKIN SAVE UP CODE
    #print 'USER %s' % usr
    #print usr == 'p247okt'
    if save:
        if os.environ['COMPUTERNAME'].lower() == my_local_machine_name:
            if 'ASSETNAME' in os.environ.keys():
                path = '%s/underTheSea' % houdini_local_folder
            else:
                if 'FOLDER' in os.environ.keys():
                    path =  '%s/%s' % (houdini_local_folder, os.environ['FOLDER'])
                else:
                    print 'NO FOLDER ENV. DISSMIS'
                    return
        else:
            shot = os.environ["SHOT"]
            shotN = os.environ["SN"]
            assetName = os.environ["ASSETNAME"]
            assetType = os.environ["ASSETTYPE"]

            user = os.environ['COMPUTERNAME'].lower()

            if assetName == 'lookdev':
                print 'LOOKDEV'
                path = shot
                asset = shot.split('/')[-3]
            else:
                path = os.path.join(shot, assetType, assetName)

        scene_name = re.findall(r'(.+)_v(\d{3})', os.path.basename(hou.hipFile.name()))[0][0]
        if 'crash.' in scene_name:
            scene_name = scene_name.strip('crash.')
        #print 'SN'
        #print scene_name

        print 'PATH %s' % path
        all_files = [i for i in os.listdir(path) if scene_name in i]
        print 'all files %s' % all_files

        versions = []

        for f in all_files:
            if not "afanasy" in f:
                if ".hip" in f:
                    v = f.split(".")[0][-3:]
                    if v.isdigit() == True:
                        versions.append(int(v))

        versions = sorted(versions)
        #print 'VERSIONS %s' % versions
        up_version = str(versions[-1] + 1).zfill(3)
        #print 'LAST %s' % sorted(all_files)[-1]

        if os.environ['COMPUTERNAME'].lower() == my_local_machine_name:
            m = re.findall(r'_v(\d{3})', sorted(all_files)[-1])
            #print 'M0 %s' % m
            hip_name = sorted(all_files)[-1].replace(m[0], up_version)
            if '.hip_' in hip_name: hip_name = hip_name[:hip_name.find('.hip_')] + '.hip'
            full_path = os.path.join(path, hip_name).replace("\\", "/")
        else:
            if assetName == 'lookdev':
                hip_name = asset + "_lookdev_" + user + "_" + "v" + up_version + ".hip"
            else:
                hip_name = shotN + "_" + assetName + "_" + user + "_" + "v" + up_version + ".hip"

            full_path = os.path.join(path, hip_name).replace("\\", "/")

        print 'SAVING TO %s' % full_path
        hou.hipFile.save(full_path)

