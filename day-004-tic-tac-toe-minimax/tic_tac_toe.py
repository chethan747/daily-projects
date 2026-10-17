"""Tic-Tac-Toe with a minimax AI.

Small demo/exercise project: a complete, playable game where the computer
picks its move with the classic minimax algorithm. With optimal play from
both sides the game always ends in a draw — you can watch that happen with
the self-play mode.
"""

import argparse
import sys

EMPTY = " "

# Prefer centre, then corners, then edges when scores are equal.
MOVE_ORDER = [4, 0, 2, 6, 8, 1, 3, 5, 7]
LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),            # diagonals
)


def winner(board):
    """Return 'X', 'O', 'draw', or None if the game is still going."""
    for a, b, c in LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    if EMPTY not in board:
        return "draw"
    return None


def minimax(board, ai, current, depth=0):
    """Return (score, best_move) for the side to move.

    Score is from the AI's perspective: +10 for an AI win, -10 for a loss,
    0 for a draw, adjusted by depth so faster wins beat slower ones.
    """
    result = winner(board)
    if result == ai:
        return 10 - depth, None
    if result == "draw":
        return 0, None
    if result is not None:  # opponent won
        return depth - 10, None

    other = "O" if current == "X" else "X"
    best_score = -float("inf") if current == ai else float("inf")
    best_move = None
    for move in MOVE_ORDER:
        if board[move] != EMPTY:
            continue
        board[move] = current
        score, _ = minimax(board, ai, other, depth + 1)
        board[move] = EMPTY
        if current == ai:
            if score > best_score:
                best_score, best_move = score, move
        else:
            if score < best_score:
                best_score, best_move = score, move
    return best_score, best_move


def best_move(board, ai):
    """Pick the AI's move (never loses when it starts)."""
    _, move = minimax(board, ai, ai)
    return move


def render(board):
    cells = [c if c != EMPTY else str(i + 1) for i, c in enumerate(board)]
    row = "{} | {} | {}".format
    sep = "\n----------\n"
    rows = [row(*cells[0:3]), row(*cells[3:6]), row(*cells[6:9])]
    return sep.join(rows)


def self_play():
    """AI vs AI — always a draw; also serves as the smoke test."""
    board = [EMPTY] * 9
    turn = "X"
    while winner(board) is None:
        board[best_move(board, turn)] = turn
        turn = "O" if turn == "X" else "X"
    print(render(board))
    print("Result:", winner(board))


def play_human():
    board = [EMPTY] * 9
    human, ai = "X", "O"
    print("You are X. Type 1-9 to place your mark.\n")
    print(render(board), "\n")
    while True:
        result = winner(board)
        if result:
            print("Draw!" if result == "draw" else f"{result} wins!")
            return
        if human_move := input("Your move (1-9): ").strip():
            try:
                pos = int(human_move) - 1
            except ValueError:
                pos = -1
            if not (0 <= pos <= 8) or board[pos] != EMPTY:
                print("Not a legal move — try again.")
                continue
            board[pos] = human
        result = winner(board)
        if result:
            print(render(board))
            print("Draw!" if result == "draw" else f"{result} wins!")
            return
        board[best_move(board, ai)] = ai
        print("\n" + render(board) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--self-play", action="store_true",
        help="run AI vs AI once and print the result",
    )
    args = parser.parse_args(argv)
    if args.self_play:
        self_play()
    else:
        play_human()


if __name__ == "__main__":
    main()
