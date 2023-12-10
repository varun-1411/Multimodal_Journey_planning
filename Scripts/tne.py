import sys
class arc:
    def __init__(self,tailnode:int,headnode:int):
        self.tailnode = tailnode
        self.headnode = headnode

arcs = dict()
arcs[1] = arc(1,3)
arcs[2] = arc(1,2)
arcs[3] = arc(2,3)
arcs[4] = arc(2,4)
arcs[5] = arc(3,4)
arcs[6] = arc(3,5)
arcs[7] = arc(5,4)
arcs[8] = arc(5,6)
arcs[9] = arc(4,6)

class Node:
  def __init__(self, nodeNumber):
    self.nodeNumber = nodeNumber
    self.adjNodes = []
    self.adjArcs = []
    self.dist = sys.maxsize
    self.parNode = -1
    self.predArc = 0
    self.indegree = 0
    self.vi = 0

  def addAdjNode(self, node):
    self.adjNodes.append(node)

  def addAdjArcs(self, n):
    self.adjArcs.append(n)

nodes = dict()
for key in arcs:
  if not arcs[key].tailnode in nodes:
    nodes[arcs[key].tailnode] = Node(arcs[key].tailnode)
  nodes[arcs[key].tailnode].addAdjNode(arcs[key].headnode)
  nodes[arcs[key].tailnode].addAdjArcs(key)
nodes[6] = Node(6)
nodes[6].adjArcs
arcs[1].headnode

for key in nodes:
    for i in nodes[key].adjNodes:
        nodes[i].indegree += 1
        print(i,nodes[i].indegree)

SEL = []
order = 0
for key in nodes:
    if nodes[key].indegree == 0:
        SEL.append(key)
SEL
while len(SEL) !=0:
    key = SEL[0]
    SEL.remove(key)
    order = order +1
    nodes[key].vi = order
    for j in nodes[key].adjNodes:
        nodes[j].indegree = nodes[j].indegree - 1
        if nodes[j].indegree == 0:
            SEL.append(j)

for key in nodes:
    print(key,nodes[key].vi)







