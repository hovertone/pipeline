# -*- coding: utf-8 -*-


try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

import os, sys

from loader_pref_UIs import Ui_Preferences
from loader_preferences import LoaderPrefs


class LoaderPreferencesUI (QWidget, Ui_Preferences):
    def __init__(self, parent=None):
        super(LoaderPreferencesUI, self).__init__(parent)
        self.setupUi(self)


        self.pref = LoaderPrefs()
        print "Preferences path: ", self.pref.path
        try:
            data = self.pref.load()["storage"]
            self.le_projects.setText(data["projects"])
            self.le_caches.setText(data["caches"])
            self.le_lib.setText(data["lib"])
            self.le_name.setText("username")
            self.le_key.setText("key")
        except:
            self.le_projects.setText("P:")
            self.le_caches.setText("Q:")
            self.le_lib.setText("L:/assetLib")
            self.le_name.setText("None")
            self.le_key.setText("None")

        self.pb_save.clicked.connect(self.save_prefs)
        self.pb_cancel.clicked.connect(self.close)


    def save_prefs(self):
        old_data = self.pref.load()["indexes"]
        storage = dict(projects=self.le_projects.text(), caches=self.le_caches.text(), lib=self.le_lib.text())
        user = dict(username=self.le_name.text(), key=self.le_key.text())

        data = dict(storage=storage, login=user, indexes=old_data)
        self.pref.save(data)
        self.close()








if __name__ == '__main__':

    app = QApplication([])
    w=LoaderPreferencesUI()
    w.show()
    sys.exit(app.exec_())




