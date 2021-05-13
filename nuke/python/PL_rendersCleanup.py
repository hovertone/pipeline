try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os
import fnmatch
import nuke
import shutil
import threading

from PL_scripts import getPipelineAttrs

renders_size = 0
precomps_size = 0
renders_folder = ''
precomps_folder = ''

def fixMissingPaths():
    needToFix = False
    for r in nuke.allNodes('Read'):
        if r.error():
            needToFix = True
            break

    print 'NEED TO FIX: %s' % needToFix
    if needToFix:
        for r in nuke.allNodes():
            if r.Class() == 'Read' or r.Class() == 'Camera2' or r.Class() == 'DeepRead' or r.Class() == 'ReadGeo2':
                oldVal = r['file'].value()
                newVal = oldVal.replace('P:/vikingsShorts/shots', 'P:/vikings/vikingsShorts/shots')
                r['file'].setValue(newVal)


def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return round(total_size/(1024*1024*1024.0), 2)

class removeFiles(threading.Thread):
    def __init__(self, files):
        threading.Thread.__init__(self)
        self.iter = 0

        self.files_to_remove = files


    def rmv(self, p):
        #print 'ITER BEFORE %s' % self.iter
        if os.path.isfile(p):
            os.remove(p)
            print 'FILE removed %s' % p
        elif os.path.isdir(p):
            shutil.rmtree(p)
            print 'FOLDER removed %s' % p
        #self.iter += 1
        #print 'ITER AFTER %s' % self.iter

    def run(self):
        for i, e in enumerate(self.files_to_remove):
            nuke.executeInMainThread(self.rmv, e)
            #return i, len(self.files_to_remove)

class cleanup_progress_bar(QDialog):
    def __init__(self, parent=None, remove_precomps=False):
        super(cleanup_progress_bar, self).__init__(parent)
        global renders_size, precomps_size, renders_folder, precomps_folder

        self.resize(400, 240)

        self.layout = QVBoxLayout()

        self.status_label =QLabel()
        self.layout.addWidget(self.status_label)
        self.progressBar = QProgressBar()
        self.progressBar.setGeometry(200, 80, 250, 20)
        self.layout.addWidget(self.progressBar)
        self.cancel = QPushButton()
        self.cancel.setText('Cancel')
        self.cancel.clicked.connect(self.close)
        self.layout.addWidget(self.cancel)

        self.setLayout(self.layout)
        self.remove_precomps = remove_precomps
        #self.show()
        #self.tread = TaskThread(self.rmv)

        #self.tread.start()

        self.progressBar.setValue(1)
        self.collect_files_to_remove()
        self.progressBar.setValue(33)
        renders_folder = self.render_path
        renders_size = self.renders_dir_size_old

        if self.remove_precomps:
            self.deal_with_precomps()
            precomps_folder = self.precomps_dir
            precomps_size = self.precomps_dir_size_old
        self.progressBar.setValue(66)


        rf = removeFiles(self.files_to_remove)
        rf.start()

        self.progressBar.setValue(100)

        self.renders_dir_size_new = get_size(self.render_path)
        #
        # if self.remove_precomps:
        #     nuke.message('Old size: %s Gb\nNewSize: %s Gb\n\nPrecomps were %s Gb' % (self.renders_dir_size_old, self.renders_dir_size_new, self.precomps_dir_size_old))
        # else:
        #     nuke.message('Old size: %s Gb\nNewSize: %s Gb' % (self.renders_dir_size_old, self.renders_dir_size_new))

        self.close()


    def deal_with_precomps(self):
        # PRECOMPS PART
        self.precomps_dir = '%s/%s/sequences/%s/%s/comp/%s/precomp' % (self.drive, self.project, self.seq, self.shot, self.assetName)
        self.precomps_dir_size_old = get_size(self.precomps_dir)

        for bdn in nuke.allNodes('BackdropNode'):
            for n in bdn.getNodes():
                nuke.delete(n)
            nuke.delete(bdn)
        print 'PRECOMP NODES REMOVED'

        if os.path.exists(self.precomps_dir):
            #newSize += get_size(precomps_dir)
            shutil.rmtree(self.precomps_dir)
            print 'PRECOMPS FOLDER REMOVED'
        self.precomps_dir_size_new = get_size(self.precomps_dir)

    def collect_files_to_remove(self):
        # rf = removeFiles('D:/my/progress_bar_tests/start')
        # rf.start()
        # fixMissingPaths()
        newSize = 0.0
        root = nuke.root().name()
        try:
            self.drive, self.project, self.seq, self.shot, self.assetName, self.version = getPipelineAttrs()
            self.render_path = '%s/%s/sequences/%s/%s/render' % (self.drive, self.project, self.seq, self.shot)
        except:
            if 'vikings' in root:
                split = root.split('/')
                render_path = '/'.join(split[:-2]) + '/render'

            else:
                print 'dont have shot attrs. EXIT'
                return

        # print 'path %s' % path
        paths = sorted([i['file'].value() for i in nuke.allNodes('Read') + nuke.allNodes('DeepRead') if
                        self.render_path in i['file'].value()])

        # Get a list of all files and directories to remove
        self.files_to_remove = list()
        dirsToRemove = list()
        for rootDir, subdirs, filenames in os.walk(self.render_path):
            # Find the files that matches the given patterm
            if filenames:
                deleteFolder = False
                for f in filenames:
                    in_script = False
                    for pat in paths:
                        p = pat.split('.')[0]
                        print 'ROOTDIR %s %s' % (rootDir, f)
                        fullpath = '%s/%s' % (rootDir, f)
                        fullpath = fullpath.replace('\\', '/')
                        # print 'FULLPATH %s' % fullpath
                        if p in fullpath:
                            in_script = True


                    if in_script:
                        print 'KEEP %s' % fullpath
                    else:
                        print 'DELETE %s' % fullpath
                        # os.remove(fullpath)
                        self.files_to_remove.append(fullpath)
                        folder = os.path.dirname(fullpath)
                        if folder not in dirsToRemove:
                            dirsToRemove.append(folder)

                print '----------------------------------------'
        self.files_to_remove += dirsToRemove

        self.renders_dir_size_old = get_size(self.render_path)

def startWithThis(remove_precomps=False):
    global renders_size, precomps_size, renders_folder, precomps_folder
    if remove_precomps:
        w = cleanup_progress_bar(remove_precomps=True)
    else:
        w = cleanup_progress_bar()

    w.show()

    renders_size_new = get_size(renders_folder)

    if remove_precomps:
        precomps_size_new = get_size(precomps_folder)
        nuke.message('Old size: %s Gb\nNewSize: %s Gb\n\nPrecomps were %s Gb\nPrecomps now %s Gb' % (renders_size, renders_size_new, precomps_size, precomps_size_new))
    else:
        nuke.message('Old size: %s Gb\nNewSize: %s Gb' % (renders_size, renders_size_new))




