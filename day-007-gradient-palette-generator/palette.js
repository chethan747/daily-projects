// gradient-palette-generator — pure colour maths, no DOM needed.
// Works in the browser and under node for testing.

'use strict';

function clamp(n, lo, hi) {
  return Math.min(hi, Math.max(lo, n));
}

function normalizeHex(hex) {
  let h = String(hex).trim().replace(/^#/, '');
  if (/^[0-9a-fA-F]{3}$/.test(h)) {
    h = h.split('').map(c => c + c).join('');
  }
  if (!/^[0-9a-fA-F]{6}$/.test(h)) {
    throw new Error('not a valid hex colour: ' + hex);
  }
  return '#' + h.toLowerCase();
}

function hexToHsl(hex) {
  hex = normalizeHex(hex);
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  let h = 0, s = 0;
  const l = (max + min) / 2;
  const d = max - min;
  if (d !== 0) {
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      default: h = (r - g) / d + 4;
    }
    h *= 60;
  }
  return { h: h % 360, s: s * 100, l: l * 100 };
}

function hslToHex(h, s, l) {
  h = ((h % 360) + 360) % 360;
  s = clamp(s, 0, 100) / 100;
  l = clamp(l, 0, 100) / 100;
  const k = n => (n + h / 30) % 12;
  const a = s * Math.min(l, 1 - l);
  const f = n => l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
  const to = x => Math.round(x * 255).toString(16).padStart(2, '0');
  return '#' + to(f(0)) + to(f(8)) + to(f(4));
}

function shiftHue(hex, deg) {
  const { h, s, l } = hexToHsl(hex);
  return hslToHex(h + deg, s, l);
}

// Build a palette from a base colour:
//   - 5 tints (lighter) and 5 shades (darker)
//   - complementary pair, 2 analogous, 2 triadic accents
function generatePalette(base) {
  const { h, s, l } = hexToHsl(normalizeHex(base));
  const tints = [];
  for (let i = 1; i <= 5; i++) {
    tints.push(hslToHex(h, s, l + (i * (92 - l)) / 6));
  }
  const shades = [];
  for (let i = 1; i <= 5; i++) {
    shades.push(hslToHex(h, s, l - (i * (l - 8)) / 6));
  }
  return {
    base: normalizeHex(base),
    tints,
    shades,
    complementary: shiftHue(base, 180),
    analogous: [shiftHue(base, -30), shiftHue(base, 30)],
    triadic: [shiftHue(base, 120), shiftHue(base, 240)],
  };
}

function toCssGradient(hexes) {
  return 'linear-gradient(135deg, ' + hexes.join(', ') + ')';
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { normalizeHex, hexToHsl, hslToHex, shiftHue, generatePalette, toCssGradient };
}
