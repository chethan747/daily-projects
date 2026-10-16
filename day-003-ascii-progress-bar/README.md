# Day 003 — ASCII Progress Bar

A tiny, dependency-free ASCII progress bar for Node.js terminal scripts. Small demo/exercise project.

## What it is

`progress-bar.js` exposes a small `ProgressBar` class:

```js
const { ProgressBar } = require('./progress-bar');
const bar = new ProgressBar(100, { label: 'Uploading', width: 30 });
for (let i = 0; i < 100; i++) {
  doSomeWork();
  bar.tick();
}
bar.done();
```

The bar renders a single in-place terminal line showing the filled/empty bar, percentage, count, and elapsed seconds. `tick(n)` advances by `n` units (defaults to 1) and auto-finishes at the total.

## How to run

```bash
node --check progress-bar.js   # syntax check
node demo.js                   # watch the bar fill over ~5 seconds
```

Requires Node.js 14 or newer; no dependencies to install.

## The idea

CLI scripts usually print a wall of log lines or nothing at all while they work. A one-file progress bar you can drop into any script makes long jobs feel responsive without pulling in a whole library. This exercise was about keeping the surface minimal — constructor, `tick`, `done` — and handling the terminal details (carriage-return rewriting, clamping over-ticks, timing) in a handful of lines.
