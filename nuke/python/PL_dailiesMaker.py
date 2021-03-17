try:
    import os
    import nuke
    import subprocess as sp
    import shutil
    import random
    import glob
    from p_utils import telega
    import socket
    from pyseq import pyseq
    from PL_scripts import inPipeline, getPipelineAttrs
    from p_utils.movie_maker import produce_daily
    from p_utils.csv_parser_bak import projectDict
    from houdini_app.Loader import loader_preferences as prefs
except:
    pass

try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
except:
    from PySide import QtGui
    from PySide import QtCore

from time import gmtime, strftime

def makeCompDaily(project, seq, shot, auto=False):
    print '________________ IN MAKE COMP DAILY _____________________'
    drive = getPipelineAttrs()[0]
    comp_assetnames = os.listdir('%s/%s/sequences/%s/%s/comp/' % (drive, project, seq, shot))
    if len(comp_assetnames) == 0:
        print 'ERROR :: No assetnames in comp'
        return
    else:
        assetName = comp_assetnames[0] # HARDCODE
        sequence_path = '%s/%s/sequences/%s/%s/comp/%s/precomp/forDaily/' % (drive, project, seq, shot, assetName)
        if not os.path.exists(sequence_path):
            nuke.message('There is no FOR DAILY folder')
            return

        # ALL PATHS FOR DAILIES CREATION
        curTime = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        all_dailies_folder = '%s/%s/sequences/%s/%s/out/allDailies' % (drive, project, seq, shot)
        if not os.path.exists(all_dailies_folder): os.makedirs(all_dailies_folder)
        if auto:
            all_dailies_file = os.path.basename('%s_%s_%s_auto_' % (seq, shot, assetName) + curTime + '.mov')
        else:
            all_dailies_file = os.path.basename(nuke.root().name()).strip('.nk') + '_' + curTime + '.mov'
        all_dailies_path = all_dailies_folder + "/" + all_dailies_file

        main_dailies_folder = '%s/%s/sequences/%s/%s/out' % (drive, project, seq, shot)
        main_dailies_file = 'DAILIES_%s_comp.mov' % shot
        main_dailies_path = main_dailies_folder + "/" + main_dailies_file

        # REMOVE SOME .TMP FILES
        files_in_directory = os.listdir(sequence_path)
        filtered_files = [file for file in files_in_directory if file.endswith(".tmp")]
        for file in filtered_files:
            path_to_file = os.path.join(sequence_path, file)
            os.remove(path_to_file)
            print 'REMOVING .tmp FILE: %s' % path_to_file

        # GET SEQ
        seqs = pyseq.get_sequences(sequence_path)
        if len(seqs) > 1:
            nuke.message('There are to many sequences in folder.\nInache govorya, dve sekvencii c papke kakbe, bratok.')
            return

        s = seqs[0]
        sq = os.path.join(sequence_path, s.format('%h%p%t'))

        # CHECK FOR AVAILABILITY OF THE MAIN OUTPUT FILE OVERIDE
        try:
            if os.path.exists(main_dailies_folder):
                # file is not used by other application. So we can overwrite it
                # nuke.tprint('it exists')
                f = open(main_dailies_path, 'w')
                f.close()
                # nuke.tprint('can be written')
        except IOError:
            print '%s is in use by another application' % main_dailies_path
            return

        print 'Daily is in progress with movie_maker'
        produce_daily(sq, all_dailies_path)

        # DUPLICATE ALL DAILY TO MAIN OUT DAILY
        shutil.copy2(all_dailies_path, main_dailies_path)

        # COPY PATH TO CLIPBOARD
        clipboard = QtWidgets.QApplication.clipboard()
        fullPath = main_dailies_path
        clipboard.setText(fullPath)

        return all_dailies_path, main_dailies_path


