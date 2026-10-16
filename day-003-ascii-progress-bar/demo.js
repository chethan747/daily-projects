'use strict';

// Demo: fake "processing" work rendered through the ASCII progress bar.
// Run with: node demo.js

const { ProgressBar } = require('./progress-bar');

const TOTAL_FILES = 42;
const bar = new ProgressBar(TOTAL_FILES, { label: 'Importing', width: 30 });

let processed = 0;
const timer = setInterval(() => {
  // Simulate a variable chunk of work finishing each tick.
  const chunk = 1 + Math.floor(Math.random() * 3);
  processed += chunk;
  bar.tick(chunk);
  if (processed >= TOTAL_FILES) {
    clearInterval(timer);
    console.log('Import finished.');
  }
}, 120);
