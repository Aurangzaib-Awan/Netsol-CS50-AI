"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    sumX=0
    sumO=0
    for rows in board:
        for cell in rows:
            if cell=="X":
                sumX+=1
            if cell=="O":
                sumO+=1
    return "X" if sumX==sumO else "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions=set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                possible_actions.add((i,j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception ("Invalid action")
    new_board=copy.deepcopy(board)
    new_board[action[0]][action[1]]=player(board)
    return new_board
        


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
  # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]

    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not None:
            return board[0][j]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    return None           


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        for cell in row:
            if cell is None:
                return False  # Game still in progress

    return True  # draw


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return 1 if winner(board) == "X" else -1 if winner(board) == "O" else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # for terminal board
    if terminal(board):
        return None 

    current = player(board)

    def max_value(state, alpha, beta):
        if terminal(state):
            return utility(state), None
        v = -math.inf
        best_action = None
        for action in actions(state):
            min_result, _ = min_value(result(state, action), alpha, beta)
            if min_result > v:
                v = min_result
                best_action = action
            alpha = max(alpha, v)
            if beta <= alpha:
                break  #  Prune
        return v, best_action

    def min_value(state, alpha, beta):
        if terminal(state):
            return utility(state), None
        v = math.inf
        best_action = None
        for action in actions(state):
            max_result, _ = max_value(result(state, action), alpha, beta)
            if max_result < v:
                v = max_result
                best_action = action
            beta = min(beta, v)
            if beta <= alpha:
                break  # Prune
        return v, best_action

    if current == "X":
        _, action = max_value(board, -math.inf, math.inf)
    else:
        _, action = min_value(board, -math.inf, math.inf)

    return action


