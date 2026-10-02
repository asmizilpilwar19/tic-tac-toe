# AI Tic-Tac-Toe (Minimax)

A beginner-friendly Tic-Tac-Toe game where you play against an AI that
never makes a random move. The AI's decisions come entirely from a
**Minimax algorithm implemented from scratch** — no AI/ML libraries involved.

## Project description

You (X) play against the computer (O) on a classic 3×3 board. Every move
the AI makes is the result of it mentally playing out *all* possible
futures from the current position and picking the one that guarantees
the best outcome for itself, assuming you also play your best. That
means the AI:

- Never loses a winnable-for-it or neutral position.
- Always blocks your immediate winning move.
- Always takes an immediate winning move of its own.
- At worst, forces a draw.

## Technologies used

- **Python 3** — language
- **Tkinter** (standard library) — GUI
- **Minimax algorithm** — hand-written recursive decision-making, no external AI/ML libraries

## Project structure

```
tic-tac-toe/
├── main.py     # Entry point: builds and runs the Tkinter GUI
├── game.py     # Board state, move validation, win/draw detection
├── ai.py       # The Minimax algorithm and AI move selection
└── README.md
```

Each file has one job:
- `game.py` knows the *rules* (what counts as a win, what counts as a valid move).
- `ai.py` knows how to *choose a move* using those rules.
- `main.py` knows how to *draw a window* and wire button clicks to the game.

## How to run

Requires Python 3 (Tkinter ships with the standard Windows/macOS installers;
on Linux you may need `sudo apt install python3-tk`).

```bash
cd tic-tac-toe
python main.py
```

Click any empty cell to place your **X**. The AI immediately replies
with an **O**. Use **Restart / New Game** at any time to clear the board
without closing the window — your running score stays on screen.

## Game rules

- Standard Tic-Tac-Toe: 3×3 grid, 9 cells.
- You are **X** and always move first.
- The AI is **O**.
- Three of your/the AI's marks in a row, column, or diagonal wins.
- If all 9 cells fill with no winner, it's a draw.
- The scoreboard (`Player / AI / Draws`) persists across restarts until
  you close the app.

## How Minimax works

Minimax is a decision rule for two-player, zero-sum games (what's good
for one player is exactly as bad for the other). It explores the game's
*entire* remaining tree of possible moves and assumes **both players
always play optimally**.

### Why recursion?

A game tree is naturally recursive: "the best move from this board" depends
on "the best move from each board that could result from it," which depends
on the boards after *that*, and so on until the board is full or someone
has won. Recursion lets `ai.py` express that exact idea — try a move,
recursively ask "how good is the position I just created?", then undo
the move and try the next one.

### How the AI evaluates a position (`minimax` in `ai.py`)

```python
def minimax(board, depth, is_maximizing):
    if check_winner(board, AI):      return 10 - depth
    if check_winner(board, PLAYER):  return depth - 10
    if is_full(board):                return 0
    ...
```

- A board where the **AI has already won** scores `+10 - depth`: a win
  found quickly (shallow depth) scores higher than a win found after many
  more moves, so the AI prefers to win sooner rather than later.
- A board where **you've already won** scores `depth - 10`: a loss that's
  far off (deep in the tree) is "less bad" than one that happens soon, so
  if the AI is doomed, it at least delays the loss / maximizes your chance
  to slip up.
- A **full board with no winner** scores `0` (a neutral draw).

For any other (non-terminal) board, the function imagines every legal
move, plays it on the board, recursively scores the result one move
deeper, and then **undoes the move** (sets the cell back to empty) before
trying the next one. This undo step — called *backtracking* — is what
lets a single `board` list be reused to explore every branch instead of
copying the board at every step.

- When it's the **AI's simulated turn** (`is_maximizing=True`), it keeps
  the **highest** score found — the AI wants to win.
- When it's **your simulated turn** (`is_maximizing=False`), it keeps the
  **lowest** score found — the algorithm assumes you'll always pick the
  move that's worst for the AI (i.e., you play your best too).

### How the AI chooses its actual move (`get_best_move` in `ai.py`)

`get_best_move` is the outer loop: it tries each empty cell as the AI's
move, asks `minimax` how good the resulting position is for the AI, and
returns whichever cell produced the highest score. That cell is the move
actually played on the real board.

### How win/loss/draw detection works (`game.py`)

`WIN_COMBINATIONS` lists the 8 index triples that make a line (3 rows, 3
columns, 2 diagonals). `check_winner(board, player)` just checks whether
all three cells of any one triple belong to `player`. `is_full(board)`
checks whether any `' '` (empty) cells remain. The `TicTacToe` class in
`game.py` combines these into `is_draw()` (full board, nobody won) and
`is_game_over()` (someone won, or it's a draw).

## Example gameplay

```
Your turn (X) — you click the center cell:

  .  |  .  |  .
 ----+----+----
  .  |  X  |  .
 ----+----+----
  .  |  .  |  .

AI is thinking... (Minimax picks a corner, since taking a corner
against a center-opening X is the AI's strongest reply)

  O  |  .  |  .
 ----+----+----
  .  |  X  |  .
 ----+----+----
  .  |  .  |  .

Play continues until someone gets three in a row, or the board fills up.
Against a perfect-playing AI like this one, the best a human can achieve
is a draw.
```

## Important functions reference

| Function | File | Purpose |
|---|---|---|
| `available_moves(board)` | `game.py` | List of empty cell indexes |
| `check_winner(board, player)` | `game.py` | Has `player` got three in a row? |
| `is_full(board)` | `game.py` | Are all 9 cells filled? |
| `TicTacToe.make_move(index, player)` | `game.py` | Place a mark if the cell is empty |
| `minimax(board, depth, is_maximizing)` | `ai.py` | Recursively score a board position |
| `get_best_move(board)` | `ai.py` | Pick the AI's best move using `minimax` |
| `TicTacToeApp.on_cell_click(index)` | `main.py` | Handle a human click, then trigger the AI's reply |
| `TicTacToeApp.ai_move()` | `main.py` | Ask `ai.py` for a move and play it on the board |
