#!/usr/bin/env node
/**
 * morse-code-cli — a tiny Morse code encoder/decoder for the terminal.
 * Small demo/exercise project, not a production system.
 *
 * Usage:
 *   node index.js encode "SOS"        -> ... --- ...
 *   node index.js decode "... --- ..." -> SOS
 *   node index.js help
 */

const MORSE = {
  A: ".-",   B: "-...", C: "-.-.", D: "-..",  E: ".",
  F: "..-.", G: "--.",  H: "....", I: "..",   J: ".---",
  K: "-.-",  L: ".-..", M: "--",   N: "-.",   O: "---",
  P: ".--.", Q: "--.-", R: ".-.",  S: "...",  T: "-",
  U: "..-",  V: "...-", W: ".--",  X: "-..-", Y: "-.--",
  Z: "--..",
  0: "-----", 1: ".----", 2: "..---", 3: "...--", 4: "....-",
  5: ".....", 6: "-....", 7: "--...", 8: "---..", 9: "----.",
  ".": ".-.-.-", ",": "--..--", "?": "..--..", "!": "-.-.--",
  "'": ".----.", "/": "-..-.", ":": "---...", "=": "-...-",
  "+": ".-.-.", "-": "-....-", "(": "-.--.", ")": "-.--.-"
};

const REVERSE = Object.fromEntries(
  Object.entries(MORSE).map(([ch, code]) => [code, ch])
);

/** Encode plain text into Morse. Letters separated by spaces, words by " / ". */
function encode(text) {
  return text
    .toUpperCase()
    .split("")
    .map((ch) => {
      if (ch === " ") return "/";
      if (!(ch in MORSE)) throw new Error(`Cannot encode character: "${ch}"`);
      return MORSE[ch];
    })
    .join(" ");
}

/** Decode Morse back into text. Words are separated by " / ". */
function decode(code) {
  return code
    .trim()
    .split(/\s+/)
    .map((token) => {
      if (token === "/") return " ";
      if (!(token in REVERSE)) throw new Error(`Unknown Morse token: "${token}"`);
      return REVERSE[token];
    })
    .join("")
    .replace(/\s+/g, " ");
}

function help() {
  console.log(`morse-code-cli — tiny Morse code encoder/decoder

Usage:
  node index.js encode "HELLO WORLD"
  node index.js decode ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
  node index.js help

Supported: A–Z, 0–9 and common punctuation (. , ? ! ' / : = + - ( ))`);
}

function main(argv) {
  const [command, ...rest] = argv.slice(2);
  const input = rest.join(" ");

  try {
    if (command === "encode") {
      if (!input) throw new Error("Nothing to encode. Pass text after 'encode'.");
      console.log(encode(input));
    } else if (command === "decode") {
      if (!input) throw new Error("Nothing to decode. Pass Morse after 'decode'.");
      console.log(decode(input));
    } else {
      help();
    }
  } catch (err) {
    console.error("Error:", err.message);
    process.exit(1);
  }
}

module.exports = { encode, decode };

if (require.main === module) main(process.argv);
