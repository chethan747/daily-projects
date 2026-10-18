# Day 005 — Password Strength Meter

A one-function password strength scorer in plain JavaScript. Small demo/exercise project — educational, not a security product.

## What it is

`strength.js` exports `scorePassword(pw)` → `{ score, label, entropy, feedback }`:

- **Score (0–100):** combines length (up to 40 pts), character variety (up to 24 pts for the four classes: lower, upper, digit, symbol), and an entropy estimate (up to 16 pts).
- **Penalties:** known-common passwords are capped at 15, repeated characters (`aaa`) and obvious sequences (`1234`, `abcd`) cost 10 pts each.
- **Feedback:** plain-language tips on what's weak and how to improve it.
- **Entropy:** `length × log2(charset size)` as a rough bit estimate.

`demo.js` is a tiny CLI: run it bare to score built-in examples, or pass your own password as an argument (it's never stored or sent anywhere).

## How to run

```bash
node --check strength.js      # syntax check
node demo.js                  # score the built-in examples
node demo.js "MyP@ssw0rd!"    # score your own
```

Requires Node.js 12 or newer; no dependencies to install.

## The idea

Real password checkers like zxcvbn are big; this is the same intuition shrunk into ~100 lines: reward length and variety, punish patterns humans actually use. The key design lesson is that *length beats cleverness* — a long passphrase like "correct-horse-battery-staple" scores well even though it's only lowercase, because each extra character multiplies the guessing space. It's a good reminder that memorable can also mean strong, as long as it's long.
