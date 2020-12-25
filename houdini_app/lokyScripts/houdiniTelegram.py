def makeDailise():
	import os, shutil
    import subprocess as sp
	import datetime
    from modules.pyseq import pyseq
    date = datetime.datetime.now().strftime("%y-%m-%H-%M-%S")
	shotEnv = hou.getenv("SHOT")
	hip = hou.getenv("HIP")
	if shotEnv is None:
		print shotEnv
		#out_path = hou.ui.selectFile(title="Select project path", file_type=hou.fileType.Directory)
		out_path = hip.rsplit("/", 1)[0]+"/out/allDailies"
		print out_path
	else:
		out_path = shotEnv+"/out/allDailies"
	if not os.path.exists(out_path): 
		os.makedirs(out_path)
	hipname = hou.getenv("HIPNAME")
	out_file = hipname+'_'+date+".mov"
	shotNumber = hou.getenv("SN")
	mpg = "X:/app/win/ffmpeg/bin/ffmpeg"
	sequence_path = os.path.expanduser("~") + "/allDailies"
	try:
		os.stat(sequence_path)
	except:
		os.makedirs(sequence_path)
	#hou.hipFile.save(hip+"/dailiesHip/"+hipname+"_"+date, save_to_recent_files=False)
	if hou.ui.displayMessage('Would you like to save scene before daily?', buttons = ('Yes', 'No')) == 0:
		hou.hipFile.save(file_name=None, save_to_recent_files=True)
	fromPath = os.environ["HIPFILE"]
	toPath = hip+"/dailiesHip"
	try:
		os.stat(toPath)
	except:
		os.makedirs(toPath)
	shutil.copy(fromPath, toPath + "/" +hipname+"_"+date+".hip")
	hou.hscript("viewwrite -f $FSTART $FEND -r 1920 1080 -c -R current -q 3 Build.panetab1.world.persp1 " + "'"+sequence_path+"/dailies.$F.jpg'")

	seqs = pyseq.get_sequences(sequence_path)

	files = os.listdir(sequence_path)
	f = os.path.join(sequence_path, files[0]).replace("\\", "/")
	for s in seqs:
		print "SQ PATH: ", sequence_path
		print "SEQUENCE: ", (s.format('%h%p%t'))
		sq = os.path.join(sequence_path, s.format('%h%p%t'))
		# Create string command to create mov
		cmd = mpg + " -threads 8 -r 25 -start_number " + s.format('%s') + " -i " + sq + " -threads 8 -y -framerate 24 -c:v libx264 -pix_fmt yuv420p -preset ultrafast -crf 10 " + out_path + "/"+out_file
		sp.call(cmd, shell=True)
		files = os.listdir(sequence_path)
		for f in files:
			f_remov = os.path.join(sequence_path, f)
			if os.path.isfile(f_remov):
				os.remove(f_remov)

	deiliespath = "Deilies path - "+out_path + "/"+out_file
	print deiliespath
	finalpath = out_path + "/"+out_file
	return finalpath


def telegramRenderPath():
	import os, hou, datetime
	import subprocess as sp
    from modules.pyseq import pyseq
    #node = hou.node('/out/arnold1')
	node = hou.pwd()
	date = datetime.datetime.now().strftime("%y-%m-%H-%M-%S")
	shotEnv = hou.getenv("SHOT")
	hip = hou.getenv("HIP")
	if shotEnv is None:
		print shotEnv
		#out_path = hou.ui.selectFile(title="Select project path", file_type=hou.fileType.Directory)
		out_path = hip.rsplit("/", 1)[0]+"/out/allDailies"
		print out_path
	else:
		out_path = shotEnv+"/out/allDailies"
	if not os.path.exists(out_path): 
		os.makedirs(out_path)
	hipname = hou.getenv("HIPNAME")
	out_file = hipname+'_'+date+".mov"
	shotNumber = hou.getenv("SN")
	mpg = "X:/app/win/ffmpeg/bin/ffmpeg"

	parmVal = hou.parm(node.path()+"/ar_picture").evalAsString()
	#parmVal = "P:/rnd/sequences/rndA/sh000/render/arnold1/v001/sh000_arnold1_v001.1009.exr"
	sequence_path = os.path.split(parmVal)[0]
	seqs = pyseq.get_sequences(sequence_path)
	print seqs
	files = os.listdir(sequence_path)
	print files
	f = os.path.join(sequence_path, files[0]).replace("\\", "/")
	for s in seqs:
		sq = os.path.join(sequence_path, s.format('%h%p%t'))
		#cmd = mpg + " -threads 8 -r 25 -start_number " + s.format('%s') + " -i " + sq + " -threads 8 -y -framerate 24 -c:v libx264 -pix_fmt yuv420p -preset ultrafast -crf 10 " + out_path + "/"+out_file
		cmd = mpg + " -apply_trc bt709 -threads 8 -r 24 -start_number " + s.format('%s') + " -i " + sq + " -threads 8 -y -framerate 24 -c:v libx264 -pix_fmt yuv420p -vf scale=1280:720 -preset ultrafast -crf 16 " + out_path + "/" + out_file
		#iec61966_2_1
		sp.call(cmd, shell=True)
	finalpath = out_path + "/"+out_file
	return finalpath, node.name(), node.parm('version').eval()

	#-vf eg=gamma 2.2
def telegramMove(filePath=""):
	if len(filePath)>=0:
		import sys
		path = "X:/app/win/Pipeline/bot"
		if not path in sys.path:
			sys.path.append(path)
		import telegram
		tokenFile = open("X:/app/win/Pipeline/bot"+'/token.txt', 'r')
		tokenData = tokenFile.read()
		chatidFile = open("X:/app/win/Pipeline/bot"+'/chatid.txt', 'r')
		chatidData = chatidFile.read()
		bot = telegram.Bot(token=tokenData)
		filePath.replace("P:", "\\NAS\project")
		file = open(filePath, 'rb')
		bot.send_video(chatidData, file, width=99, height=51)
		bot.send_message(chat_id=chatidData, text="<i>Zacenite: "+filePath+"</i>", parse_mode=telegram.ParseMode.HTML)
		
		