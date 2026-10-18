// password-strength-meter — score a password's strength in one function.
// No dependencies. Works in Node.js and the browser.
// Small demo/exercise project, not a security product.

const COMMON = [
  "password", "123456", "123456789", "qwerty", "abc123", "password1",
  "12345678", "111111", "123123", "admin", "welcome", "letmein",
  "monkey", "dragon", "football", "iloveyou", "master", "sunshine",
  "princess", "qwertyuiop", "passw0rd", "12345", "654321", "1qaz2wsx",
];

function isCommonPassword(pw) {
  const lower = pw.toLowerCase();
  return COMMON.some((c) => lower === c || (lower.includes(c) && c.length >= 6 && lower.length <= c.length + 2));
}

function hasRepeats(pw) {
  // three or more of the same character in a row, e.g. "aaa"
  return /(.)\1\1/.test(pw);
}

function hasSequence(pw) {
  // obvious ascending/descending runs like "1234", "abcd", "4321"
  const lower = pw.toLowerCase();
  const runs = ["0123456789", "abcdefghijklmnopqrstuvwxyz"];
  for (const run of runs) {
    for (let i = 0; i + 3 < run.length; i++) {
      const fwd = run.slice(i, i + 4);
      const rev = [...fwd].reverse().join("");
      if (lower.includes(fwd) || lower.includes(rev)) return true;
    }
  }
  return false;
}

/**
 * Score a password from 0 (hopeless) to 100 (excellent).
 * Returns { score, label, entropy, feedback }.
 */
function scorePassword(pw) {
  pw = String(pw);
  const feedback = [];

  // --- character set size for an entropy estimate
  let charset = 0;
  const hasLower = /[a-z]/.test(pw);
  const hasUpper = /[A-Z]/.test(pw);
  const hasDigit = /\d/.test(pw);
  const hasSymbol = /[^a-zA-Z0-9]/.test(pw);
  if (hasLower) charset += 26;
  if (hasUpper) charset += 26;
  if (hasDigit) charset += 10;
  if (hasSymbol) charset += 32;
  const entropy = charset > 0 ? Math.round(pw.length * Math.log2(charset)) : 0;

  let score = 0;

  // length: up to 40 points
  score += Math.min(40, pw.length * 3);

  // variety: up to 24 points, 6 per character class
  let classes = 0;
  if (hasLower) classes++;
  if (hasUpper) classes++;
  if (hasDigit) classes++;
  if (hasSymbol) classes++;
  score += classes * 6;

  // entropy bonus: up to 16 points (80 bits ≈ strong)
  score += Math.min(16, Math.round((entropy / 80) * 16));

  // --- penalties
  if (isCommonPassword(pw)) {
    score = Math.min(score, 15);
    feedback.push("This is (or looks like) a very common password.");
  }
  if (hasRepeats(pw)) {
    score -= 10;
    feedback.push("Avoid repeated characters like 'aaa'.");
  }
  if (hasSequence(pw)) {
    score -= 10;
    feedback.push("Avoid obvious sequences like '1234' or 'abcd'.");
  }
  if (pw.length < 8) {
    feedback.push("Use at least 8 characters; 12+ is much better.");
  } else if (pw.length < 12) {
    feedback.push("Longer is stronger — aim for 12+ characters.");
  }
  if (classes < 3) {
    feedback.push("Mix character types: letters, numbers and symbols.");
  }

  score = Math.max(0, Math.min(100, Math.round(score)));
  const label =
    score >= 80 ? "Excellent" :
    score >= 60 ? "Good" :
    score >= 40 ? "Fair" :
    score >= 20 ? "Weak" : "Very weak";

  return { score, label, entropy, feedback: [...new Set(feedback)] };
}

module.exports = { scorePassword };
