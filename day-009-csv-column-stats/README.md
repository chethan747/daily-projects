# Day 009 — csv-column-stats

A small demo CLI that reads a CSV file and prints a quick summary of every
column: detected type, basic stats, and tiny ASCII bar charts right in the
terminal.

## Run it

```sh
python3 stats.py sample.csv
python3 stats.py sample.csv --top 8   # show more top values for text columns
```

Standard library only — no installs needed.

## What it does

- Detects whether each column is **numeric** or **text** (empty cells are skipped).
- Numeric columns: count, min, max, mean, standard deviation, plus an 8-bucket ASCII histogram.
- Text columns: count, number of distinct values, and the most common values rendered as ASCII bars.

## The idea

Opening a spreadsheet just to answer "what's in this column?" is slow. One
glance at `stats.py` output tells you the shape of your data — the value range,
the skew, the dominant categories. A good habit before writing any analysis
code: summarise first, assume nothing.
