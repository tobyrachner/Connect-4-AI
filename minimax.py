import numpy, copy

def getEmptyCols(board):
    return [i for i in range(7) if board[i][-1] == 0]

def playMark(board, col, mark):
    lowest = board[col].index(0)
    board[col][lowest] = mark
    return board

def changePlayer(currPlayer):
    if currPlayer == 'X':
        return 'O'
    if currPlayer == 'O':
        return 'X'
    
def getAllLines(board):
    lines = board.copy()

    for i in range(6):
        lines.append([col[i] for col in board])

    a = numpy.array(board)
    diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
    diags = [diag.tolist() for diag in diags if len(diag) > 3]
    for diag in diags:
        lines.append([x for x in diag])
    return lines

def determineWinner(board):
    lines = getAllLines(board)

    for line in lines:
        count = 0
        previous = 0
        for obj in line:
            if obj == previous: count += 1
            else:
                count = 0
                previous = obj

            if count >= 3 and obj != 0:
                return obj
           
    return False

def scorePosition(board, aiMark, humanMark):
    lines = getAllLines(board)
    windows = []
    for line in lines:
        for i in range(len(line) - 3):
            windows.append(line[i:i+4])

    score = 0

    for window in windows:
        if window.count(aiMark) == 3 and window.count(humanMark) == 0:
            score += 5

        if window.count(aiMark) == 2 and window.count(humanMark) == 0:
            score += 2

        if window.count(humanMark) == 3 and window.count(aiMark) == 0:
            score -= 4

    return score

   
def minimax(currBoard, currPlayer, alpha, beta, depth, node = 0, aiMark = '', humanMark = ''):
    startingNode = node
    if node == 0:
        aiMark = currPlayer
        humanMark = changePlayer(aiMark)
    node += 1

    emptyCols = getEmptyCols(currBoard)

    winner = determineWinner(currBoard)
    if winner == aiMark:
        return 100, node
    elif winner == humanMark:
        return -100, node
    if len(emptyCols) == 0:
        return 0, node
    
    if depth == 0:
        return scorePosition(currBoard, aiMark, humanMark), node

   
    testRecords = []
    lowestScore = 1000
    highestScore = -1000
   
    for col in emptyCols:
        testBoard = playMark(copy.deepcopy(currBoard), col, currPlayer)
        result, node = minimax(testBoard, changePlayer(currPlayer), alpha, beta, depth - 1, node=node, aiMark=aiMark, humanMark=humanMark)
        testRecords.append((col, result))

        if currPlayer == aiMark:
            highestScore = max(highestScore, result)
            alpha = max(highestScore, alpha)
            if beta <= alpha:
                break
        if currPlayer == humanMark:
            lowestScore = min(lowestScore, result)
            beta = min(lowestScore, beta)
            if beta <= alpha:
                break

    if startingNode == 0:
        print(testRecords)
        bestMove = (0, -300)
        for move in testRecords:
            if move[1] > bestMove[1]:
                bestMove = move
        return bestMove[0], node
   
    if currPlayer == aiMark:
        return highestScore, node
   
    if currPlayer == humanMark:
        return lowestScore, node
