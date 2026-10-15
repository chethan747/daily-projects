# markdown-toc

A tiny Node.js command-line tool that generates a **table of contents** from the headings of a Markdown file. Small demo/exercise project — not a production tool.

## The idea

Long README files are easier to navigate with a clickable table of contents, but hand-writing one is tedious and it goes stale whenever a heading changes. This script scans a Markdown file for `#` headings (ignoring headings inside fenced code blocks), builds an indented list with GitHub-style anchor links, and can either print it or insert it directly into the file between `<!-- TOC START -->` / `<!-- TOC END -->` markers — re-running the script with `-i` refreshes the TOC instead of duplicating it.

## Files

- `toc.js` — the CLI (no dependencies, runs on plain Node.js)
- `sample.md` — a sample document to try it on
- `README.md` — this file

## How to run

```bash
# Print the TOC of a file
node toc.js sample.md

# Insert (or refresh) the TOC inside the file itself
node toc.js sample.md -i
```

No build step and no dependencies — just Node.js.
