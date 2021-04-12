# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\dev\Pipeline\maya\Exporter\AssetExporter_UI.ui'
#
# Created: Thu Nov 15 17:51:08 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!
try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *
import sys

class Ui_AssetExportDialog(object):
    def setupUi(self, AssetExportDialog):
        AssetExportDialog.setObjectName("AssetExportDialog")
        AssetExportDialog.resize(450, 349)
        self.vLayout_main = QVBoxLayout(AssetExportDialog)
        self.vLayout_main.setObjectName("vLayout_main")
        self.hLayout_top = QHBoxLayout()
        self.hLayout_top.setObjectName("hLayout_top")
        self.gridLayout_top = QGridLayout()
        self.gridLayout_top.setObjectName("gridLayout_top")
        self.lb_source = QLabel(AssetExportDialog)
        self.lb_source.setObjectName("lb_source")
        self.gridLayout_top.addWidget(self.lb_source, 0, 0, 1, 1)
        self.comboSource = QComboBox(AssetExportDialog)
        self.comboSource.setMaximumSize(QSize(200, 16777215))
        self.comboSource.setObjectName("comboSource")
        self.comboSource.addItem("")
        self.comboSource.addItem("")
        self.comboSource.addItem("")
        self.gridLayout_top.addWidget(self.comboSource, 0, 1, 1, 1)
        self.lb_type = QLabel(AssetExportDialog)
        self.lb_type.setObjectName("lb_type")
        self.gridLayout_top.addWidget(self.lb_type, 1, 0, 1, 1)
        self.comboBoxType = QComboBox(AssetExportDialog)
        self.comboBoxType.setMaximumSize(QSize(200, 16777215))
        self.comboBoxType.setObjectName("comboBoxType")
        self.comboBoxType.addItem("")
        self.comboBoxType.addItem("")
        self.gridLayout_top.addWidget(self.comboBoxType, 1, 1, 1, 1)
        self.lb_geoType = QLabel(AssetExportDialog)
        self.lb_geoType.setObjectName("lb_geoType")
        self.gridLayout_top.addWidget(self.lb_geoType, 2, 0, 1, 1)
        self.comboBoxGeoType = QComboBox(AssetExportDialog)
        self.comboBoxGeoType.setMaximumSize(QSize(200, 16777215))
        self.comboBoxGeoType.setObjectName("comboBoxGeoType")
        self.gridLayout_top.addWidget(self.comboBoxGeoType, 2, 1, 1, 1)
        self.lb_ext = QLabel(AssetExportDialog)
        self.lb_ext.setObjectName("lb_ext")
        self.gridLayout_top.addWidget(self.lb_ext, 3, 0, 1, 1)
        self.comboBoxExt = QComboBox(AssetExportDialog)
        self.comboBoxExt.setMinimumSize(QSize(150, 0))
        self.comboBoxExt.setMaximumSize(QSize(200, 16777215))
        self.comboBoxExt.setObjectName("comboBoxExt")
        self.comboBoxExt.addItem("")
        self.comboBoxExt.addItem("")
        self.comboBoxExt.addItem("")
        self.gridLayout_top.addWidget(self.comboBoxExt, 3, 1, 1, 1)
        self.hLayout_top.addLayout(self.gridLayout_top)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout_top.addItem(spacerItem)
        self.vLayout_main.addLayout(self.hLayout_top)
        self.hLayout_version = QHBoxLayout()
        self.hLayout_version.setObjectName("hLayout_version")
        self.lb_version = QLabel(AssetExportDialog)
        self.lb_version.setObjectName("lb_version")
        self.hLayout_version.addWidget(self.lb_version)
        self.le_version = QLineEdit(AssetExportDialog)
        self.le_version.setMaximumSize(QSize(70, 16777215))
        self.le_version.setObjectName("le_version")
        self.hLayout_version.addWidget(self.le_version)
        self.horizontalSlider = QSlider(AssetExportDialog)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.hLayout_version.addWidget(self.horizontalSlider)
        self.pb_setLastVer = QPushButton(AssetExportDialog)
        self.pb_setLastVer.setObjectName("pb_setLastVer")
        self.hLayout_version.addWidget(self.pb_setLastVer)
        self.vLayout_main.addLayout(self.hLayout_version)
        self.hLayout_objectName = QHBoxLayout()
        self.hLayout_objectName.setObjectName("hLayout_objectName")
        self.pb_selectObjectName = QPushButton(AssetExportDialog)
        self.pb_selectObjectName.setObjectName("pb_selectObjectName")
        self.hLayout_objectName.addWidget(self.pb_selectObjectName)
        self.lb_objectName = QLabel(AssetExportDialog)
        self.lb_objectName.setObjectName("lb_objectName")
        self.hLayout_objectName.addWidget(self.lb_objectName)
        self.le_objectName = QLineEdit(AssetExportDialog)
        self.le_objectName.setObjectName("le_objectName")
        self.hLayout_objectName.addWidget(self.le_objectName)
        self.vLayout_main.addLayout(self.hLayout_objectName)

        #####
        self.pb_tool = QToolButton(AssetExportDialog)
        self.pb_tool.setText("...")
        self.hLayout_objectName.addWidget(self.pb_tool)
        #####

        self.hLayout_component = QHBoxLayout()
        self.hLayout_component.setObjectName("hLayout_component")
        self.pb_componet = QPushButton(AssetExportDialog)
        self.pb_componet.setObjectName("pb_componet")
        self.hLayout_component.addWidget(self.pb_componet)
        self.lb_component = QLabel(AssetExportDialog)
        self.lb_component.setObjectName("lb_component")
        self.hLayout_component.addWidget(self.lb_component)
        self.le_component = QLineEdit(AssetExportDialog)
        self.le_component.setObjectName("le_component")
        self.hLayout_component.addWidget(self.le_component)
        self.vLayout_main.addLayout(self.hLayout_component)
        self.hLayout_filePath = QHBoxLayout()
        self.hLayout_filePath.setObjectName("hLayout_filePath")
        self.lb_filePath = QLabel(AssetExportDialog)
        self.lb_filePath.setObjectName("lb_filePath")
        self.hLayout_filePath.addWidget(self.lb_filePath)
        self.le_filePath = QLineEdit(AssetExportDialog)
        self.le_filePath.setEnabled(False)
        self.le_filePath.setObjectName("le_filePath")
        self.hLayout_filePath.addWidget(self.le_filePath)
        self.vLayout_main.addLayout(self.hLayout_filePath)
        self.hLayout_Export = QHBoxLayout()
        self.hLayout_Export.setObjectName("hLayout_Export")
        self.lb_curves = QLabel(AssetExportDialog)
        self.lb_curves.setText("Curves")
        self.ch_box = QCheckBox(AssetExportDialog)
        self.hLayout_Export.addWidget(self.lb_curves)
        self.hLayout_Export.addWidget(self.ch_box)

        self.lb_step = QLabel(AssetExportDialog)
        self.lb_step.setText("Sub step:")
        self.hLayout_Export.addWidget(self.lb_step)
        self.le_step = QLineEdit(AssetExportDialog)
        self.le_step.setMaximumWidth(40)
        self.le_step.setText("1.0")
        self.le_step.setValidator(QDoubleValidator())
        self.hLayout_Export.addWidget(self.le_step)



        spacerItem1 = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout_Export.addItem(spacerItem1)


        self.lb_message = QLabel(AssetExportDialog)
        self.lb_message.setText("Send message:")
        self.ch_box_message = QCheckBox(AssetExportDialog)
        self.hLayout_Export.addWidget(self.lb_message)
        self.hLayout_Export.addWidget(self.ch_box_message)

        self.lb_namspace = QLabel(AssetExportDialog)
        self.lb_namspace.setText("strip Namespace:")
        self.ch_box_namespace = QCheckBox(AssetExportDialog)
        self.hLayout_Export.addWidget(self.lb_namspace)
        self.hLayout_Export.addWidget(self.ch_box_namespace)






        self.pb_export = QPushButton(AssetExportDialog)


        self.pb_export.setMaximumSize(QSize(300, 16777215))
        self.pb_export.setObjectName("pb_export")

        self.hLayout_Export.addWidget(self.pb_export)
        spacerItem2 = QSpacerItem(50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout_Export.addItem(spacerItem2)
        self.vLayout_main.addLayout(self.hLayout_Export)

        self.retranslateUi(AssetExportDialog)
        QMetaObject.connectSlotsByName(AssetExportDialog)

    def retranslateUi(self, AssetExportDialog):
        AssetExportDialog.setWindowTitle("AssetExporter")
        self.comboBoxGeoType.addItems(["PROPS", "ENV", "CHAR"])
        self.lb_source.setText("SOURCE PATH")
        self.comboSource.setItemText(0, "ASSETBUILDS")
        self.comboSource.setItemText(1, "SHOT")
        self.comboSource.setItemText(2, "LIBRARY")
        self.lb_type.setText("TYPE")
        self.comboBoxType.setItemText(0, "GEO")
        self.comboBoxType.setItemText(1, "ANIMATION")
        self.lb_geoType.setText("GEO Type")
        self.lb_ext.setText("File Extension")
        self.comboBoxExt.setItemText(0, "ABC")
        self.comboBoxExt.setItemText(1, "BGEO.SC")
        self.comboBoxExt.setItemText(2, "OBJ")
        self.lb_version.setText("Version")
        self.le_version.setText("1")
        self.pb_setLastVer.setText("Set Last Version")
        self.pb_selectObjectName.setText("Select ObjectName")
        self.lb_objectName.setText("Object Name")
        self.pb_componet.setText("Component Name")
        self.lb_component.setText("Component Name")
        self.lb_filePath.setText("FILE PATH")
        self.pb_export.setText("Expot")

class TEST(QWidget, Ui_AssetExportDialog):
    def __init__(self, parent=None):
        super(TEST, self).__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    import sys
    app = QApplication([])
    w=TEST()
    w.show()
    sys.exit(app.exec_())
