"""
Core Tic-Tac-Toe game logic.

The board is a list of 9 characters, indexed 0-8 like this:

     0 | 1 | 2
     3 | 4 | 5
     6 | 7 | 8

Each cell holds 'X', 'O', or ' ' (empty).
"""

EMPTY = ' '
PLAYER = 'X'
AI = 'O'

# Every possible way to win: 3 rows, 3 columns, 2 diagonals.
WIN_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


def available_moves(board):
    """Return a list of empty cell indexes."""
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def is_full(board):
    """True if there are no empty cells left."""
    return EMPTY not in board


def check_winner(board, player):
    """True if `player` ('X' or 'O') has three in a row."""
    for a, b, c in WIN_COMBINATIONS:
        if board[a] == board[b] == board[c] == player:
            return True
    return False


class TicTacToe:
    """Holds the state of a single game and the rules for playing it."""

    def __init__(self):
        self.board = [EMPTY] * 9

    def reset(self):
        self.board = [EMPTY] * 9

    def make_move(self, index, player):
        """Place `player` at `index` if that cell is empty. Returns success."""
        if self.board[index] != EMPTY:
            return False
        self.board[index] = player
        return True

    def available_moves(self):
        return available_moves(self.board)

    def check_winner(self, player):
        return check_winner(self.board, player)

    def is_full(self):
        return is_full(self.board)

    def is_draw(self):
        return self.is_full() and not self.check_winner(PLAYER) and not self.check_winner(AI)

    def is_game_over(self):
        return self.check_winner(PLAYER) or self.check_winner(AI) or self.is_full()
