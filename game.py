import numpy as np
from c4Minimax import minimax

DEFAULT_BOARD = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]

def main():
    humanMark, aiMark = getStarter()

    currPlayer = 'X'
    board = DEFAULT_BOARD
    translation = {1: 'X', 2: 'O'}
   
    while True:

        if currPlayer == humanMark:
            PrettyPrint(board)
            print("Your turn")

            col = get_move(board)
        else:
            col = minimax(board, currPlayer, -300, +300, 8)[0]
            print('The AI chose column', col + 1)
        lowest = board[col].index(0)


        board[col][lowest] = currPlayer

        winner = check_win(board, lowest, col)
        if winner:
            PrettyPrint(board)
            print(currPlayer + ' Wins')
            break

        currPlayer = changePlayer(currPlayer)

def getStarter():
    while True:
        index = input('Do you want to go first or second? (1/2): ') 
        if index in ['1', '2']:
            break
        print('Invalid input')
    if index == '1':
        return 'X', 'O'
    else:
        return 'O', 'X'

def PrettyPrint(inputBoard):
    flippedBoard = list(np.transpose(np.flip(inputBoard, axis=1)))
    board = []
    for x in flippedBoard:
        board.append(list(x))
    print_board = board
    translation = {0: ' ', 1: 'X', 2: 'O'}
    for row in board:
        for i in range(len(row)):
            if row[i] == 0 or row[i] == '0':
                board[board.index(row)][i] = ' '
        

    rows = len(board)
    cols = len(board)
    print("+---+---+---+---+---+---+---+")
    for r in range(rows):
        print("|", print_board[r][0], "|", print_board[r][1], "|", print_board[r][2], "|", print_board[r][3], "|", print_board[r][4], "|", print_board[r][5], "|", print_board[r][6], "|")
        print("+---+---+---+---+---+---+---+")

def changePlayer(currPlayer):
    if currPlayer == 'X':
        return 'O'
    if currPlayer == 'O':
        return 'X'

def get_move(board):
    while True:
        valid_inputs  = [0, 1, 2, 3, 4, 5, 6]
        col = input('Enter column: ')
        if not col.isnumeric():
            continue
        col = int(col) - 1
        if not col in valid_inputs:
            print('Invalid column')
            continue
        if board[col][-1] != 0:
            print('column full')
            continue
        return col
   
def check_win(board, row, col):
    check_col = board[col]
    check_row = [x[row] for x in board]

    a = np.array(board)
    diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
    diags = [diag for diag in diags if len(diag) >= 3]

    for l in [check_row, check_col] + diags:
        count = 0
        previous = 0
        for obj in l:
            if obj == previous: count += 1
            else:
                count = 0
                previous = obj

            if count >= 3 and obj != 0 and obj != '0':
                return obj
           
    return False

if __name__ == '__main__':
    main()
