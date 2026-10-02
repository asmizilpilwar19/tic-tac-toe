"""
Minimax algorithm for the Tic-Tac-Toe AI.

No external AI/ML library is used. The AI works by brute-force recursion:
it simulates every possible sequence of future moves, scores how each
sequence ends (AI win / human win / draw), and picks the move that leads
to the best guaranteed outcome, assuming the human also plays their best.
"""

from game import check_winner, available_moves, is_full, PLAYER, AI, EMPTY


def minimax(board, depth, is_maximizing):
    """
    Recursively score the current board.

    - is_maximizing=True  -> it's the AI's ('O') turn, AI wants the HIGHEST score.
    - is_maximizing=False -> it's the human's ('X') turn, human wants the LOWEST score.

    Scores:
      AI win    -> +10 minus depth (win sooner = higher score)
      Human win -> depth minus 10 (lose later = less negative = "less bad")
      Draw      -> 0
    """
    if check_winner(board, AI):
        return 10 - depth
    if check_winner(board, PLAYER):
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for move in available_moves(board):
            board[move] = AI
            score = minimax(board, depth + 1, False)
            board[move] = EMPTY  # undo the simulated move
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for move in available_moves(board):
            board[move] = PLAYER
            score = minimax(board, depth + 1, True)
            board[move] = EMPTY  # undo the simulated move
            best_score = min(best_score, score)
        return best_score


def get_best_move(board):
    """
    Try every empty cell, ask minimax how good that move is, and return
    the index of the best one for the AI ('O').
    """
    best_score = float('-inf')
    best_move = None

    for move in available_moves(board):
        board[move] = AI
        score = minimax(board, 0, False)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            best_move = move

    return best_move
