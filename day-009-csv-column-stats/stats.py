#!/usr/bin/env python3
"""csv-column-stats: tiny demo CLI that prints per-column stats of a CSV file.

Usage:
    python3 stats.py data.csv
    python3 stats.py data.csv --top 5

For each column it reports the type it detected, and:
  - numeric columns: count, min, max, mean, stdev + an ASCII histogram
  - text columns: count, distinct values + the most common values as ASCII bars

Small learning exercise. Standard library only.
"""

import argparse
import csv
import math
import sys
from collections import Counter


def looks_numeric(values):
    nums = []
    for v in values:
        if v == "" or v is None:
            continue
        try:
            nums.append(float(v))
        except ValueError:
            return None
    return nums


def describe_numeric(nums, width=30):
    n = len(nums)
    if n == 0:
        return ["  (no values)"]
    mean = sum(nums) / n
    var = sum((x - mean) ** 2 for x in nums) / n
    lines = [
        f"  count: {n}   min: {min(nums):g}   max: {max(nums):g}",
        f"  mean:  {mean:.4g}   stdev: {math.sqrt(var):.4g}",
        "  histogram:",
    ]
    lo, hi = min(nums), max(nums)
    span = hi - lo or 1.0
    bins = [0] * 8
    for x in nums:
        idx = min(7, int((x - lo) / span * 8))
        bins[idx] += 1
    peak = max(bins) or 1
    for i, b in enumerate(bins):
        edge_lo = lo + span * i / 8
        edge_hi = lo + span * (i + 1) / 8
        bar = "#" * math.ceil(b / peak * width)
        lines.append(f"    {edge_lo:8.3g}-{edge_hi:8.3g} | {bar} ({b})")
    return lines


def describe_text(values, top=5, width=30):
    nonempty = [v for v in values if v not in ("", None)]
    lines = [f"  count: {len(nonempty)}   distinct: {len(set(nonempty))}"]
    if not nonempty:
        return lines + ["  (no values)"]
    common = Counter(nonempty).most_common(top)
    peak = common[0][1]
    lines.append("  top values:")
    for val, c in common:
        bar = "#" * math.ceil(c / peak * width)
        label = val if len(val) <= 20 else val[:17] + "..."
        lines.append(f"    {label:22} | {bar} ({c})")
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print per-column stats for a CSV file.")
    parser.add_argument("csv_file", help="path to a .csv file (first row = header)")
    parser.add_argument("--top", type=int, default=5, help="top-N values shown for text columns")
    args = parser.parse_args(argv)

    try:
        with open(args.csv_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            columns = [[] for _ in header]
            for row in reader:
                for i, col in enumerate(columns):
                    col.append(row[i] if i < len(row) else "")
    except FileNotFoundError:
        sys.exit(f"error: file not found: {args.csv_file}")
    except StopIteration:
        sys.exit("error: empty file")

    print(f"{len(header)} columns")
    for name, values in zip(header, columns):
        nums = looks_numeric(values)
        kind = "numeric" if nums is not None else "text"
        print(f"\n{name}  [{kind}]")
        if kind == "numeric":
            print("\n".join(describe_numeric(nums)))
        else:
            print("\n".join(describe_text(values, top=args.top)))


if __name__ == "__main__":
    main()
