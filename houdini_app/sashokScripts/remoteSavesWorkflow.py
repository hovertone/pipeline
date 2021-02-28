import getpass
import os
import hou
import socket

print 'of remote saves workflow'

# import ctypes, os
#
# def isAdmin():
#     try:
#         is_admin = (os.getuid() == 0)
#     except AttributeError:
#         is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
#     return is_admin
#
# if isAdmin():
#     print("Admin! Oh yeah!")
# else:
#     print("Just a mortal!")


class basic_workflow:
    def __init__(self):
        self.local = 'sanka'
        self.workst = 'sashok'
        self.local_host = 'desktop-p247okt'
        self.workst_host = 'sashok'
        self.local_drive = 'G:'
        self.netw_drive = 'P:'

    def weLocal(self):
        usr = getpass.getuser()
        host = socket.gethostname()
        # if usr == self.local:
        #     return True
        # else:
        #     return True

        if host == self.local_host:
            return True
        else:
            return True

    def check_for_last_version(self, folder):


        if os.path.exists(folder):
            all_files = os.listdir(folder)
            versions = []
            if len(all_files) == 0:
                return '000', '001'
            for f in all_files:
                if not "afanasy" in f:
                    if ".hip" in f:
                        v = f.split(".")[0][-3:]
                        if v.isdigit() == True:
                            versions.append(int(v))

                            versions = sorted(versions)
                            last_version = str(versions[-1]).zfill(3)
                            next_version = str(versions[-1]+1).zfill(3)

                            return last_version, next_version
        else:
            print 'there is no folder %s\ncreting it' % folder
            os.makedirs(folder)
            return '000', '001'

    def saveLocaly(self):
        print 'in save localy'
        if self.weLocal():
            print 'from home'
            if self.netw_drive in hou.hipFile.path(): #
                if hou.ui.displayMessage("Want to resave localy?", buttons=("Yes", "No")) == 0:
                    spl = os.environ['SHOT'].split('/')
                    project = spl[1]
                    seq = spl[3]
                    shot = spl[4]
                    assetname = os.environ['ASSETNAME']

                    local_hip_folder = '%s/%s/sequences/%s/%s' % (self.local_drive, project, seq, shot)
                    print 'local hip folder %s' % local_hip_folder
                    lv, nv = self.check_for_last_version(local_hip_folder)

                    local_hip_file = '%s_%s_%s_v%s.hip' % (shot, assetname, self.workst_host, nv)
                    local_hip_filepath = '%s/%s' % (local_hip_folder, local_hip_file)

                    print 'local hip filePATH %s' % local_hip_filepath

                    hou.hipFile.save(local_hip_filepath)
        else:
            print 'from work'

    def saveToWork(self):
        if self.weLocal():
            print 'from home'
            if self.local_drive in hou.hipFile.path(): #
                if hou.ui.displayMessage("Want to resave to work network?", buttons=("Yes", "No")) == 0:
                    spl = os.environ['SHOT'].split('/')
                    project = spl[1]
                    seq = spl[3]
                    shot = spl[4]
                    assetname = os.environ['ASSETNAME']

                    netw_hip_folder = '%s/%s/sequences/%s/%s' % (self.netw_drive, project, seq, shot)
                    #print 'local hip folder %s' % local_hip_folder
                    lv, nv = self.check_for_last_version(netw_hip_folder)

                    netw_hip_file = '%s_%s_%s_v%s.hip' % (shot, assetname, self.workst_host, nv)
                    netw_hip_filepath = '%s/%s' % (netw_hip_folder, netw_hip_file)

                    print 'local hip filePATH %s' % netw_hip_filepath

                    hou.hipFile.save(netw_hip_filepath)
        else:
            print 'from work'

if __name__ == '__main__':
    bw = basic_workflow()
    bw.saveLocaly()


