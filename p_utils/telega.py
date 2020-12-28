import os
import sys
import re
path = os.environ["PIPELINE_ROOT"] + "/modules/bot"
if not path in sys.path:
    sys.path.append(path)
import telegram
import socket
try:
    import hou
except:
    pass
reload(telegram)
from time import gmtime, strftime

def telegramReport(filePath, tp, args = None):
    '''
    tpS : 'anim', 'cache', 'fx', 'render', 'comp'
    argsL : file path, node name, version, user name
    '''

    tokenFile = open(path + '/token.txt', 'r')
    tokenData = tokenFile.read()
    chatidFile = open(path + '/chatid.txt', 'r')
    chatidData = chatidFile.read()
    bot = telegram.Bot(token=tokenData)
    usr = socket.gethostname().lower()

    curTime = strftime("%H", gmtime())
    hour = int(curTime)
    if hour > 23 and hour < 11:
        #print 'ne vremya pilikat'
        notification = False
    else:
        #print 'mozhno i popilikat'
        notification = True

    #thunderstorm = u'\U0001F4A8'  # Code: 200's, 900, 901, 902, 905
    if args != None and 'dev' in args:# or socket.gethostname() == 'sashok':
        print 'IN DEV'
        chatidData = "-331612623"   # DEV

    project = os.environ['SHOT'].split('/')[1]
    shot = os.environ['SHOT'].split('/')[4]
    seq = os.environ['SHOT'].split('/')[3]
    if tp == 'anim':
        cap = '%s :: %s :: %s :: <b> ANIM by %s </b>' % (project, seq, shot.upper(), usr)
    elif tp == 'cache':
        if 'assetBuilds' in filePath:
            #"P:\Raid\assetBuilds\char\skeleton\main\geo\v016\skeleton_main_v016.abc"
            assetType = filePath.split('/')[3]
            assetName = filePath.split('/')[4]
            assetComponent = filePath.split('/')[5]
            ver = filePath.split('/')[7]
            cap = '%s :: <b> ASSETBUILDS </b> :: <i> %s %s %s %s by %s</i>' % (project, assetType, assetName, assetComponent, ver, usr)
        else:
            asset = filePath.split('/')[7]
            ver = filePath.split('/')[9]
            cap = '%s :: %s :: %s :: <b> CACHE </b> :: <i> %s %s by %s </i>' % (project, seq, shot.upper(), asset, ver, usr)

        bot.send_message(chat_id=chatidData, text= cap, parse_mode=telegram.ParseMode.HTML, disable_notification = not notification)
        return # EXIT
    elif tp == 'houdini':
        f = os.path.split(filePath)[1]
        result = re.search('sh\d{3}\_(\w+)\_(\w+)\_(v\d{3})', f)
        print '%s\n%s' % (f, result)
        if result:
            print 'there is result'
            if '/fx/' in hou.hipFile.path():
                cap = '%s :: %s :: %s :: <b> FX </b> :: <i> %s %s by %s </i>' % (project, seq, shot.upper(), result.group(1), result.group(3), usr)
            elif '/light/' in hou.hipFile.path():
                cap = '%s :: %s :: %s :: <b> LIGHT </b> :: <i> %s %s by %s </i>' % (project, seq, shot.upper(), result.group(1), result.group(3), usr)
            elif '/model/' in hou.hipFile.path():
                cap = '%s :: %s :: %s :: <b> MODEL </b> :: <i> %s %s by %s </i>' % (project, seq, shot.upper(), result.group(1), result.group(3), usr)
            else:
                print 'Unknown scene type'
        else:
            cap = '%s :: %s :: %s :: <b> HOUDINI DAILIES by %s </b>' % (project, seq, shot.upper(), usr)
    elif tp == 'render':
        if args[2]:
            usr = args[2]
            cap = '%s :: %s :: %s :: <b> RENDER </b> :: <i> %s v%s by %s </i>' % (project, seq, shot.upper(), args[0], str(args[1]).zfill(3), usr.lower())
        else:
            cap = '%s :: %s :: %s :: <b> RENDER </b>' % (project, seq, shot.upper())
    elif tp == 'comp':
        cap = '%s :: %s :: %s :: <b> COMP by %s </b>' % (project, seq, shot.upper(), usr)
    elif tp == 'cam':
        cap = '%s :: %s :: %s :: <b> CAMERA v%s by %s </b>' % (project, seq, shot.upper(), args[0], usr)
        bot.send_message(chat_id=chatidData, text=cap, parse_mode=telegram.ParseMode.HTML,
                         disable_notification=not notification)
        return  # EXIT
    filePath.replace("P:", "\\NAS\project")
    file = open(filePath, 'rb')

    bot.send_video(chatidData, file, width=99, height=56, caption=cap, parse_mode=telegram.ParseMode.HTML, disable_notification = not notification)
    #bot.send_message(chat_id=chatidData, text= cap, parse_mode=telegram.ParseMode.HTML)

