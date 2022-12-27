'''
  - Helmet left (H) and right (h)
  - BAMA top (B) and bottom (b)
  - Elephant top (E) and bottom (e)
  - Alabama top (A) and bottom (a)
'''

# Human-readable models

TILES = [
    'HbAE', 'ebAh', 'BbAh',
    'ahEe', 'bhAe', 'bhAE',
    'aEBH', 'aHEb', 'aBEh'
]

CHECKS = [
    '1',    '1.1+2.3',    '2',    '2.1+3.3',    '3',
    '1.2+4.0',            '2.2+5.0',            '3.2+6.0',
    '4',    '4.1+5.3',    '5',    '5.1+6.3',    '6',
    '4.2+7.0',            '5.2+8.0',            '6.2+9.0',
    '7',    '7.1+8.3',    '8',    '8.1+9.3',    '9'
]

# Build computer-readable models

tiles = []
for t in TILES:
    tiles.append([])
    for c in t:
        tiles[-1].append(c)
# print(tiles)

checks = []
for c in CHECKS:
    if len(c) > 1:
        w = int(c[0])-1
        x = int(c[2])
        y = int(c[4])-1
        z = int(c[6])
        checks.append((w, x, y, z))
# print(checks)

cursor = [
    [0, 0], [1, 0], [2, 0],
    [3, 0], [4, 0], [5, 0],
    [6, 0], [7, 0], [8, 0],
]

total = 0


def grow(cursor):
    global total
    if len(cursor) == 9:
        yield cursor
        total += 1
    for i in range(9):
        if not i in cursor:
            yield from grow(cursor+[i])


def check_board(board):
    global checks
    # print(board)
    for ch in checks:
        # print(ch)
        a = board[ch[0]][0][ch[1]]
        b = board[ch[2]][0][ch[3]]
        if a == b or a.upper() != b.upper():
            return False
        # print('match',a,b)
    return True


def advance(board, i=0):
    if i == 9:
        return True
    board[i][1] += 1
    # print(board[i])
    board[i][0] = [board[i][0][-1]] + board[i][0][:3]
    if board[i][1] < 4:
        return False
    board[i][1] = 0
    return advance(board, i+1)


def logit(msg):
    with open('logs.txt', 'a') as f:
        f.write(msg+'\n')


logit('starting')

solutions = []
#TEST = [0,1,5,7,6,8,2,4,3]
last = [1, 1, 1, 1, 1]
total = 0
# ready = False
for c in grow([]):
    # if not ready:
    #    if c != [1, 5, 7, 6, 8, 0, 4, 2, 3]:
    #        continue
    #    ready = True
    logit(str(c)+' '+str(solutions))
    #c = TEST
    total += 1
    print(c, solutions)
    if str(c[:5]) != str(last[:5]):
        print(c)
        last = list(c)
    board = []
    for i in c:
        board.append([list(tiles[i]), 0])
    while True:
        if check_board(board):
            solutions.append(board)
            print("Found solution:", board)
            logit('Found solution: '+str(board))
        if advance(board, 0):
            break

print('solutions', solutions)
