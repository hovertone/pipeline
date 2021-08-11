#
# CSV_DICT = {'Poker': [sh_010, sh_020],
#             'Shorts': [sh_222, sh_333]}
#
# SHOT_DICT = {'name':'sh_010',
#              'first_frame':1001,
#              'last_frame':1100,
#              'preroll':50}
import os
import shutil
from time import gmtime, strftime


class projectDict(object):
    def __init__(self, project, dr=None):
        self.d = dict()
        self.project = project

        if not dr:
            self.drive = 'P:'
        else:
           self.drive = dr

        self.csvpath = "%s/%s/project_config.csv" % (self.drive, project)
        if not os.path.exists(self.csvpath):
            self.project_exists = False
            print 'There is no CSV file in %s project on %s drive' % (project, self.drive)
            return
        else:
            self.project_exists = True
            self.fillDictVar()

    def fillDictVar(self):
        #print 'Filling dict var'
        file = open(self.csvpath, 'r')
        filedata = file.read()
        lines = filedata.split('\n')
        lines = [i.strip('\r') for i in lines]
        #print 'lines ' + str(lines)

        for l in lines:
            if l == "":
                pass
            else:
                if 'seq' in l:
                    seq = l.split(' ')[-1].strip(' ')
                    #print 'afafasff' + seq
                    if seq not in self.d.keys():
                        self.d[seq] = list()
                else:
                    line_splitted = l.split(',')
                    sh_d = dict()
                    sh_d['name'] = line_splitted[0]
                    sh_d['first_frame'] = line_splitted[1]
                    sh_d['last_frame'] = line_splitted[2]
                    sh_d['preroll'] = line_splitted[3]
                    self.d[seq].append(sh_d)

        # for i in self.d.keys():
        #     print self.d[i]
    def getSequences(self):
        if not self.project_exists:
            print "ERROR :: Project does not exists"
            return

        return self.d.keys()

    def getShots(self, seq):
        if not self.project_exists:
            print "ERROR :: Project does not exists"
            return

        shotsList = list()
        shotsData = self.d[seq]
        #print "DATA CSV", self.d
        for i in shotsData:
            #print "I", i
            shotsList.append(i['name'])
        return shotsList

    def getAllShotData(self, seq, shot):
        if seq not in self.d.keys():
            print '%s seq does not exist' % seq
            return
        if shot not in [i['name'] for i in self.d[seq]]:
            print 'there is no %s shot in %s seq' % (shot, seq)
            return

        shots = self.d[seq]
        shotData = [i for i in shots if i['name'] == shot]
        if len(shotData) != 1:
            print 'Some shit happens. Call the POLICE!'
            return
        return shotData[0]

    def getSpecificShotData(self, seq, shot, key):
        #print 'test %s %s %s' % (seq, shot, key)
        shots = self.d[seq]
        #print shots
        shotData = [i for i in shots if i['name'] == shot]
        return shotData[0][key]

    def getDict(self):
        return self.d

    def addSequence(self, seq):
        if seq in self.d.keys():
            print '%s seq already exists' % seq
        else:
            self.d[seq] = list()

    def addShot(self, seq, shot_name, first_frame='1001', last_frame='1050', preroll='10'):
        if seq not in self.d.keys():
            print 'ERROR :: There is no %s seq in dict' % seq
            return
        elif shot_name in [i['name'] for i in self.d[seq]]:
            print 'ERROR :: Shot %s already exists' % shot_name
            for sh in self.d[seq]:
                #print 'FOR %s' % str(sh)
                if sh['name'] == shot_name:
                    #print 'GOT IT'
                    sh['first_frame'] = first_frame
                    sh['last_frame'] = last_frame
                    sh['preroll'] = preroll
                    break
            return
        elif 'sh' not in shot_name:
            print 'ERROR :: "sh" should be in shot name'
            return
        else:
            shot_d = dict()
            shot_d['name'] = shot_name
            shot_d['first_frame'] = first_frame
            shot_d['last_frame'] = last_frame
            shot_d['preroll'] = preroll
            self.d[seq].append(shot_d)

            print 'Shot %s added to %s seq' % (shot_name, seq)

    def setSpecificShotData(self, seq, shot, data, value):
        if seq not in self.d.keys():
            print 'ERROR :: There is no %s seq in dict' % seq
            return
        elif shot not in self.getShots(seq):
            print 'ERROR :: There is no %s shot in %s seq' % (shot, seq)
            return
        else:
            self.backupCSV()
            for s in self.d[seq]:
                if s['name'] == shot:
                    s[data] = value
                    break
            self.update_proj()



    def writeCSV(self):
        print 'Begining to write CSV...'
        if self.project_exists:
            self.backupCSV()

        folder = os.path.split(self.csvpath)[0]
        if not os.path.exists(folder):
            os.makedirs(folder)

        data_lines = []
        csv = open(self.csvpath, "w")
        for seq in sorted(self.d.keys()):
            sq = "seq " + seq + "\n"
            data_lines.append(sq)
            for shot in self.d[seq]:
                shot_name = str(shot['name'])
                line = ",".join([shot_name, shot["first_frame"], shot["last_frame"], shot["preroll"] + "\n"])
                data_lines.append(line)

        # LAST EMPTY LINE FIX
        if '\n' in data_lines[-1]:
            data_lines[-1] = data_lines[-1].strip('\n')

        csv.writelines(data_lines)
        csv.close()

    def backupCSV(self):
        temp_folder = '%s/%s/temp/CSV_backups' % (self.drive, self.project)
        if not os.path.exists(temp_folder): os.makedirs(temp_folder)
        curTime = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        temp_file = 'project_config_%s.csv' % curTime
        shutil.copy2(self.csvpath, '%s/%s' % (temp_folder, temp_file))
        print 'Backuped %s/%s' % (temp_folder, temp_file)

    def print_dict(self):
        print 'PROJECT: %s' % self.project
        for seq in sorted(self.d.keys()):
            print '\tSEQ: %s' % seq
            for shot in self.d[seq]:
                print '\t\tSH %s:' % shot['name']
                print '\t\t\t first_frame: %s' % shot['first_frame']
                print '\t\t\t last_frame: %s' % shot['last_frame']
                print '\t\t\t preroll: %s' % shot['preroll']

    def folders_routine(self):
        rootFolders = ['assetBuilds',
                       'assetBuilds/art',
                       'assetBuilds/art/concept',
                       'assetBuilds/art/src',
                       'assetBuilds/art/in',
                       'assetBuilds/art/out',
                       'assetBuilds/footages',
                       'assetBuilds/fx',
                       'assetBuilds/hdri',
                       'assetBuilds/char',
                       'assetBuilds/props',
                       'assetBuilds/env',
                       'in',
                       'out',
                       'dailies',
                       'edit',
                       'edit/src',
                       'edit/sound',
                       'edit/prProj',
                       'preproduction',
                       'preproduction/storyboard',
                       'preproduction/script',
                       'preproduction/prProj',
                       'preproduction/previz',
                       'ref']
        shotFolders = ['animation',
                       'src',
                       'track',
                       'art',
                       'cache',
                       'cache/anim',
                       'cache/anim/!cachename',
                       'cache/fx',
                       'cache/fx/!fxName',
                       'cache/fx/!cacheName/v001',
                       'cache/cam',
                       'comp',
                       'fx',
                       'light',
                       'render',
                       'render/!layerName',
                       'render/!layerName/v001']

        ###############################################

        drive = self.drive
        project = self.project
        projectPath = os.path.join(drive, project)

        for rf in rootFolders:
            folder = '/'.join([projectPath, rf])
            # print path
            if not os.path.exists(folder): os.makedirs(folder)

        for seq in self.d.keys():
            for shot in [i['name'] for i in self.d[seq]]:
                for f in shotFolders:
                    folder = '/'.join([projectPath, 'sequences', seq, shot, f])
                    # print folder
                    if not os.path.exists(folder): os.makedirs(folder)

    def update_proj(self):
        self.writeCSV()
        self.folders_routine()

    def __repr__(self):
        print str(self.d)

if __name__ == '__main__':
    # CREATE NEW PROJ
    proj_name = 'Raid'
    projD = projectDict(proj_name)
    #
    # print 'All shot data'
    # print projD.getAllShotData('BGN', 'sh040')

    # projD.addSequence('BGN')
    # for s in range(8, 22):
    #     projD.addShot(seq='BGN', shot_name='sh%s' % str(s*10).zfill(3))
    #
    # projD.update_proj()

    # print 'SEQs'
    # print projD.getSequences()
    #
    # print 'SHOTs'
    # print projD.getShots('BGN')

    # projD.addShot('angerManagement', 'sh010', '1001', '1031', '10')
    # projD.print_dict()
    # projD.update_proj()

    # projD.setSpecificShotData('serenade', 'sh010', 'first_frame', '1001')
    print projD.getSpecificShotData('serenade', 'sh040', 'first_frame')

