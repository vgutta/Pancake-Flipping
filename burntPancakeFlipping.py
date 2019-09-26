import copy

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
    print('Starting: ', fringe[0].pancake + '|')
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
            newChild.flipcost = i
            cost += i//2
            #print(flip[:i] + '|' + flip[i:] + ',', 'Flip Cost: ' + str(i//2) + ',', 'Total Cost: ' + str(cost))
            fringe.append(newChild)
        visited.append(fringe[0].pancake)
        fringe.pop(0)
    goalNode = fringe[0]
    #print(goalNode)
    #print(goalNode.parent)
    finalList = []
    while goalNode.parent is not None:
        finalList.insert(0, goalNode)
        goalNode = goalNode.parent
    for node in finalList:
        print(node.pancake[:node.flipcost] + '|' + node.pancake[node.flipcost:])

    print('Total Flips:', cost)
    print('Visited:', len(visited))

class ListNode:
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


    def __init__(self, pancake):
        self.pancake = pancake
        self.parent = None
        self.g = 0
        self.h = self.heuristic()
        self.f = self.g + self.h



def aStar(pancake):
    init_node = ListNode(pancake)
    openlist = [init_node]
    closedlist = []
    print(openlist[0].h)
    #while len(openlist) > 0:

        #for i in range(2,9,2):
        #    flip = flip_pancake(pancake)

bfs('1b2b3b4b')