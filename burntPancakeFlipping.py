import copy
import sys

def flip_pancake(pancake, range):
    strlist = list(pancake)
    endlist = copy.deepcopy(strlist)
    if range is 2:
        if strlist[1] == 'b':
            endlist[1] = 'w'
        else:
            endlist[1] = 'b'
    elif range is 4:
        endlist[0] = strlist[2]
        endlist[2] = strlist[0]
        if strlist[1] is 'b':
            endlist[3] = 'w'
        else:
            endlist[3] = 'b'
        if strlist[3] is 'b':
            endlist[1] = 'w'
        else:
            endlist[1] = 'b'
    elif range is 6:
        endlist[0] = strlist[4]
        endlist[4] = strlist[0]
        if strlist[1] is 'b':
            endlist[5] = 'w'
        else:
            endlist[5] = 'b'
        if strlist[3] is 'b':
            endlist[3] = 'w'
        else:
            endlist[3] = 'b'
        if strlist[5] is 'b':
            endlist[1] = 'w'
        else:
            endlist[1] = 'b'
    elif range is 8:
        endlist[0] = strlist[6]
        endlist[6] = strlist[0]
        endlist[2] = strlist[4]
        endlist[4] = strlist[2]
        if strlist[1] is 'b':
            endlist[7] = 'w'
        else:
            endlist[7] = 'b'
        if strlist[3] is 'b':
            endlist[5] = 'w'
        else:
            endlist[5] = 'b'
        if strlist[5] is 'b':
            endlist[3] = 'w'
        else:
            endlist[3] = 'b'
        if strlist[7] is 'b':
            endlist[1] = 'w'
        else:
            endlist[1] = 'b'

    #print(''.join(endlist))
    return ''.join(endlist)

class BfsNode:
    def __init__(self, pancake):
        self.pancake = pancake
        self.parent = None
        self.flipcost = 0


def bfs(pancake):
    cost = 0
    visited = []
    start = BfsNode(pancake)
    fringe = [start]
    while fringe[0].pancake != '1w2w3w4w':
        #print(fringe[0].pancake)
        if fringe[0].pancake in visited:
            fringe.pop(0)
            continue
        for i in range(2,9,2):
            flip = flip_pancake(fringe[0].pancake, i)
            if flip in visited:
                continue
            newChild = BfsNode(flip)
            newChild.parent = fringe[0]
            newChild.flipcost = i//2
            cost += i//2
            #print(flip[:i] + '|' + flip[i:] + ',', 'Flip Cost: ' + str(i//2) + ',', 'Total Cost: ' + str(cost))
            fringe.append(newChild)
        visited.append(fringe[0].pancake)
        fringe.pop(0)
    goalNode = fringe[0]
    #print(goalNode)
    #print(goalNode.parent)
    finalList = []
    leastFlips = 0
    while goalNode.parent is not None:
        finalList.insert(0, goalNode)
        leastFlips += goalNode.flipcost
        goalNode.parent.childcost = goalNode.flipcost
        goalNode.parent.split = goalNode.flipcost * 2
        goalNode = goalNode.parent
    finalList.insert(0, goalNode)
    for node in finalList:
        try:
            print(node.pancake[:node.split] + '|' + node.pancake[node.split:], node.childcost)
        except:
            print(node.pancake)
        #print(node.pancake[:node.flipcost*2] + '|' + node.pancake[node.flipcost*2:], node.flipcost)
    print('Least Flips to find solution:', leastFlips)
    print('Total Flips during search:', cost)
    print('Total new nodes visited during search:', len(visited))

class AstarNode:
    def __init__(self, pancake, flipLocation=0):
        self.pancake = pancake
        self.parent = None
        self.flipLocation = flipLocation
        self.g = 0
        self.h = self.heuristic()
        self.f = self.g + self.h

    def heuristic(self):
        max_pancake = 0
        totalb = 0
        if int(self.pancake[0]) is not 1:
            max_pancake = 1
        if int(self.pancake[2]) is not 2:
            max_pancake = 2
        if int(self.pancake[4]) is not 3:
            max_pancake = 3
        if int(self.pancake[6]) is not 4:
            max_pancake = 4
        for i in range(1, 8, 2):
            if self.pancake[i] is 'b':
                totalb += 1
        return max(max_pancake, totalb)

    def getG(self, flips):
        self.g = self.parent.g + flips
        self.f = self.g + self.h

def tiebreak(minlist, openlist):
    d = {}
    for i in minlist:
        tmp = openlist[i].pancake
        tmp = tmp.replace('w', '1')
        tmp = tmp.replace('b', '0')
        d[i] = int(tmp)
    maxkey = 0
    maxval = 0
    for key, val in d.items():
        if val > maxval:
            maxval = val
            maxkey = key
    #print(openlist[maxkey])
    return openlist.pop(maxkey)

def minf(openlist):
    min = 0
    minList = [0]
    for i in range(len(openlist)):
        if openlist[i].f < openlist[min].f:
            minList = [i]
            min = i
        elif openlist[i].f == openlist[min].f:
            minList.append(i)
    if len(minList) > 1:
        #print('tie break')
        return tiebreak(minList, openlist)
    else:
        return openlist.pop(min)



def aStar(pancake):
    openlist = [AstarNode(pancake)]
    closedset = set()
    solutionNode = None
    while solutionNode is None:
        #print([i.pancake for i in openlist])
        current = minf(openlist)
        #print([i.pancake for i in openlist])
        #print('Node:', current.pancake)
        for i in range(2,9,2):
            flip = flip_pancake(current.pancake, i)
            newChild = AstarNode(flip, i)
            newChild.parent = current
            newChild.getG(i//2)
            if flip == '1w2w3w4w':
                solutionNode = newChild
                break
            if flip not in closedset:
                openlist.append(newChild)
            #print('Test')
        closedset.add(current.pancake)
    #print(solutionNode.pancake, solutionNode.g, solution) 
    finalList = []
    while solutionNode.parent is not None:
        finalList.insert(0, solutionNode)
        solutionNode.parent.split = solutionNode.flipLocation
        solutionNode = solutionNode.parent
    finalList.insert(0, solutionNode)
    for i in finalList:
        try:
            print(i.pancake[:i.split] + '|' + i.pancake[i.split:], 'g=' + str(i.g), 'h=' + str(i.h))
        except:
            print(i.pancake, 'g=' + str(i.g), 'h=' + str(i.h))


alg = sys.argv[1][-1]
pancakestr = sys.argv[1][:-2]

if alg == 'f':
    bfs(pancakestr)
elif alg == 'a':
    aStar(pancakestr)