

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *


import sys, subprocess, os

path = os.environ['PIPELINE_ROOT'] + "/modules"
if not path in sys.path:
    sys.path.append(path)
    sys.path.append(path+"/moviepy")

from functools import partial
from modules.moviepy.editor import *
from montage_item import MontageItem



class MakeMontage(QDialog):
    def __init__(self, parent=None):
        super(MakeMontage, self).__init__(parent)
        self.resize(800,540)

        self.pb_montage_hd = QPushButton(self)
        self.pb_montage_3K = QPushButton(self)
        self.list_dailies = QListWidget(self)
        self.layoutMain = QVBoxLayout(self)
        self.layoutButtonsTop = QHBoxLayout()
        self.layoutButtonsBottom = QHBoxLayout()
        self.layoutProgressBar = QHBoxLayout()
        self.lb_progress = QLabel(self)
        self.progressBar = QProgressBar(self)

        self.layoutMain.addWidget(self.list_dailies)
        self.layoutButtonsBottom.addWidget(self.pb_montage_hd)
        self.layoutButtonsBottom.addWidget(self.pb_montage_3K)
        self.layoutProgressBar.addWidget(self.lb_progress)
        self.layoutProgressBar.addWidget(self.progressBar)

        self.layoutMain.addLayout(self.layoutButtonsTop)
        self.layoutMain.addLayout(self.layoutButtonsBottom)
        self.layoutMain.addLayout(self.layoutProgressBar)

        self.pb_montage_hd.setText("1920x1080")
        self.pb_montage_3K.setText("3200x1800")
        self.lb_progress.setText("Rendering...")

        self.pb_montage_hd.setMinimumHeight(30)
        self.pb_montage_3K.setMinimumHeight(30)
        self.progressBar.setRange(0, 100)
        self.progressBar.setVisible(False)
        self.lb_progress.setVisible(False)
        self.list_dailies.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.pb_montage_hd.clicked.connect(partial(self.onStart, self.pb_montage_hd.text()))
        self.pb_montage_3K.clicked.connect(partial(self.onStart, self.pb_montage_3K.text()))

        self.myLongTask = TaskThread(self.make_montage)
        self.myLongTask.taskFinished.connect(self.onFinished)

        self.project_path = None
        self.sequence = None
        self.shots = None


    def set_shots(self, project_path, sequence, shots):
        self.list_dailies.clear()
        if shots:
            for i in shots:
                if "sh000" in i:
                    pass
                else:
                    # ITEM MODEL VIEW
                    model = MontageItem(shot=i)
                    listItem = QListWidgetItem()
                    self.list_dailies.addItem(listItem)
                    listItem.setSizeHint(QSize(0, 30))
                    self.list_dailies.setItemWidget(listItem, model)

            self.project_path = project_path
            self.sequence = sequence
            self.shots = shots
            return self.project_path, self.sequence, self.shots


    def make_montage(self, size):
        path = self.project_path + "/edit/" + self.sequence

        if not os.path.exists(path):
            os.makedirs(path)
        videos = []


        for i in self.list_dailies.selectedItems():
            if os.path.isfile(self.list_dailies.itemWidget(i).dailies):
                videos.append(self.list_dailies.itemWidget(i).dailies)
            else:
                pass
        videos = sorted(videos)

        clips = []
        for i in videos:
            clips.append(VideoFileClip(i, target_resolution=(size['height'], size['width'])))

        final_clip = concatenate_videoclips(clips)
        pathMp4 = path+"/"+self.sequence+".mp4"

        files = os.listdir(path)
        versions = []
        version = "001"
        if files:
            for f in files:
                if ".mov" in f:
                    v = f.rsplit(".", 1)[0]
                    if "_v" in v:
                        v = v.rsplit("_v", 1)[1]
                        if v.isdigit():
                            versions.append(v)
            if versions:
                versions.sort()
                version = str(int(versions[-1])+1).zfill(3)


        pathMov = path + "/" + self.sequence + "_v" + version + ".mov"
        final_clip.to_videofile(pathMp4, fps=24, remove_temp=False, temp_audiofile=os.path.expanduser("~")+"/montage_temp.wav")
        #final_clip.write_videofile("output3.mp4", fps=24, audio_codec='pcm_s16le', remove_temp=False, temp_audiofile=os.path.expanduser("~")+"/montage_temp.wav")  # will use 16-bit WAV
        self.progressBar.setRange(0,100)
        self.progressBar.setVisible(True)
        mpg = "X:/app/win/Pipeline/modules/ffmpeg/bin/ffmpeg -y -r 24 -i " + pathMp4 + " -f mov " + pathMov
        subprocess.call(mpg, shell=True)
        self.progressBar.setValue(90)
        subprocess.call([r"X:\app\win\rv\rv7.1.1\bin\rv.exe", pathMov])


    def onStart(self, btn):
        if self.list_dailies.selectedItems():
            self.progressBar.setVisible(True)
            self.lb_progress.setVisible(True)
            self.repaint()
            self.progressBar.setRange(0,0)
            self.myLongTask.setSize(width=int(btn.split("x")[0]), height=int(btn.split("x")[1]))
            self.myLongTask.start()
        else:
            message = QMessageBox(self)
            message.setStyleSheet("QPushButton{ width:100px; font-size: 16px; }")
            message.setText("Please select files.")
            message.show()


    def onFinished(self):
        # Stop the pulsation
        self.progressBar.setVisible(False)
        self.lb_progress.setVisible(False)
        self.progressBar.setRange(0,1)



class TaskThread(QThread):
    taskFinished = Signal()
    def __init__(self, function):
        QThread.__init__(self)
        self.function = function
        self.size = dict(width=1920, height=1080)

    def setSize(self, width, height):
        self.size = dict(width=width, height=height)


    def run(self):
        self.function(size=self.size)
        self.taskFinished.emit()





if __name__ == '__main__':

    app = QApplication([])
    w=MakeMontage()
    w.show()
    sys.exit(app.exec_())





