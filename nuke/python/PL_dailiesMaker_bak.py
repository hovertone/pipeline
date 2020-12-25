import os
import nuke
import subprocess as sp
import shutil
import random
import glob
import telega
import socket
from pyseq import pyseq
from PL_scripts import inPipeline, getPipelineAttrs
from p_utils.csv_parser_bak import projectDict
from houdini_app.Loader import loader_preferences as prefs

from PySide import QtGui
from time import gmtime, strftime

def sendTelegramMessage(filePath):
    #filePath = "P:/Raid/sequences/absentPlayer2/sh050/out/DAILIES_sh050_comp.mov"

    import sys
    path = "X:/app/win/Pipeline/bot"
    if not path in sys.path:
        sys.path.append(path)
    import telegram
    tokenFile = open("X:/app/win/Pipeline/bot" + '/token.txt', 'r')
    tokenData = tokenFile.read()
    chatidFile = open("X:/app/win/Pipeline/bot" + '/chatid.txt', 'r')
    chatidData = chatidFile.read()
    bot = telegram.Bot(token=tokenData)
    filePath.replace("P:", "\\NAS\project")
    file = open(filePath, 'rb')

    #chatidData = "-331612623"   # TEST
    shot = filePath.split('/')[4]
    #print shot
    bot.send_video(chatidData, file, width=99, height=56, caption='<b>%s</b> COMP' % shot.upper(), parse_mode=telegram.ParseMode.HTML)
    #bot.send_message(chat_id=chatidData, text="<i>Testing: "+filePath+"</i>", parse_mode=telegram.ParseMode.HTML)

