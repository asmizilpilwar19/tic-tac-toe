"""
Entry point: launches the Tic-Tac-Toe GUI.

Human plays X, AI plays O. The AI always uses Minimax (ai.py) to pick
its move, so it never plays randomly and never loses a winnable game.
"""

import tkinter as tk
from tkinter import font

from game import TicTacToe, PLAYER, AI
from ai import get_best_move


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Tic-Tac-Toe (Minimax)")
        self.root.resizable(False, False)

        self.game = TicTacToe()
        self.buttons = []
        self.scores = {"player": 0, "ai": 0, "draws": 0}

        self.cell_font = font.Font(family="Helvetica", size=32, weight="bold")
        self.status_font = font.Font(family="Helvetica", size=13, weight="bold")

        self._build_widgets()
        self._update_status("Your turn (X)")

    def _build_widgets(self):
        # Status label at the top.
        self.status_label = tk.Label(self.root, text="", font=self.status_font, pady=10)
        self.status_label.grid(row=0, column=0, columnspan=3)

        # 3x3 grid of buttons.
        board_frame = tk.Frame(self.root)
        board_frame.grid(row=1, column=0, columnspan=3)

        for index in range(9):
            button = tk.Button(
                board_frame,
                text="",
                font=self.cell_font,
                width=4,
                height=2,
                command=lambda i=index: self.on_cell_click(i),
            )
            row, col = divmod(index, 3)
            button.grid(row=row, column=col, padx=2, pady=2)
            self.buttons.append(button)

        # Score tracker.
        self.score_label = tk.Label(self.root, text="", font=("Helvetica", 11), pady=10)
        self.score_label.grid(row=2, column=0, columnspan=3)
        self._update_score_label()

        # Restart button.
        restart_button = tk.Button(self.root, text="Restart / New Game", command=self.restart_game)
        restart_button.grid(row=3, column=0, columnspan=3, pady=(0, 12))

    def on_cell_click(self, index):
        if self.game.is_game_over():
            return
        if not self.game.make_move(index, PLAYER):
            return  # cell already taken

        self._refresh_board()

        if self._handle_game_over():
            return

        self._update_status("AI is thinking...")
        self.root.after(200, self.ai_move)

    def ai_move(self):
        move = get_best_move(self.game.board)
        if move is not None:
            self.game.make_move(move, AI)

        self._refresh_board()

        if self._handle_game_over():
            return

        self._update_status("Your turn (X)")

    def _handle_game_over(self):
        """If the game has ended, update score/status and return True."""
        if self.game.check_winner(PLAYER):
            self.scores["player"] += 1
            self._update_status("You win!")
        elif self.game.check_winner(AI):
            self.scores["ai"] += 1
            self._update_status("AI wins!")
        elif self.game.is_draw():
            self.scores["draws"] += 1
            self._update_status("It's a draw!")
        else:
            return False

        self._update_score_label()
        return True

    def _refresh_board(self):
        for index, cell_value in enumerate(self.game.board):
            self.buttons[index]["text"] = cell_value if cell_value != " " else ""

    def _update_status(self, message):
        self.status_label["text"] = message

    def _update_score_label(self):
        s = self.scores
        self.score_label["text"] = (
            f"Player: {s['player']}    AI: {s['ai']}    Draws: {s['draws']}"
        )

    def restart_game(self):
        self.game.reset()
        self._refresh_board()
        self._update_status("Your turn (X)")


def main():
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
