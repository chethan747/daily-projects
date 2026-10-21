#!/usr/bin/env python3
"""Contribution heatmap calendar.

A small demo/exercise project: given daily activity counts (date -> count),
render a GitHub-style contribution heatmap -- 52-ish columns of weeks,
7 rows of days -- as a PNG image using only the standard library plus
matplotlib.

Usage:
    python3 heatmap.py                  # renders demo data to heatmap.png
    python3 heatmap.py data.json        # renders your own data
    python3 heatmap.py data.json out.png

data.json format:
    {"2025-01-03": 4, "2025-01-04": 1, ...}
Dates outside a single trailing 53-week window are ignored; missing dates
count as zero.
"""

import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless-safe: no display needed
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# GitHub-ish green scale, light background included for completeness.
COLORS = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
WEEKDAY_LABELS = ["Mon", "", "Wed", "", "Fri", "", ""]


def demo_data(days: int = 371) -> dict:
    """Generate a year of reproducible pseudo-random demo activity."""
    rng = random.Random(42)
    data = {}
    today = date.today()
    for back in range(days):
        day = today - timedelta(days=back)
        # Weekend dips + occasional busy streaks, like real dev life.
        base = 2 if day.weekday() < 5 else 1
        if rng.random() < 0.18:  # busy streak
            count = rng.randint(4, 10)
        elif rng.random() < 0.25:  # quiet day
            count = 0
        else:
            count = rng.randint(0, base + 1)
        data[day.isoformat()] = count
    return data


def load_data(path: str | None) -> dict:
    if path is None:
        return demo_data()
    raw = json.loads(Path(path).read_text())
    data = {}
    for key, value in raw.items():
        try:
            day = date.fromisoformat(str(key))
            data[day.isoformat()] = max(0, int(value))
        except (ValueError, TypeError):
            print(f"warning: skipping invalid entry {key!r}", file=sys.stderr)
    if not data:
        print("warning: no usable data, falling back to demo data", file=sys.stderr)
        return demo_data()
    return data


def build_grid(data: dict) -> tuple:
    """Return (grid, start_monday, month_ticks) for a trailing 53-week window."""
    today = date.today()
    end = today - timedelta(days=(today.weekday() + 1) % 7)  # last Sunday
    start = end - timedelta(weeks=53) + timedelta(days=1)     # Monday, 53 wks back
    weeks = 53
    grid = [[0] * weeks for _ in range(7)]
    cursor = start
    for w in range(weeks):
        for d in range(7):
            grid[d][w] = data.get(cursor.isoformat(), 0)
            cursor += timedelta(days=1)
    month_ticks, month_labels = [], []
    last_month = None
    cursor = start
    for w in range(weeks):
        if cursor.month != last_month:
            month_ticks.append(w + 0.5)
            month_labels.append(cursor.strftime("%b"))
            last_month = cursor.month
        cursor += timedelta(weeks=1)
    return grid, start, month_ticks, month_labels


def levelize(grid: list) -> list:
    """Map counts to intensity levels 0-4 using quartiles of nonzero values."""
    nonzero = sorted(v for row in grid for v in row if v > 0)
    if not nonzero:
        return [[0] * len(grid[0]) for _ in range(7)]
    def quartile(p):
        return nonzero[min(len(nonzero) - 1, int(p * len(nonzero)))]
    q1, q2, q3 = quartile(0.25), quartile(0.5), quartile(0.75)
    levels = []
    for row in grid:
        levels.append([
            0 if v == 0 else 1 if v <= q1 else 2 if v <= q2 else 3 if v <= q3 else 4
            for v in row
        ])
    return levels


def render(data: dict, out_path: str) -> None:
    grid, start, month_ticks, month_labels = build_grid(data)
    levels = levelize(grid)
    total = sum(sum(row) for row in grid)

    fig, ax = plt.subplots(figsize=(12, 2.6))
    cmap = ListedColormap(COLORS)
    ax.pcolormesh(levels, cmap=cmap, edgecolors="#ffffff", linewidths=1.2,
                  vmin=0, vmax=4)
    ax.set_aspect("equal")
    ax.set_xlim(0, len(levels[0]))
    ax.set_ylim(0, 7)
    ax.invert_yaxis()  # row 0 (Monday) on top
    ax.set_xticks(month_ticks)
    ax.set_xticklabels(month_labels, fontsize=8, color="#57606a")
    ax.set_yticks([r + 0.5 for r in range(7)])
    ax.set_yticklabels(WEEKDAY_LABELS, fontsize=8, color="#57606a")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(
        f"Activity heatmap -- {total} contributions in the last 53 weeks "
        f"({start.isoformat()} to {date.today().isoformat()})",
        fontsize=10, color="#24292f", loc="left", pad=12,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main(argv: list) -> int:
    data_path = argv[1] if len(argv) > 1 else None
    out_path = argv[2] if len(argv) > 2 else "heatmap.png"
    data = load_data(data_path)
    render(data, out_path)
    nonzero_days = sum(1 for v in data.values() if v > 0)
    print(f"Wrote {out_path} ({len(data)} days of data, "
          f"{nonzero_days} active days).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