def telegramRenderPath():
    import os, hou, datetime
    import subprocess as sp
    from modules.pyseq import pyseq
    # node = hou.node('/out/arnold1')


    if hou.isUIAvailable():
        if len(hou.selectedNodes()) > 0:
            node = hou.selectedNodes()[0]
        else:
            hou.ui.displayMessage('Select ROP node')
            raise Exception('No ROP selected')
    else:
        node = hou.pwd()

    date = datetime.datetime.now().strftime("%y-%m-%H-%M-%S")
    shotEnv = hou.getenv("SHOT")
    hip = hou.getenv("HIP")
    if shotEnv is None:
        print shotEnv
        # out_path = hou.ui.selectFile(title="Select project path", file_type=hou.fileType.Directory)
        out_path = hip.rsplit("/", 1)[0] + "/out/allDailies"
        print out_path
    else:
        out_path = shotEnv + "/out/allDailies"
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    hipname = hou.getenv("HIPNAME")
    out_file = hipname + '_' + date + ".mov"
    shotNumber = hou.getenv("SN")
    mpg = "X:/app/win/ffmpeg/bin/ffmpeg"


    parmVal = hou.parm(node.path() + "/ar_picture").evalAsString()
    # parmVal = "P:/rnd/sequences/rndA/sh000/render/arnold1/v001/sh000_arnold1_v001.1009.exr"
    sequence_path = os.path.split(parmVal)[0]
    seqs = pyseq.get_sequences(sequence_path)
    print seqs
    files = os.listdir(sequence_path)
    print files
    f = os.path.join(sequence_path, files[0]).replace("\\", "/")
    for s in seqs:
        sq = os.path.join(sequence_path, s.format('%h%p%t'))
        # cmd = mpg + " -threads 8 -r 25 -start_number " + s.format('%s') + " -i " + sq + " -threads 8 -y -framerate 24 -c:v libx264 -pix_fmt yuv420p -preset ultrafast -crf 10 " + out_path + "/"+out_file
        cmd = mpg + " -apply_trc bt709 -threads 8 -r 24 -start_number " + s.format(
            '%s') + " -i " + sq + " -threads 8 -y -framerate 24 -c:v libx264 -pix_fmt yuv420p -vf scale=1280:720 -preset ultrafast -crf 16 " + out_path + "/" + out_file
        # iec61966_2_1
        sp.call(cmd, shell=True)
    finalpath = out_path + "/" + out_file
    return finalpath, node.name(), node.parm('version').eval(), hou.getenv('USER').lower() #path, node name, version, user name

def afterRenderReport():
    pass

def simpleMyReport(text):
    tokenFile = open("X:/app/win/Pipeline/bot" + '/token.txt', 'r')
    tokenData = tokenFile.read()
    chatidFile = open("X:/app/win/Pipeline/bot" + '/chatid.txt', 'r')
    chatidData = "-331612623"
    bot = telegram.Bot(token=tokenData)
    #usr = socket.gethostname().lower()
    bot.send_message(chat_id=chatidData, text=text, parse_mode=telegram.ParseMode.HTML)