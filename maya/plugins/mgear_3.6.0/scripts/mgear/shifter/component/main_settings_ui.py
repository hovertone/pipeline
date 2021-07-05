import mgear.core.pyqt as gqt
from mgear.vendor.Qt import QtCore, QtWidgets


class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(286, 527)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.mainSettings_groupBox = QtWidgets.QGroupBox(Form)
        self.mainSettings_groupBox.setTitle("")
        self.mainSettings_groupBox.setObjectName("mainSettings_groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.mainSettings_groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.name_label = QtWidgets.QLabel(self.mainSettings_groupBox)
        self.name_label.setObjectName("name_label")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.name_label)
        self.name_lineEdit = QtWidgets.QLineEdit(self.mainSettings_groupBox)
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.name_lineEdit)
        self.side_label = QtWidgets.QLabel(self.mainSettings_groupBox)
        self.side_label.setObjectName("side_label")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.side_label)
        self.side_comboBox = QtWidgets.QComboBox(self.mainSettings_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.side_comboBox.sizePolicy().hasHeightForWidth())
        self.side_comboBox.setSizePolicy(sizePolicy)
        self.side_comboBox.setObjectName("side_comboBox")
        self.side_comboBox.addItem("")
        self.side_comboBox.addItem("")
        self.side_comboBox.addItem("")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.side_comboBox)
        self.componentIndex_label = QtWidgets.QLabel(
            self.mainSettings_groupBox)
        self.componentIndex_label.setObjectName("componentIndex_label")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.componentIndex_label)
        self.componentIndex_spinBox = QtWidgets.QSpinBox(
            self.mainSettings_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.componentIndex_spinBox.sizePolicy().hasHeightForWidth())
        self.componentIndex_spinBox.setSizePolicy(sizePolicy)
        self.componentIndex_spinBox.setObjectName("componentIndex_spinBox")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.componentIndex_spinBox)
        self.conector_label = QtWidgets.QLabel(self.mainSettings_groupBox)
        self.conector_label.setObjectName("conector_label")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.conector_label)
        self.connector_comboBox = QtWidgets.QComboBox(
            self.mainSettings_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.connector_comboBox.sizePolicy().hasHeightForWidth())
        self.connector_comboBox.setSizePolicy(sizePolicy)
        self.connector_comboBox.setObjectName("connector_comboBox")
        self.connector_comboBox.addItem("")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.connector_comboBox)
        self.gridLayout_4.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.mainSettings_groupBox, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.host_label = QtWidgets.QLabel(self.groupBox)
        self.host_label.setObjectName("host_label")
        self.horizontalLayout_2.addWidget(self.host_label)
        self.host_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.host_lineEdit.setObjectName("host_lineEdit")
        self.horizontalLayout_2.addWidget(self.host_lineEdit)
        self.host_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.host_pushButton.setObjectName("host_pushButton")
        self.horizontalLayout_2.addWidget(self.host_pushButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 1)
        self.jointSettings_groupBox = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.jointSettings_groupBox.sizePolicy().hasHeightForWidth())
        self.jointSettings_groupBox.setSizePolicy(sizePolicy)
        self.jointSettings_groupBox.setObjectName("jointSettings_groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.jointSettings_groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.useJointIndex_checkBox = QtWidgets.QCheckBox(
            self.jointSettings_groupBox)
        self.useJointIndex_checkBox.setObjectName("useJointIndex_checkBox")
        self.horizontalLayout_5.addWidget(self.useJointIndex_checkBox)
        self.parentJointIndex_spinBox = QtWidgets.QSpinBox(
            self.jointSettings_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.parentJointIndex_spinBox.sizePolicy().hasHeightForWidth())
        self.parentJointIndex_spinBox.setSizePolicy(sizePolicy)
        self.parentJointIndex_spinBox.setMinimum(-1)
        self.parentJointIndex_spinBox.setMaximum(999999)
        self.parentJointIndex_spinBox.setProperty("value", -1)
        self.parentJointIndex_spinBox.setObjectName("parentJointIndex_spinBox")
        self.horizontalLayout_5.addWidget(self.parentJointIndex_spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.jointNames_label = QtWidgets.QLabel(self.jointSettings_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.jointNames_label.sizePolicy().hasHeightForWidth())
        self.jointNames_label.setSizePolicy(sizePolicy)
        self.jointNames_label.setMinimumSize(QtCore.QSize(0, 0))
        self.jointNames_label.setObjectName("jointNames_label")
        self.horizontalLayout.addWidget(self.jointNames_label)
        self.jointNames_pushButton = QtWidgets.QPushButton(
            self.jointSettings_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.jointNames_pushButton.sizePolicy().hasHeightForWidth())
        self.jointNames_pushButton.setSizePolicy(sizePolicy)
        self.jointNames_pushButton.setObjectName("jointNames_pushButton")
        self.horizontalLayout.addWidget(self.jointNames_pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.jointSettings_groupBox, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, 
            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.subGroup_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.subGroup_lineEdit.setObjectName("subGroup_lineEdit")
        self.horizontalLayout_3.addWidget(self.subGroup_lineEdit)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(gqt.fakeTranslate("Form", "Form", None, -1))
        self.name_label.setText(gqt.fakeTranslate("Form", "Name:", None, -1))
        self.side_label.setText(gqt.fakeTranslate("Form", "Side:", None, -1))
        self.side_comboBox.setItemText(
            0, gqt.fakeTranslate("Form", "Center", None, -1))
        self.side_comboBox.setItemText(
            1, gqt.fakeTranslate("Form", "Left", None, -1))
        self.side_comboBox.setItemText(
            2, gqt.fakeTranslate("Form", "Right", None, -1))
        self.componentIndex_label.setText(
            gqt.fakeTranslate("Form", "Component Index:", None, -1))
        self.conector_label.setText(
            gqt.fakeTranslate("Form", "Connector:", None, -1))
        self.connector_comboBox.setItemText(
            0, gqt.fakeTranslate("Form", "standard", None, -1))
        self.groupBox.setTitle(gqt.fakeTranslate(
            "Form", "Channels Host Settings", None, -1))
        self.host_label.setText(gqt.fakeTranslate("Form", "Host:", None, -1))
        self.host_pushButton.setText(gqt.fakeTranslate("Form", "<<", None, -1))
        self.jointSettings_groupBox.setTitle(
            gqt.fakeTranslate("Form", "Joint Settings", None, -1))
        self.useJointIndex_checkBox.setText(
            gqt.fakeTranslate("Form", "Parent Joint Index", None, -1))
        self.jointNames_label.setText(
            gqt.fakeTranslate("Form", "Joint Names", None, -1))
        self.jointNames_pushButton.setText(
            gqt.fakeTranslate("Form", "Configure", None, -1))
        self.groupBox_2.setTitle(gqt.fakeTranslate(
            "Form", "Custom Controllers Group", None, -1))
        self.subGroup_lineEdit.setToolTip(gqt.fakeTranslate("Form", "<html><head/><body><p>Name for a custom controllers Group (Maya set) for the component controllers.</p><p align=\"center\"><span style=\" font-weight:600;\">i.e</span>: Setting the name &quot;arm&quot; will create a sub group (sub set in Mayas terminology) with the name &quot;rig_arm_grp&quot;. This group will be under the &quot;rig_controllers_grp&quot;</p><p>Leave this option empty for the default behaviour.</p></body></html>", None, -1))

