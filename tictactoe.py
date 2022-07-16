from copy import deepcopy

X= "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    
    empty_cells: int = sum([row.count(EMPTY) for row in board])
    
    #X plays if there are odd Empty cells
    return X if empty_cells % 2 == 1 else O

def getLastMove(board):
    if player(board) == X:
        return O
    else:
        return X

def actions(board):
    possibleActions = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is EMPTY:
                possibleActions.add((i,j))
    return possibleActions

def result(board, action):
    boardCopy = deepcopy(board)

    if boardCopy[action[0]][action[1]] is not EMPTY:
        raise Exception("Action is not valid for the board.")

    boardCopy[action[0]][action[1]] = player(board)
    return boardCopy


def winner(board):
    lastMoveMade = getLastMove(board)
    #Checks rows
    for row in board:
        if all([cell == lastMoveMade for cell in row]):
            return lastMoveMade

    #Checks columns   
    for i in range(len(board)):
        column = [row[i] for row in board]  
        if all([cell == lastMoveMade for cell in column]):
            return lastMoveMade
    
    #Checks diagonally
    diag1 = (board[0][0],board[1][1],board[2][2])
    diag2 = (board[2][0],board[1][1],board[0][2])
    if all([cell == lastMoveMade for cell in diag1]) or all([cell == lastMoveMade for cell in diag2]):
        return lastMoveMade
    
    #If there is no winner
    return None


def terminal(board):
    #If board has been filled or someone has won
    if all([EMPTY not in row for row in board]) or winner(board) is not None:
        return True
    else:
        return False


def utility(board):
    winnerPlayer = winner(board)
    if winnerPlayer == X:
        return 1
    elif winnerPlayer == O:
        return -1
    else:
        return 0

def minimax(board):
    current_player = player(board)
    
    if terminal(board):
        return None
    
    elif current_player == X:  
        value_action_x = dict()    # A dictionary to store {action:value}
        for action in actions(board):
            result_of_action = result(board,action)
            if winner(result_of_action) == current_player: #If the move can result in a win, return it
                return action
            value_action_x.update({action : returnBest(result_of_action)})   
        return max(value_action_x,key=value_action_x.get)
    

    elif current_player == O:
        value_action_o = dict() # A dictionary to store {action:value}
        for action in actions(board):
            result_of_action = result(board,action)
            if winner(result_of_action) == current_player:  #If the move can result in a win, return it
                return action
            value_action_o.update({action : returnBest(result_of_action)}) 
        return min(value_action_o,key=value_action_o.get)


def returnBest(board):
    current_player = player(board)
    
    if terminal(board):
        return utility(board)
    
    elif current_player == X:
        value = float('-inf')
        for action in actions(board):
            value = max(value,returnBest(result(board,action)))
            if value == 1: #Pruning, if value is 1, no need to continue branching
                return value
        return value
    
    elif current_player == O:
        value = float('inf')
        for action in actions(board):
            value = min(value,returnBest(result(board,action)))
            if value == -1: #Pruning, if value is -1, no need to continue branching
                return value
        return value