def beginDailyProccess():
    # STARTUP EXCEPTIONS
    if not inPipeline():
        nuke.message('Not in Pipeline')
        return

    if [i for i in nuke.allNodes('Write') if 'forDaily' in i['file'].value()] == []:
        nuke.message('You need to create a DailyEXR Write node')

    # PIPELINE ATTRS ACQUISITION
    drive, project, seq, shot, assetName, ver = getPipelineAttrs()
    os.environ['SHOT'] = '%s/%s/sequences/%s/%s' % (drive, project, seq, shot)

    # SEQUENCE PATH ASSEMBLY
    sequence_path = '%s/%s/sequences/%s/%s/comp/%s/precomp/forDaily/' % (drive, project, seq, shot, assetName)
    if not os.path.exists(sequence_path):
        nuke.message('There is no FOR DAILY folder')
        return

    # ACTUAL MAKE DAILY MOVS
    all_dailies_path, main_out_path = makeCompDaily(project, seq, shot)

    # NUKE RESAVE
    curTime = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    currentPath = nuke.root().name()
    nkname = os.path.split(currentPath)[-1]
    dailynkPath = '%s/%s/sequences/%s/%s/comp/%s/dailiesComps/%s' % (drive, project, seq, shot, assetName, nkname[:-3] + '_' + curTime + '.nk')
    if not os.path.exists(os.path.dirname(dailynkPath)): os.makedirs(os.path.dirname(dailynkPath))
    nuke.scriptSaveAs(dailynkPath, 1)
    nuke.scriptSaveAs(currentPath, 1)

    # OPEN DAILY WITH RV
    sp.Popen([r"X:\app\win\rv\rv7.1.1\bin\rv.exe", all_dailies_path])

    # OUTPUT MESSAGE AND TELEGRAM REPORT
    phrases = ['Vot eto tu harosh!', 'Mozhet ne nado tak zhossko?', 'Vou Vou, polegche!', 'Teper v mire na odin topovuj deiliz bolshe!', 'A smotrel(a) chto poluchilos?', 'Da pribudet s toboi sila!' , "Tak derzhat'! Rabotaem."]
    if nuke.ask('Daily done! %s\nZapostim eto v telegy?' % phrases[random.randrange(len(phrases))]):
        print 'OUT OUT %s' % (all_dailies_path)
        telega.telegramReport(filePath = all_dailies_path, tp = 'comp')



def createDailyWrite():
    drive, project, seq, shot, assetName, ver = getPipelineAttrs()
    path = '%s/%s/sequences/%s/%s/out/DAILIES_%s_comp.mov' % (drive, project, seq, shot, shot)
    w = nuke.createNode('Write')
    w['channels'].setValue('rgb')
    w['file'].setValue(path)
    w['colorspace'].setValue('Output - Rec.709')
    w['file_type'].setValue('mov')
    w['meta_codec'].setValue('apcn')
    return w

def createEXRforDaily():
    drive, project, seq, shot, assetName, ver = getPipelineAttrs()
    path = '%s/%s/sequences/%s/%s/comp/%s/precomp/forDaily/%s_%s_forDaily.####.exr' % (drive, project, seq, shot, assetName, seq, shot)
    w = nuke.createNode('Write')
    w['channels'].setValue('rgb')
    w['file'].setValue(path)
    w['colorspace'].setValue('Output - Rec.709')
    return w

def createProxyStill(n = None):
    drive, project, seq, shot, assetname, ver = getPipelineAttrs()
    path = '%s/%s/sequences/%s/%s/comp/%s/precomp/forDaily/%s_%s_forDaily.%s.exr' % (drive, project, seq, shot, assetname, seq, shot, str(int(nuke.root()['first_frame'].value())))
    if n == None:
        ww = nuke.thisNode()
    else:
        ww = n

    # if ww.dependencies() != []:
    #     tn = ww.dependencies()[0]
    # else:
    #     nuke.message('Daily write has to be connected to Read node')
    #     return None

    read = nuke.createNode('Read')
    read['postage_stamp'].setValue(False)
    read['file'].setValue(path)
    read['colorspace'].setValue('Output - Rec.709')

    ref = nuke.createNode('Reformat')
    ref.setInput(0, read)
    ref['type'].setValue('to box')
    ref['box_fixed'].setValue(True)
    ref['box_width'].setValue(512)
    ref['box_height'].setValue(288)

    w = nuke.createNode('Write')
    w.setInput(0, ref)
    p = '%s/%s/sequences/%s/%s/out/proxy/proxy.jpg' % (drive, project, seq, shot)
    w['file'].setValue(p)
    nuke.execute(w.name(), int(nuke.root()['first_frame'].value()), int(nuke.root()['first_frame'].value()))
    nuke.delete(w)
    nuke.delete(ref)
    nuke.delete(read)
    return True

def sequenceDailies(project, seq):
    print 'IN MAIN OF SEQUENCE DAILY'
    d = projectDict(project)
    shots = d.getShots(seq)
    shots.pop(shots.index('sh000'))
    shots = sorted(shots)
    print 'BEGINING TO DO SHOTS: %s' % str(shots)

    for s in shots:
        print 'doing comp daily for %s' % s
        makeCompDaily(project, seq, s, auto = True)

def masterDaily():
    drive, project, seq, shot, assetname, ver = getPipelineAttrs()
    w_list = [n for n in nuke.allNodes('Write') if '%s/precomp/forDaily' % (assetname) in n['file'].value()]
    if len(w_list) == 0:
        #w = createDailyWrite()
        createEXRforDaily()
        return
    else:
        createProxyStill(w_list[-1])
        beginDailyProccess()