import hou

def getMostUpperInputNode(node):
    def askFurther(n):
        global s
        #print '\t %s inputs: %s' % (n.name(), n.inputs())
        #print len(n.inputs())
        if len(n.inputs()) == 0:
            s = n
        else:
            #print '%s node has inputs. Going in' % n.name()
            askFurther(n.inputs()[0])

    askFurther(node)
    return s


