def fillShotsPart(self, project):
    # project = 'rnd3'

    self.projectFrame = QtGui.QGroupBox(self)
    self.projectFrame.setTitle(project)

    self.grid = QtGuiWidgets.QGridLayout()
    self.column_counter = 0
    self.row_counter = 0

    self.d = csv_parser.projectDict(project)
    # shots = self.projectShotsFromFile(project)
    for seq in self.d.getSequences():
        seq_grid = QtGuiWidgets.QGridLayout()
        for shot in self.d.getShots(seq):
            button = ShotButton(shot, project, seq, 0)
            button.clicked.connect(self.openShotScript, )
            # nuke.tprint('%s %s' % (self.row_counter, self.column_counter))
            seq_grid.addWidget(button, self.row_counter, self.column_counter)
            self.column_counter += 1
        self.grid.addWidget(seq_grid)
        # self.row_counter += 1

        # if i != len(shots)-1:
        #     if int(shots[i+1]) - int(shots[i]) > 10:
        #         self.row_counter += 1
        #         self.column_counter = 0
        #     else:
        #         self.column_counter += 1
    self.projectFrame.setLayout(self.grid)
    self.masterLayout.addWidget(self.projectFrame)
    #==========================================================================

    self.projectFrame = QtGui.QGroupBox(self)
    self.projectFrame.setTitle(project)

    self.projectLayout = QtGuiWidgets.QVBoxLayout()
    self.projectFrame.setLayout(self.projectLayout)

    button = ShotButton('shot', project, 'seq', 0)
    button.clicked.connect(self.openShotScript, )
    self.projectLayout.addWidget(button)

    self.masterLayout.addWidget(self.projectFrame)
    #==========================================================================
    # self.seqFrame1 = QtGui.QGroupBox('seq')
    # self.seqLayout1 = QtGui.QHBoxLayout()
    # self.pb = QtGui.QPushButton('asdf')
    # self.seqLayout1.addWidget(self.pb)
    # self.pb2 = QtGui.QPushButton('hdg')
    # self.seqLayout1.addWidget(self.pb2)
    # self.projectLayout.addWidget(self.seqFrame1)
    #
    # self.seqFrame1.setLayout(self.seqLayout1)
    # self.projectFrame.setLayout(self.projectLayout)

    import PL_dailiesMaker
    reload(PL_dailiesMaker)
    PL_dailiesMaker.makeDailyFromRead()
