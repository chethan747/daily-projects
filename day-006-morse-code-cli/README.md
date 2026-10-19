# Day 6 — Morse Code CLI

A tiny command-line Morse code encoder and decoder written in Node.js.
A small demo/exercise project — not a production system.

## The idea

Morse code maps each letter, digit and a handful of punctuation marks to a
pattern of dots and dashes. The interesting bit is that decoding is just a
reverse dictionary lookup, but the *spacing* carries the structure: one space
separates letters, three spaces (or a `/` here) separate words. This little
tool implements both directions — plain text in, Morse out, and back again —
plus clear errors when it meets a character or pattern it doesn't know.

## How to run

Requires Node.js (any recent version).

```bash
# Encode
node index.js encode "SOS"
# ... --- ...

node index.js encode "Hello, World!"
# .... . .-.. .-.. --- --..-- / .-- --- .-. .-.. -.. -.-.--

# Decode (letters separated by spaces, words by /)
node index.js decode "... --- ..."
# SOS

node index.js help
```

## Files

- `index.js` — the whole thing: encode/decode functions and the CLI. The
  functions are also exported, so you can `require('./index.js')` and reuse
  them in your own experiments.

## Supported characters

A–Z, 0–9, and `. , ? ! ' / : = + - ( )`. Anything else raises a friendly
error instead of silently mangling your message.
