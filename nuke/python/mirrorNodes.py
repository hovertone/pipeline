import nuke

def getNodeCenter(n):
    centerX = n.xpos() + n.screenWidth()/2
    centerY = n.ypos() + n.screenHeight()/2
    return (centerX, centerY)

def centerNodeByXY(n, centerX, centerY):

    n.setXYpos(centerX - n.screenWidth()/2, centerY - n.screenHeight()/2)


def mirrorNodes():
    if len(nuke.selectedNodes()) < 1:
        nuke.message("Select nodes to mirror.")
        return

    nodes = nuke.selectedNodes()
    sumX = 0
    sumY = 0
    for n in nodes:
        nX, nY = getNodeCenter(n)
        sumX += nX
        sumY += nY

    globalCenter = (sumX/len(nodes), sumY/len(nodes))



    for n in nodes:
        nX, nY = getNodeCenter(n)
        # d = nuke.createNode('Dot')
        # centerNodeByXY(d, nX, nY)
        centerNodeByXY(n, globalCenter[0] - (getNodeCenter(n)[0] - globalCenter[0]), n.ypos() + n.screenHeight()/2)
