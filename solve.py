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

# Computer-readable models

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

def get_permutations(size, cursor=None):
    if cursor is None:
        cursor = []    
    if len(cursor) == size:
        yield cursor
    for i in range(size):
        if not i in cursor:
            yield from get_permutations(size=size, cursor=cursor+[i])

def check_board(board):    
    for ch in checks:        
        a = board[ch[0]][0][ch[1]]
        b = board[ch[2]][0][ch[3]]
        if a == b or a.upper() != b.upper():
            # Stop checking with the first failure
            return False        
    # All checks pass ... this board is a win
    return True

def next_rotation(board, i=0):
    if i == 9:
        return True
    board[i][1] += 1
    # print(board[i])
    board[i][0] = [board[i][0][-1]] + board[i][0][:3]
    if board[i][1] < 4:
        return False
    board[i][1] = 0
    return next_rotation(board, i+1)

def logit(msg):
    with open('logs.txt', 'a') as f:
        f.write(msg+'\n')


logit('starting')

solutions = []
SKIP_TO = [7, 5, 2, 8, 6, 1, 4, 3, 0]
total = 0
ready = False
for c in get_permutations(9):
    # In case we are restarting from a given point
    if SKIP_TO and not ready:
       if c != SKIP_TO:
           continue
       ready = True

    print(c, solutions) 
    logit(str(c)+' '+str(solutions))
       
    board = []
    for i in c:
        board.append([list(tiles[i]), 0])
    while True:
        if check_board(board):
            solutions.append(board)
            print("Found solution:", c, board)
            logit('Found solution: '+str(c)+' '+str(board))
        if next_rotation(board, 0):
            break

print('solutions', solutions)
