# Day 004 — Tic-Tac-Toe with a Minimax AI

A playable tic-tac-toe game where the computer opponent uses the classic minimax algorithm. Small demo/exercise project.

## What it is

`tic_tac_toe.py` implements the full game plus an unbeatable AI in one file:

- `minimax(board, ai, current)` — scores every possible line of play (+10 win, −10 loss, 0 draw, adjusted by depth so faster wins win) and picks the optimal move. Worst case it explores ~550k positions, fast enough to be instant.
- `best_move(board, ai)` — the AI's move; a preferred move order (centre → corners → edges) makes its play look sensible when scores tie.
- `play_human()` — interactive game: you are X, the AI is O, moves via 1–9.
- `self_play()` — AI vs AI; with optimal play from both sides it always draws.

## How to run

```bash
python3 tic_tac_toe.py            # play against the computer (interactive)
python3 tic_tac_toe.py --self-play  # watch AI vs AI, always a draw
```

Requires Python 3.8 or newer; no dependencies to install.

## The idea

Tic-tac-toe is small enough that the whole game tree can be brute-forced, which makes it the perfect playground for minimax — the same algorithm family behind chess and Go engines, stripped down to its essence. The exercise here was keeping the search tiny and readable: one recursive function, depth-weighted scores so the AI prefers quick wins and slow losses, and a sensible tie-break order. The self-play mode doubles as the smoke test: run it and the board always fills to a draw, proving the search actually explored everything.