def makeDailyFromRead():
    dev = False

    # VAR FOR DEVELOPMENT PURPOSES
    if socket.gethostname() == 'sashok':
        dev = True

    if not inPipeline():
        nuke.message('Not in Pipeline')
        return

    if [i for i in nuke.allNodes('Write') if 'forDaily' in i['file'].value()] == []:
        nuke.message('You need to create a DailyEXR Write node')

    mpg = "X:/app/win/ffmpeg/bin/ffmpeg"
    drive, project, seq, shot, assetName, ver = getPipelineAttrs()

    d = projectDict(project)
    #sequence_path = '%s/%s/sequences/%s/%s/out/hires/' % (drive, project, seq, shot)
    #sequence_path = 'P:/Raid/sequences/absentPlayer2/sh050/comp/mainComp/precomp/forDaily'
    sequence_path = '%s/%s/sequences/%s/%s/comp/%s/precomp/forDaily/' % (drive, project, seq, shot, assetName)
    if not os.path.exists(sequence_path):
        nuke.message('There is no FOR DAILY folder')
        return
    # if len(os.listdir(sequence_path)) != int(d.getSpecificShotData(seq, shot, 'last_frame')) - int(d.getSpecificShotData(seq, shot, 'first_frame')) + 1:
    #     nuke.message("Malo frejmov")
    #     return

    curTime = strftime("%Y-%m-%d_%H-%M-%S", gmtime())

    out_path_daily = '%s/%s/sequences/%s/%s/out/allDailies' % (drive, project, seq, shot)
    if not os.path.exists(out_path_daily): os.makedirs(out_path_daily)
    out_path_daily_ftrack = 'P:/%s/sequences/%s/%s/out' % (project, seq, shot)
    out_file = os.path.basename(nuke.root().name()).strip('.nk') + '_' + curTime + '.mov'
    out_file_ftrack = 'DAILIES_%s_comp.mov' % shot

    w_list = [n for n in nuke.allNodes('Write') if '_forDaily' in n['file'].value()]
    if w_list[0].dependencies() != []:
        tn = w_list[0].dependencies()[0]
    else:
        nuke.message('Daily write has to be connected to Read node')
        return None

    okValues = [1080.0, 1920.0, 3200.0, 1800.0]
    # if tn.bbox().h() not in okValues or tn.bbox().w() not in okValues:
    #     nuke.message('Proebalsya bbox. Peredelyvaem!\n%s %s' % (tn.bbox().h(), tn.bbox().w()))
    #     return

    seqs = pyseq.get_sequences(sequence_path)
    if len(seqs) > 1:
        nuke.message('There are to many sequences in folder.\nInache govorya, dve sekvencii c papke kakbe, bratok.')
        return

    s = seqs[0]
    sq = os.path.join(sequence_path, s.format('%h%p%t'))

    # CHECK FOR AVAILABILITY OF THE OUTPUT FILE
    try:
        if os.path.exists(out_path_daily_ftrack + "/"+out_file_ftrack):
            # file is not used by other application. So we can overwrite it
            #nuke.tprint('it exists')
            f = open(out_path_daily_ftrack + "/"+out_file_ftrack, 'w')
            f.close()
            #nuke.tprint('can be written')
    except IOError:
        nuke.message('%s is in use by another application' % (out_path_daily_ftrack + "/"+out_file_ftrack))
        return

    # SOUND
    soundFolder = '%s/%s/sequences/%s/%s/sound/' % (drive, project, seq, shot)
    if os.path.exists(soundFolder):
        files = filter(os.path.isfile, glob.glob(soundFolder + "*.wav"))
        files.sort(key=lambda x: os.path.getmtime(x))
        lastSoundFile = files[-1].replace('\\', '/')
    else:
        print 'There is no folder for sound'
        lastSoundFile = False

    print 'Daily is in progress...'
    # Create string command to create mov
    if lastSoundFile:
        cmd = mpg + " -threads 8 -r 24 -i " + lastSoundFile + " -start_number " + s.format('%s') + " -i " + sq + " -threads 8 -y -framerate 24 -c:v libx264 -pix_fmt yuv420p -vf scale=1920:1080 -preset ultrafast -crf 20 " + out_path_daily + "/"+out_file
    else:
        cmd = mpg + " -threads 8 -r 24 -start_number " + s.format(
            '%s') + " -i " + sq + " -threads 8 -y -framerate 24 -c:v libx264 -pix_fmt yuv420p -vf scale=1920:1080 -preset ultrafast -crf 20 " + out_path_daily + "/" + out_file
    #-vf lutrgb=r=gammaval(0.45454545):g=gammaval(0.45454545):b=gammaval(0.45454545)

    # DEV TESTS
    # if dev:
    #     nuke.tprint(cmd)
    #     return

    nuke.tprint(cmd)
    sp.call(cmd, shell=True)

    #print '%s done' % out_file

    # NUKE RESAVE
    currentPath = nuke.root().name()
    nkname = os.path.split(currentPath)[-1]
    dailynkPath = '%s/%s/sequences/%s/%s/comp/%s/dailiesComps/%s' % (drive, project, seq, shot, assetName, nkname[:-3] + '_' + curTime + '.nk')
    if not os.path.exists(os.path.dirname(dailynkPath)): os.makedirs(os.path.dirname(dailynkPath))
    nuke.scriptSaveAs(dailynkPath, 1)
    #print '%s saved to DAILY' % dailynkPath
    nuke.scriptSaveAs(currentPath, 1)
    #print '%s saved BACK' % currentPath

    shutil.copy2(out_path_daily + "/"+out_file, out_path_daily_ftrack + "/"+out_file_ftrack)

    cmd = mpg + " -threads 8 -r 25 -start_number " + s.format('%s') + " -i " + sq + " -threads 8 -y -framerate 25 -c:v libx264 -pix_fmt yuv420p -preset ultrafast -crf 10 " + out_path_daily_ftrack + "/"+out_file_ftrack
    #sp.call(cmd, shell=True)
    #print '%s done' % out_file_ftrack

    # COPY PATH TO CLIPBOARD
    clipboard = QtGui.QApplication.clipboard()
    fullPath = out_path_daily_ftrack + "/"+out_file_ftrack
    clipboard.setText(fullPath)

    sp.Popen([r"X:\app\win\rv\rv7.1.1\bin\rv.exe", fullPath])

    phrases = ['Vot eto tu harosh!', 'Mozhet ne nado tak zhossko?', 'Vou Vou, polegche!', 'Teper v mire na odin topovuj deiliz bolshe!', 'A smotrel(a) chto poluchilos?', 'Da pribudet s toboi sila!' , "Tak derzhat'! Rabotaem."]
    if nuke.ask('Daily done! %s\nZapostim eto v telegy?' % phrases[random.randrange(len(phrases))]):
        telega.telegramReport(filePath = out_path_daily +"/"+ out_file, tp = 'comp')
        #sendTelegramMessage()



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
    if n == None:
        ww = nuke.thisNode()
    else:
        ww = n

    if ww.dependencies() != []:
        tn = ww.dependencies()[0]
    else:
        nuke.message('Daily write has to be connected to Read node')
        return None

    ref = nuke.createNode('Reformat')
    ref.setInput(0, tn)
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
    return True

def masterDaily():
    w_list = [n for n in nuke.allNodes('Write') if '_forDaily' in n['file'].value()]
    if len(w_list) == 0:
        #w = createDailyWrite()
        createEXRforDaily()
        return
    else:
        createProxyStill(w_list[-1])
        makeDailyFromRead()

    #print w.name()
