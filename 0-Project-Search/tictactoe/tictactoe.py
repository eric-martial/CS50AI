"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.

    """
    count = 0
    for _ in board:
        for cell in _:
            count += 1 if cell == X else -1 if cell == O else 0

    return X if count <= 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.

    """
    actions = set()
    for i, _ in enumerate(board):
        for j, w in enumerate(_):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.

    """
    i, j = action
    new_board = deepcopy(board)

    if (
        0 <= i < len(new_board)
        and 0 <= j < len(new_board[0])
        and new_board[i][j] == EMPTY
    ):
        new_board[i][j] = player(new_board)
        return new_board
    else:
        raise ValueError("Invalid action: {}".format(action))


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]

        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.

    """
    gameover = False
    count_empty = 0
    for _ in board:
        for cell in _:
            count_empty += 1 if cell == EMPTY else 0

    if winner(board) != None or count_empty == 0:
        gameover = True

    return gameover


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return 1 if winner(board) == X else -1 if winner(board) == O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    optimal_actions = set()

    if player(board) == X:
        # Prioritize blocking immediate threats
        for action in actions(board):
            new_board = result(board, action)
            if winner(new_board) == O:  # Check if opponent has a winning move
                return action  # Immediately block the threat

        lowest = -math.inf
        for action in actions(board):
            v = maxValue(result(board, action))
            if v > lowest:
                optimal_actions.add(action)
                lowest = v

    if player(board) == O:
        # Prioritize blocking immediate threats
        for action in actions(board):
            new_board = result(board, action)
            if winner(new_board) == O:  # Check if opponent has a winning move
                return action  # Immediately block the threat

        highest = math.inf
        for action in actions(board):
            v = minValue(result(board, action))
            if v < highest:
                optimal_actions.add(action)
                highest = v

    if optimal_actions:
        return optimal_actions.pop()
    else:
        return None


def maxValue(board):
    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        new_board = result(board, action)
        if winner(new_board) == O:  # Check for opponent's winning move
            return -1  # Immediately return its utility
        v = max(v, minValue(result(board, action)))

    return v


def minValue(board):
    if terminal(board):
        return utility(board)

    v = math.inf

    for action in actions(board):
        new_board = result(board, action)
        if winner(new_board) == O:  # Check for opponent's winning move
            return -1  # Immediately return its utility
        v = min(v, maxValue(result(board, action)))

    return v
