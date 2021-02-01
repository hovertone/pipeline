print 'in mirror frames'
import hou

def getFrame(l):
    return l[0]

def main():
    channel_editor = hou.ui.paneTabOfType(hou.paneTabType.ChannelEditor)
    chg = channel_editor.graph()

    keyframes = channel_editor.graph().selectedKeyframes()  # get the graph's selected keyframes in a dict called keyframes
    print 'KEYS ARE %s' % str(keyframes)

    for parm in keyframes.keys():
        print 'parm is %s' % parm.name()
        keys_amount = len(parm.keyframes())

        # copy old values
        oldValues = list()
        for key in keyframes[parm]:
            oldValues.append(key.value())
        #print 'oldvalues %s' % str(oldValues)
        #reverse list
        oldValues_rev = oldValues[::-1]
        #print 'oldvalues rev %s' % str(oldValues_rev)

        print 'in for loop'
        for i, key in enumerate(keyframes[parm]):

            frame = key.time() * hou.fps() + 1
            print 'frame is %s' % frame
            #mk = key
            key.setFrame(frame)
            key.setValue(oldValues_rev[i])
            try:
                #parm.deleteKeyframeAtFrame(frame)
                parm.setKeyframe(key)
            except:
                print 'EXCEPTION'

