import copy # used for deep copy
import sys #used for bash args

'''
Given an input string of size 8 and index to flip at
this function returns the flipped order of the pancakes
'''
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

    return ''.join(endlist)

'''
Instances of Nodes in BFS search tree
'''
class BfsNode:
    def __init__(self, pancake):
        self.pancake = pancake # string of pancakes orientation
        self.parent = None # parent node
        self.flipcost = 0 # index of parent where flip took place

'''
Takes the starting pancakes orientation
Creates 4 possible flips for each orientation
Adds starting order to list. Then for each of the four
possible flips for each order. If the new child's pancake orientation
was not visited already it will be added to the fringe
in the order that its expanded.
Stops when goal state 1w2w3w4w is encountered in the fringe.
'''
def bfs(pancake):
    cost = 0
    visited = []
    start = BfsNode(pancake)
    fringe = [start]
    while fringe[0].pancake != '1w2w3w4w':
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
            fringe.append(newChild)
        visited.append(fringe[0].pancake)
        fringe.pop(0)
    
    # following actions are for printing purposes only
    goalNode = fringe[0]
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
    print('Least Flips to find solution:', leastFlips)
    print('Total Flips during search:', cost)
    print('Total new nodes visited during search:', len(visited))

'''
Class to create nodes for A* search algorithm
Again pancake is the string of pancakes orientation

Heuristics function returns max of either largest number out of 
place or number of b's in the string.

Getg sets current g to parent's g + cost from parent to child
It also updates f
'''
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

'''
replaces w with 1 and b with 0 and expands
the node with the max value after this conversion
Helper function when more than one node in fringe
may have the same minimum f value
'''
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
    return openlist.pop(maxkey)

'''
Find the node(s) with minimum f
Uses tiebreak when multiple node have min f
'''
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
        return tiebreak(minList, openlist)
    else:
        return openlist.pop(min)

'''
Open List is the fringe that includes nodes that can be explored
Starts with input string and corresponding node
Node with minimum f is chosen to expand

'''
def aStar(pancake):
    openlist = [AstarNode(pancake)]
    closedset = set()
    solutionNode = None
    while solutionNode is None:
        current = minf(openlist)
        for i in range(2,9,2):
            flip = flip_pancake(current.pancake, i) # flip growing in size from top
            newChild = AstarNode(flip, i) # create new child from resulting flip
            newChild.parent = current # sets current node and child nodes parent
            newChild.getG(i//2) # set child nodes g as parent nodes g plus position of flip
            if flip == '1w2w3w4w':
                solutionNode = newChild # exits while loop
                break
            if flip not in closedset: # if new resulting flip orientation is not seen before
                openlist.append(newChild) # add to fringe
        closedset.add(current.pancake) # current node is added to closed set after expanding children
    
    # following is for printing purposes only
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