print 'in subprocess taskbar'
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os
import sys
import shutil
import time
import nuke
import threading

# sys.path.append(os.path.abspath(os.getcwd()))

#from uis.progress_bar_v001_UI import Ui_Form

# class TaskThread(QThread):
#     taskFinished = Signal()
#
#     def __init__(self, function):
#         QThread.__init__(self)
#         self.function = function
#         self.files = None
#
#     def setFiles(self, files):
#         self.files = files
#
#     def run(self):
#         self.function(self.files)
#         self.taskFinished.emit()
#

class removeFiles(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.iter = 0

        self.glob_path = path
        self.collect_files_to_remove(self.glob_path)

    def collect_files_to_remove(self, path):
        #folder =
        files = list()
        folders = list()

        for rootDir, subdirs, filenames in os.walk(path):
            # Find the files that matches the given patterm
            if filenames:
                for f in filenames:
                    fullpath = '%s/%s' % (rootDir, f)
                    fullpath = fullpath.replace('\\', '/')
                    if fullpath not in files:
                        files.append(fullpath)
                    if rootDir not in folders:
                        folders.append(rootDir.replace('\\', '/'))
        #self.tread.setFiles(files)
        self.files_to_remove = files + folders
        print 'FILES TO REMOVE %s' % str(self.files_to_remove)

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



class progress_bar(QDialog):
    def __init__(self, parent=None):
        super(progress_bar, self).__init__(parent)

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
        #self.show()
        #self.tread = TaskThread(self.rmv)

        #self.tread.start()
        self.fillBar()

    def fillBar(self):

        self.progressBar.setValue(1)

        rf = removeFiles('D:/my/progress_bar_tests/start')
        rf.start()

        self.progressBar.setValue(100)
        self.close()

    def collect_files_to_remove(self, path):
        #folder =
        files = list()
        folders = list()

        for rootDir, subdirs, filenames in os.walk(path):
            # Find the files that matches the given patterm
            if filenames:
                for f in filenames:
                    fullpath = '%s/%s' % (rootDir, f)
                    fullpath = fullpath.replace('\\', '/')
                    if fullpath not in files:
                        files.append(fullpath)
                    if rootDir not in folders:
                        folders.append(rootDir.replace('\\', '/'))
        #self.tread.setFiles(files)
        self.files_to_remove = files + folders




# ===================================================================================


#
# def collect_files_to_remove(path):
#     #folder =
#     files = list()
#     folders = list()
#
#     for rootDir, subdirs, filenames in os.walk(path):
#         # Find the files that matches the given patterm
#         if filenames:
#             for f in filenames:
#                 fullpath = '%s/%s' % (rootDir, f)
#                 fullpath = fullpath.replace('\\', '/')
#                 if fullpath not in files:
#                     files.append(fullpath)
#                 if rootDir not in folders:
#                     folders.append(rootDir.replace('\\', '/'))
#
#     return files + folders
#
# def rmv(p):
#     if os.path.isfile(p):
#         os.remove(p)
#         print 'FILE removed %s' % p
#     elif os.path.isdir(p):
#         shutil.rmtree(p)
#         print 'FOLDER removed %s' % p
#
# def progress_example():
#     t = nuke.ProgressTask("Example!")
#
#     obj_to_remove = collect_files_to_remove('D:/my/progress_bar_tests/start')
#
#     #tasks = len(files) + len(folders)
#
#     for i, x in enumerate(obj_to_remove):
#         percent = int(100 * (float(i) / (len(obj_to_remove) - 1)))
#         t.setProgress(percent)
#         t.setMessage("Removing %s" % (x))
#         rmv(x)
#         #time.sleep(0.1)
#
#
# def progress_example2():
#     tasks = 3
#     task = nuke.ProgressTask("Working!")
#     for i in range(tasks):
#         if task.isCancelled():
#             break
#
#         task.setMessage("Step %s of %d" % (i+1, tasks))
#         percent = int(100*(float(i) / (tasks)))
#         task.setProgress(percent)
#         time.sleep(2)
#
# def progress_example3():
#     task = nuke.ProgressTask('Examining Read Nodes...')
#     reads = nuke.allNodes('Read')
#     progIncr = 100.0 / len(reads)
#     for i, r in enumerate(reads):
#         if task.isCancelled():
#             nuke.executeInMainThread(nuke.message, args=('Aborted',))
#             return
#         task.setProgress(int(i * progIncr))
#         task.setMessage(r.fullName())
#         # Placeholder for some long per-node process
#         time.sleep(2)






if __name__ == '__main__':

    app = QApplication([])
    w=progress_bar()
    w.show()
    sys.exit(app.exec_())

    #print collect_files_to_remove('D:/my/progress_bar_tests/start')
