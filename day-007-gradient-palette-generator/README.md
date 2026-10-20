# Gradient Palette Generator (Day 007)

A tiny single-page app that turns any base colour into a ready-to-use design palette:
tints, shades, complementary, analogous and triadic swatches — plus a hero gradient
built from all of them. Click any swatch to copy its hex code.

**The idea:** colour theory in about 60 lines of pure maths. Hex ↔ HSL conversion
lets the generator rotate hues and scale lightness with predictable results, so
every palette stays harmonious with the colour you pick.

## How to run

No build step, no dependencies. Either:

- Open `index.html` in any modern browser, or
- Serve the folder and visit it:

```sh
cd day-007-gradient-palette-generator
python3 -m http.server 8080
# open http://localhost:8080
```

## Files

| File | What it is |
|---|---|
| `index.html` | Page structure, styling and UI wiring (colour picker, hex input, random button, copy-on-click swatches). |
| `palette.js` | Framework-free colour maths: `hexToHsl`, `hslToHex`, `generatePalette`, `toCssGradient`. Also runs under node for testing. |
| `README.md` | This file. |

## Notes

- Type a hex code (e.g. `#7c5cff` or shorthand `abc`) or pick from the colour input.
- Invalid input flashes the text field red instead of breaking the page.
- The "Random" button generates a palette from a random base colour.
- Small demo exercise — not a production design system.
