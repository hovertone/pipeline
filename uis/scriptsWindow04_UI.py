# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'X:\app\win\Pipeline\uis222\scriptsWindow04.ui'
#
# Created: Wed May 22 19:05:57 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(607, 269)
        self.viewerGroup = QtGui.QGroupBox(Form)
        self.viewerGroup.setGeometry(QtCore.QRect(10, 10, 181, 111))
        self.viewerGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.viewerGroup.setObjectName("viewerGroup")
        self.layoutWidget = QtGui.QWidget(self.viewerGroup)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 161, 83))
        self.layoutWidget.setObjectName("layoutWidget")
        self.viewerLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.viewerLayout.setContentsMargins(0, 0, 0, 0)
        self.viewerLayout.setObjectName("viewerLayout")
        self.flopflop = QtGui.QPushButton(self.layoutWidget)
        self.flopflop.setObjectName("flopflop")
        self.viewerLayout.addWidget(self.flopflop)
        self.autocrop = QtGui.QPushButton(self.layoutWidget)
        self.autocrop.setObjectName("autocrop")
        self.viewerLayout.addWidget(self.autocrop)
        self.viewerToRGBA = QtGui.QPushButton(self.layoutWidget)
        self.viewerToRGBA.setObjectName("viewerToRGBA")
        self.viewerLayout.addWidget(self.viewerToRGBA)
        self.nodegraphGroup = QtGui.QGroupBox(Form)
        self.nodegraphGroup.setGeometry(QtCore.QRect(200, 10, 161, 171))
        self.nodegraphGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.nodegraphGroup.setObjectName("nodegraphGroup")
        self.layoutWidget1 = QtGui.QWidget(self.nodegraphGroup)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 141, 141))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.nodegraphLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.nodegraphLayout.setContentsMargins(0, 0, 0, 0)
        self.nodegraphLayout.setObjectName("nodegraphLayout")
        self.lineupHorizontally = QtGui.QPushButton(self.layoutWidget1)
        self.lineupHorizontally.setObjectName("lineupHorizontally")
        self.nodegraphLayout.addWidget(self.lineupHorizontally)
        self.lineupVertically = QtGui.QPushButton(self.layoutWidget1)
        self.lineupVertically.setObjectName("lineupVertically")
        self.nodegraphLayout.addWidget(self.lineupVertically)
        self.toggleViewerInputs = QtGui.QPushButton(self.layoutWidget1)
        self.toggleViewerInputs.setObjectName("toggleViewerInputs")
        self.nodegraphLayout.addWidget(self.toggleViewerInputs)
        self.mirrorNodes = QtGui.QPushButton(self.layoutWidget1)
        self.mirrorNodes.setObjectName("mirrorNodes")
        self.nodegraphLayout.addWidget(self.mirrorNodes)
        self.w_scaletree = QtGui.QPushButton(self.layoutWidget1)
        self.w_scaletree.setObjectName("w_scaletree")
        self.nodegraphLayout.addWidget(self.w_scaletree)
        self.writeGroup = QtGui.QGroupBox(Form)
        self.writeGroup.setGeometry(QtCore.QRect(10, 120, 181, 91))
        self.writeGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.writeGroup.setObjectName("writeGroup")
        self.layoutWidget2 = QtGui.QWidget(self.writeGroup)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 20, 161, 54))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.writeLayout = QtGui.QVBoxLayout(self.layoutWidget2)
        self.writeLayout.setContentsMargins(0, 0, 0, 0)
        self.writeLayout.setObjectName("writeLayout")
        self.deleteWriteFiles = QtGui.QPushButton(self.layoutWidget2)
        self.deleteWriteFiles.setObjectName("deleteWriteFiles")
        self.writeLayout.addWidget(self.deleteWriteFiles)
        self.rerenderMissingFrames = QtGui.QPushButton(self.layoutWidget2)
        self.rerenderMissingFrames.setObjectName("rerenderMissingFrames")
        self.writeLayout.addWidget(self.rerenderMissingFrames)
        self.otherGroup = QtGui.QGroupBox(Form)
        self.otherGroup.setGeometry(QtCore.QRect(370, 10, 201, 221))
        self.otherGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.otherGroup.setObjectName("otherGroup")
        self.layoutWidget3 = QtGui.QWidget(self.otherGroup)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 20, 181, 191))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.otherLayout = QtGui.QVBoxLayout(self.layoutWidget3)
        self.otherLayout.setContentsMargins(0, 0, 0, 0)
        self.otherLayout.setObjectName("otherLayout")
        self.glezin = QtGui.QPushButton(self.layoutWidget3)
        self.glezin.setObjectName("glezin")
        self.otherLayout.addWidget(self.glezin)
        self.batchRenamer = QtGui.QPushButton(self.layoutWidget3)
        self.batchRenamer.setObjectName("batchRenamer")
        self.otherLayout.addWidget(self.batchRenamer)
        self.deepDefocusSlicer = QtGui.QPushButton(self.layoutWidget3)
        self.deepDefocusSlicer.setObjectName("deepDefocusSlicer")
        self.otherLayout.addWidget(self.deepDefocusSlicer)
        self.normalize = QtGui.QPushButton(self.layoutWidget3)
        self.normalize.setObjectName("normalize")
        self.otherLayout.addWidget(self.normalize)
        self.copyTrackingDataToRoto = QtGui.QPushButton(self.layoutWidget3)
        self.copyTrackingDataToRoto.setObjectName("copyTrackingDataToRoto")
        self.otherLayout.addWidget(self.copyTrackingDataToRoto)
        self.cameraFromExr = QtGui.QPushButton(self.layoutWidget3)
        self.cameraFromExr.setObjectName("cameraFromExr")
        self.otherLayout.addWidget(self.cameraFromExr)
        self.toolsetLoaderGroup = QtGui.QGroupBox(Form)
        self.toolsetLoaderGroup.setGeometry(QtCore.QRect(200, 180, 161, 81))
        self.toolsetLoaderGroup.setAlignment(QtCore.Qt.AlignCenter)
        self.toolsetLoaderGroup.setObjectName("toolsetLoaderGroup")
        self.widget = QtGui.QWidget(self.toolsetLoaderGroup)
        self.widget.setGeometry(QtCore.QRect(10, 20, 141, 54))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolsetLoaderCreate = QtGui.QPushButton(self.widget)
        self.toolsetLoaderCreate.setObjectName("toolsetLoaderCreate")
        self.verticalLayout.addWidget(self.toolsetLoaderCreate)
        self.toolsetLoader = QtGui.QPushButton(self.widget)
        self.toolsetLoader.setObjectName("toolsetLoader")
        self.verticalLayout.addWidget(self.toolsetLoader)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.viewerGroup.setTitle(QtGui.QApplication.translate("Form", "Viewer Stuff", None, QtGui.QApplication.UnicodeUTF8))
        self.flopflop.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Зеркалит картинку по горизонтали. </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.flopflop.setText(QtGui.QApplication.translate("Form", "FLOP FLOP", None, QtGui.QApplication.UnicodeUTF8))
        self.flopflop.setProperty("script", QtGui.QApplication.translate("Form", "LH.mirrorViewer()", None, QtGui.QApplication.UnicodeUTF8))
        self.flopflop.setProperty("name", QtGui.QApplication.translate("Form", "flopflop", None, QtGui.QApplication.UnicodeUTF8))
        self.flopflop.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.autocrop.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Создает <span style=\" font-weight:600;\">CROP </span>ноду, которой оставляет только <span style=\" text-decoration: underline;\">нужные</span> пиксели.</p><p>Перед выполнением нужно заселектить ноду.</p><p>Сканирует по альфе.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.autocrop.setText(QtGui.QApplication.translate("Form", "AUTOCROP", None, QtGui.QApplication.UnicodeUTF8))
        self.autocrop.setProperty("script", QtGui.QApplication.translate("Form", "frames = nuke.getInput(\'Set Frame Range\', \'%s-%s\' % (int(nuke.root()[\'first_frame\'].value()), int(nuke.root()[\'last_frame\'].value()))).split(\'-\')\n"
"nukescripts.autocrop(first = frames[0], last = frames[1], layer = \'alpha\')", None, QtGui.QApplication.UnicodeUTF8))
        self.autocrop.setProperty("name", QtGui.QApplication.translate("Form", "autocrop", None, QtGui.QApplication.UnicodeUTF8))
        self.autocrop.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.viewerToRGBA.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Пересчелкивает вьювер в <span style=\" font-weight:600;\">rgba</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.viewerToRGBA.setText(QtGui.QApplication.translate("Form", "Viewer to RGBA", None, QtGui.QApplication.UnicodeUTF8))
        self.viewerToRGBA.setProperty("script", QtGui.QApplication.translate("Form", "v = nuke.activeViewer().node().name()\n"
"nuke.toNode(v)[\'channels\'].setValue(\'rgba\')", None, QtGui.QApplication.UnicodeUTF8))
        self.viewerToRGBA.setProperty("name", QtGui.QApplication.translate("Form", "viewerToRGBA", None, QtGui.QApplication.UnicodeUTF8))
        self.viewerToRGBA.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.nodegraphGroup.setTitle(QtGui.QApplication.translate("Form", "NodeGraph", None, QtGui.QApplication.UnicodeUTF8))
        self.lineupHorizontally.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Выставляет выделенные ноды <span style=\" font-weight:600;\">горизонтально</span>.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lineupHorizontally.setText(QtGui.QApplication.translate("Form", "Lineup Horizontally", None, QtGui.QApplication.UnicodeUTF8))
        self.lineupHorizontally.setProperty("script", QtGui.QApplication.translate("Form", "scripts.lineupNodes()", None, QtGui.QApplication.UnicodeUTF8))
        self.lineupHorizontally.setProperty("name", QtGui.QApplication.translate("Form", "lineupHorizontally", None, QtGui.QApplication.UnicodeUTF8))
        self.lineupHorizontally.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.lineupVertically.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Выставляет выделенные ноды <span style=\" font-weight:600;\">вертикально</span>.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lineupVertically.setText(QtGui.QApplication.translate("Form", "Lineup Vertically", None, QtGui.QApplication.UnicodeUTF8))
        self.lineupVertically.setProperty("script", QtGui.QApplication.translate("Form", "scripts.linedownNodes()", None, QtGui.QApplication.UnicodeUTF8))
        self.lineupVertically.setProperty("name", QtGui.QApplication.translate("Form", "lineupVertically", None, QtGui.QApplication.UnicodeUTF8))
        self.lineupVertically.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.toggleViewerInputs.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Прячет все инпут коннекшены всех нод вьюверов в скрипте.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.toggleViewerInputs.setText(QtGui.QApplication.translate("Form", "Toggle viewer inputs", None, QtGui.QApplication.UnicodeUTF8))
        self.toggleViewerInputs.setProperty("script", QtGui.QApplication.translate("Form", "LH.toggleViewerInput()", None, QtGui.QApplication.UnicodeUTF8))
        self.toggleViewerInputs.setProperty("name", QtGui.QApplication.translate("Form", "toggleViewerInputs", None, QtGui.QApplication.UnicodeUTF8))
        self.toggleViewerInputs.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.mirrorNodes.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Зеркалит расположение выделенных нод по горизонтали.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.mirrorNodes.setText(QtGui.QApplication.translate("Form", "Mirror nodes", None, QtGui.QApplication.UnicodeUTF8))
        self.mirrorNodes.setProperty("script", QtGui.QApplication.translate("Form", "mirrorNodes.mirrorNodes()", None, QtGui.QApplication.UnicodeUTF8))
        self.mirrorNodes.setProperty("name", QtGui.QApplication.translate("Form", "mirronNodes", None, QtGui.QApplication.UnicodeUTF8))
        self.mirrorNodes.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.w_scaletree.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Скейлер расположения выделеных нод.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.w_scaletree.setText(QtGui.QApplication.translate("Form", "W_ScaleTree", None, QtGui.QApplication.UnicodeUTF8))
        self.w_scaletree.setProperty("script", QtGui.QApplication.translate("Form", "W_scaleTree.scaleTreeFloatingPanel()", None, QtGui.QApplication.UnicodeUTF8))
        self.w_scaletree.setProperty("name", QtGui.QApplication.translate("Form", "w_scaleTree", None, QtGui.QApplication.UnicodeUTF8))
        self.w_scaletree.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.writeGroup.setTitle(QtGui.QApplication.translate("Form", "Write", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteWriteFiles.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Удаляет файлы из папки, которая указана в пути <span style=\" font-weight:600;\">write</span> ноды.<br/>Перед выполнением нужно выделить <span style=\" font-weight:600;\">write</span> ноду.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteWriteFiles.setText(QtGui.QApplication.translate("Form", "Delete write files", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteWriteFiles.setProperty("script", QtGui.QApplication.translate("Form", "deleteFilesFromWrite.deleteFilesFromWritePath(nuke.selectedNode())", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteWriteFiles.setProperty("name", QtGui.QApplication.translate("Form", "deleteWriteFiles", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteWriteFiles.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.rerenderMissingFrames.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Дорендеривает недостающие кадры из секвенции <span style=\" font-weight:600;\">write</span> ноды.<br/>Перед выполнением выделить <span style=\" font-weight:600;\">write</span> ноду.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.rerenderMissingFrames.setText(QtGui.QApplication.translate("Form", "Rerender missing frames", None, QtGui.QApplication.UnicodeUTF8))
        self.rerenderMissingFrames.setProperty("script", QtGui.QApplication.translate("Form", "rerenderMissingFrames.rerenderMissedFrame()", None, QtGui.QApplication.UnicodeUTF8))
        self.rerenderMissingFrames.setProperty("name", QtGui.QApplication.translate("Form", "rerenderMissingFrames", None, QtGui.QApplication.UnicodeUTF8))
        self.rerenderMissingFrames.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.otherGroup.setTitle(QtGui.QApplication.translate("Form", "Other", None, QtGui.QApplication.UnicodeUTF8))
        self.glezin.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Удобный сплиттер <span style=\" font-weight:600;\">EXR</span>\'ов. <br/>Перед запуском выделить <span style=\" font-weight:600;\">read </span>ноду.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.glezin.setText(QtGui.QApplication.translate("Form", "Glezin Split EXR", None, QtGui.QApplication.UnicodeUTF8))
        self.glezin.setProperty("script", QtGui.QApplication.translate("Form", "split_layers.main()", None, QtGui.QApplication.UnicodeUTF8))
        self.glezin.setProperty("name", QtGui.QApplication.translate("Form", "glezin", None, QtGui.QApplication.UnicodeUTF8))
        self.glezin.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.batchRenamer.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Переименовывает секвенцию из <span style=\" font-weight:600;\">read</span> ноды.<br/>Перед испольхованием выделить <span style=\" font-weight:600;\">read</span> ноду.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.batchRenamer.setText(QtGui.QApplication.translate("Form", "Batch renamer", None, QtGui.QApplication.UnicodeUTF8))
        self.batchRenamer.setProperty("script", QtGui.QApplication.translate("Form", "batchrenamer.main()", None, QtGui.QApplication.UnicodeUTF8))
        self.batchRenamer.setProperty("name", QtGui.QApplication.translate("Form", "batchRenamer", None, QtGui.QApplication.UnicodeUTF8))
        self.batchRenamer.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.deepDefocusSlicer.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Разрезает <span style=\" font-weight:600;\">deep exr</span> по глубине от камеры на разные плейны и добавляет дефокус на каждый план отдельно.<br/>Перед запуском требуется выделать ноду с <span style=\" font-weight:600;\">deep</span> потоком.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.deepDefocusSlicer.setText(QtGui.QApplication.translate("Form", "Deep Defocus Slicer", None, QtGui.QApplication.UnicodeUTF8))
        self.deepDefocusSlicer.setProperty("script", QtGui.QApplication.translate("Form", "deepDefocusSlicer.deepDefocus()", None, QtGui.QApplication.UnicodeUTF8))
        self.deepDefocusSlicer.setProperty("name", QtGui.QApplication.translate("Form", "deepDefocusSlicer", None, QtGui.QApplication.UnicodeUTF8))
        self.deepDefocusSlicer.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.normalize.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Нормализирует величины.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.normalize.setText(QtGui.QApplication.translate("Form", "Normalize", None, QtGui.QApplication.UnicodeUTF8))
        self.normalize.setProperty("script", QtGui.QApplication.translate("Form", "LH.normalizeDepth()", None, QtGui.QApplication.UnicodeUTF8))
        self.normalize.setProperty("name", QtGui.QApplication.translate("Form", "normalize", None, QtGui.QApplication.UnicodeUTF8))
        self.normalize.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.copyTrackingDataToRoto.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Перебрасывает треккинг данные в рут рото(ротопеинт) ноды.<br/>Перед выделением нужны выделить:<br/>1) Tracker<br/>2) Roto<br/>3) Root поле в ноде roto.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.copyTrackingDataToRoto.setText(QtGui.QApplication.translate("Form", "Copy Tracking data to Roto", None, QtGui.QApplication.UnicodeUTF8))
        self.copyTrackingDataToRoto.setProperty("script", QtGui.QApplication.translate("Form", "Points3DToTracker.copyTrackingToRoto(True)", None, QtGui.QApplication.UnicodeUTF8))
        self.copyTrackingDataToRoto.setProperty("name", QtGui.QApplication.translate("Form", "copyTrackingToRoto", None, QtGui.QApplication.UnicodeUTF8))
        self.copyTrackingDataToRoto.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.cameraFromExr.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Перебрасывает треккинг данные в рут рото(ротопеинт) ноды.<br/>Перед выделением нужны выделить:<br/>1) Tracker<br/>2) Roto<br/>3) Root поле в ноде roto.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cameraFromExr.setText(QtGui.QApplication.translate("Form", "Camera From EXR", None, QtGui.QApplication.UnicodeUTF8))
        self.cameraFromExr.setProperty("script", QtGui.QApplication.translate("Form", "ExportAnimationFromEXR.CamExp()", None, QtGui.QApplication.UnicodeUTF8))
        self.cameraFromExr.setProperty("name", QtGui.QApplication.translate("Form", "copyTrackingToRoto", None, QtGui.QApplication.UnicodeUTF8))
        self.cameraFromExr.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsetLoaderGroup.setTitle(QtGui.QApplication.translate("Form", "Toolset loader", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsetLoaderCreate.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Выставляет выделенные ноды <span style=\" font-weight:600;\">горизонтально</span>.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsetLoaderCreate.setText(QtGui.QApplication.translate("Form", "Toolset Create", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsetLoaderCreate.setProperty("script", QtGui.QApplication.translate("Form", "tlc = toolsets_loader.toolsetCreate()\ntlc.show()", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsetLoaderCreate.setProperty("name", QtGui.QApplication.translate("Form", "toolsetLoaderCreate", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsetLoaderCreate.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsetLoader.setToolTip(QtGui.QApplication.translate("Form", "<html><head/><body><p>Выставляет выделенные ноды <span style=\" font-weight:600;\">горизонтально</span>.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsetLoader.setText(QtGui.QApplication.translate("Form", "Toolset Loader", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsetLoader.setProperty("script", QtGui.QApplication.translate("Form", "scripts.lineupNodes()", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsetLoader.setProperty("name", QtGui.QApplication.translate("Form", "lineupHorizontally", None, QtGui.QApplication.UnicodeUTF8))
        self.toolsetLoader.setProperty("gifname", QtGui.QApplication.translate("Form", "giphy", None, QtGui.QApplication.UnicodeUTF8))

