// Demo for password-strength-meter.
// Usage:
//   node demo.js                      # score the built-in examples
//   node demo.js "your password"      # score your own (history-safe: nothing is stored or sent)
const { scorePassword } = require("./strength");

const examples = [
  "password",
  "12345678",
  "fluffy7",
  "Tr0ub4dor&3",
  "correct-horse-battery-staple",
  "Xk9!qL2#vB7@zW",
];

const inputs = process.argv.length > 2 ? process.argv.slice(2) : examples;

for (const pw of inputs) {
  const { score, label, entropy, feedback } = scorePassword(pw);
  const shown = process.argv.length > 2 ? "(hidden)" : JSON.stringify(pw);
  console.log(`\n${shown}`);
  console.log(`  score:   ${score}/100 — ${label}`);
  console.log(`  entropy: ~${entropy} bits`);
  if (feedback.length) {
    for (const f of feedback) console.log(`  tip:     ${f}`);
  } else {
    console.log("  tip:     nothing to complain about");
  }
}
