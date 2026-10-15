#!/usr/bin/env node
/*
 * markdown-toc — a tiny CLI that generates a table of contents
 * from the headings of a Markdown file.
 *
 * Usage:
 *   node toc.js <file.md>        # print TOC to stdout
 *   node toc.js <file.md> -i     # insert/replace TOC in place
 *
 * In insert mode, the TOC is placed between these markers:
 *   <!-- TOC START -->
 *   <!-- TOC END -->
 * (the markers are created right after the first H1 if absent).
 *
 * This is a small demo/exercise project — not a production tool.
 */

const fs = require('fs');
const path = require('path');

function slugify(text) {
  // GitHub-style anchor slugs
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\p{L}\p{N}\s_-]/gu, '')
    .replace(/[\s]+/g, '-');
}

function extractHeadings(lines) {
  const headings = [];
  let inFence = false;
  for (const line of lines) {
    if (/^```/.test(line)) { inFence = !inFence; continue; }
    if (inFence) continue;
    const m = /^(#{1,6})\s+(.+?)\s*(?:#+\s*)?$/.exec(line);
    if (m) headings.push({ level: m[1].length, text: m[2].trim() });
  }
  return headings;
}

function buildToc(headings) {
  if (headings.length === 0) return '';
  const minLevel = Math.min(...headings.map(h => h.level));
  return headings
    .map(h => {
      const indent = '  '.repeat(h.level - minLevel);
      return `${indent}- [${h.text}](#${slugify(h.text)})`;
    })
    .join('\n');
}

function insertToc(content, toc) {
  const start = '<!-- TOC START -->';
  const end = '<!-- TOC END -->';
  const block = `${start}\n${toc}\n${end}`;
  if (content.includes(start) && content.includes(end)) {
    return content.replace(
      new RegExp(`${escapeRe(start)}[\\s\\S]*?${escapeRe(end)}`),
      block
    );
  }
  // Insert right after the first H1 line, or at the top
  const lines = content.split('\n');
  const h1 = lines.findIndex(l => /^#\s+/.test(l));
  const at = h1 === -1 ? 0 : h1 + 1;
  lines.splice(at, 0, '', block, '');
  return lines.join('\n');
}

function escapeRe(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function main() {
  const args = process.argv.slice(2);
  if (args.length < 1 || args.includes('-h') || args.includes('--help')) {
    console.log('Usage: node toc.js <file.md> [-i]\n');
    console.log('  Print a Markdown table of contents for the headings in <file.md>.');
    console.log('  -i   Insert/replace the TOC in the file between <!-- TOC START --> markers.');
    process.exit(args.length < 1 ? 1 : 0);
  }
  const file = args[0];
  const inPlace = args.includes('-i');
  if (!fs.existsSync(file)) {
    console.error(`Error: file not found: ${file}`);
    process.exit(1);
  }
  const content = fs.readFileSync(file, 'utf8');
  const toc = buildToc(extractHeadings(content.split('\n')));
  if (!toc) {
    console.error('No headings found — nothing to do.');
    process.exit(1);
  }
  if (inPlace) {
    fs.writeFileSync(file, insertToc(content, toc), 'utf8');
    console.log(`TOC written to ${path.basename(file)}`);
  } else {
    console.log(toc);
  }
}

main();
