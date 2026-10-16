'use strict';

// Tiny dependency-free ASCII progress bar for terminal scripts.
// Small demo/exercise project — not a production library.

class ProgressBar {
  /**
   * @param {number} total - total units of work
   * @param {object} [options]
   * @param {number} [options.width=30] - bar width in characters
   * @param {string} [options.label='Progress'] - label shown before the bar
   * @param {string} [options.stream] - output stream (defaults to process.stdout)
   */
  constructor(total, options = {}) {
    if (!Number.isFinite(total) || total <= 0) {
      throw new Error('total must be a positive number');
    }
    this.total = total;
    this.width = options.width ?? 30;
    this.label = options.label ?? 'Progress';
    this.stream = options.stream ?? process.stdout;
    this.current = 0;
    this.startedAt = Date.now();
    this._finished = false;
  }

  tick(n = 1) {
    if (this._finished) return;
    this.current = Math.min(this.total, this.current + n);
    this._render();
    if (this.current >= this.total) this.done();
  }

  _render() {
    const ratio = this.current / this.total;
    const filled = Math.round(ratio * this.width);
    const empty = this.width - filled;
    const bar = '█'.repeat(filled) + '░'.repeat(empty);
    const pct = (ratio * 100).toFixed(1).padStart(5, ' ');
    const elapsed = ((Date.now() - this.startedAt) / 1000).toFixed(1);
    const line = `\r${this.label} |${bar}| ${pct}% (${this.current}/${this.total}) ${elapsed}s`;
    this.stream.write(line);
    if (this._finished) this.stream.write('\n');
  }

  done() {
    if (this._finished) return;
    this._finished = true;
    this.current = this.total;
    this._render();
  }
}

module.exports = { ProgressBar };
