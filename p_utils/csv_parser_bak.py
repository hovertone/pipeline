#
# CSV_DICT = {'Poker': [SH_010, SH_020],
#             'Shorts': [SH_222, SH_333]}
#
# SHOT_DICT = {'name':'SH_010',
#              'first_frame':1001,
#              'last_frame':1100,
#              'preroll':50}


class projectDict(object):
    def __init__(self, project, dr=None):
        if not dr:
            drive = 'P:'
        else:
            drive = dr
        csvpath = "%s/%s/project_config.csv" % (drive, project)
        file = open(csvpath, 'r')
        filedata = file.read()
        lines = filedata.split('\n')
        lines = [i.strip('\r') for i in lines]
        #print 'lines ' + str(lines)

        self.d = dict()
        for l in lines:
            if l == "":
                pass
            else:
                if 'seq' in l:
                    seq = l.split(' ')[-1].strip(' ')
                    #print 'afafasff' + seq
                    self.d[seq] = list()
                else:
                    line_splitted = l.split(',')
                    sh_d = dict()
                    sh_d['shot'] = line_splitted[0]
                    sh_d['first_frame'] = line_splitted[1]
                    sh_d['last_frame'] = line_splitted[2]
                    sh_d['preroll'] = line_splitted[3]
                    self.d[seq].append(sh_d)

        # for i in self.d.keys():
        #     print self.d[i]

    def getSequences(self):
        return self.d.keys()

    def getShots(self, seq):
        shotsList = list()
        shotsData = self.d[seq]
        #print "DATA CSV", self.d
        for i in shotsData:
            #print "I", i
            shotsList.append(i['shot'])
        return shotsList

    def getAllShotData(self, seq, shot):
        shots = self.d[seq]
        #print shots
        shotData = [i for i in shots if i['shot'] == shot]
        return shotData[0]

    def getSpecificShotData(self, seq, shot, key):
        shots = self.d[seq]
        #print shots
        shotData = [i for i in shots if i['shot'] == shot]
        return shotData[0][key]

    def getDict(self):
        return self.d

    def __repr__(self):
        print str(self.d)

if __name__ == '__main__':
    pass
    #v = projectDict('P:/rnd3')
    #print v.getSequences()
    #print v.getShots('Poker')
    #print v.getAllShotData('Poker', 'sh_010')
    #print v.getSpecificShotData('Poker', 'sh_010', 'first_frame')

