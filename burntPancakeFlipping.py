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



def bfs(pancake):
    count = 0
    visited = []
    fringe = [pancake]
    print('Starting: ', pancake)
    while fringe[0] != '1w2w3w4w':
        #count += 1
        #if fringe[0] in visited:
        #    break
        #print('Node: ', fringe[0])
        #print('Fringe: ', fringe)
        for i in range(2,9,2):
            flip = flip_pancake(fringe[0], i)
            #print(flip)
            if flip in visited:
                continue
            fringe.append(flip)
        #break
        visited.append(fringe[0])
        fringe.pop(0)
    print('Visited: ', len(visited))
    #print(fringe[0])

bfs('1b2b3b4b')