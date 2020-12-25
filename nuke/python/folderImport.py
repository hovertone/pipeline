import os, nuke

def seqloader():
    topFolder = nuke.getFilename("Select Directory")

    for root, dirs, files in os.walk(topFolder):
        for dir in dirs:
                dir = os.path.join(root, dir)
                files = nuke.getFileNameList(dir)
                for seq in files:
                    if seq != 'Thumbs.db' and seq != '' :
                        try:
                            frames, end = seq.split('-')
                            frames, start = frames.split(' ')
                            end = int(end)
                            start = int(start)
                            path = os.path.join(dir, frames)
                            path = path.replace("\\","/")
                            nodename = frames[:-9]
                            # print "nodename : %s" %(nodename)
                            # print "frames : %s" %(path)
                            # print "start : %s" %(start)
                            # print "end : %s"  %(end)
                            fileNode = nuke.nodes.Read(file="%s" %(path),name=nodename)
                            fileNode.knob("first").setValue(start)
                            fileNode.knob("last").setValue(end)
                            fileNode.knob("on_error").setValue(3)
                        except ValueError:
                            break