import nuke
from CUF import selectOnly

def branch():
  nodesToBranch = nuke.selectedNodes()
       #  ### depNodes ### === {n.name():[dependencie1, dependencie2 ...]}, {...}}
                                   #  ## dep2Nodes ### === {n.name():{dep:[dep.input(^dependent of our n node^)]}, {...}}
  connections = dict()
  for n in nodesToBranch:
    dependecies = n.dependencies()
    depNodes, dep2Nodes = [], []
    for nInp in range(n.inputs()):
      if n.input(nInp) in dependecies:
        depNodes.append((nInp, n.input(nInp)))

    for dep in n.dependent():
      for depInp in range(dep.inputs()):
        #print 'checking %s input' % depInp
        if dep.input(depInp) == n:
          #print '%s input of %s node points to %s' % (depInp, dep.name(), n.name())
          dep2Nodes.append((depInp, dep))

    connections[n.name()] = (depNodes, dep2Nodes)

  #print connections

  for n in nodesToBranch:
    selectOnly(n)
    nuke.nodeCopy("%clipboard%")
    selectOnly()
    copy = nuke.nodePaste("%clipboard%")

    dependencies, dependent = connections[n.name()][0], connections[n.name()][1]
    #print dependencies, '\n', dependent
    for dep in dependencies:
      copy.setInput(dep[0], dep[1])

    for dep in dependent:
      dep[1].setInput(dep[0], n)    

    copy.setXYpos(n.xpos() + copy.screenWidth() + 40, n.ypos() + 80)

# def isNodeInCoord(coord = )

# def spawnDots(coords):
#     print type(coords)
#     if type(coords) == list or type(coords) == set or type(coords) == set:
#         print 'y'

# coords = [(-193, 195), (-100, 135), (-113, 165), (-173, 115)]
# #print type(crd)
# spawnDots(coords)



