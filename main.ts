// gta6-meme-x-01 entrypoint, written for this entry (Node 22, stdlib only).
// The meme itself lives on X: this program only hands the gate the post's
// address. Before copying anything it checks POST.json really names a live
// X status URL, so a leftover placeholder can never slip into /output.
//
// Local run: mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const POST_URL = /^https:\/\/x\.com\/[A-Za-z0-9_]+\/status\/[0-9]+$/;

const postPath = join(BOT_DIR, 'POST.json');
let post: unknown;
try {
  post = JSON.parse(readFileSync(postPath, 'utf8'));
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

const url = (post as { url?: unknown } | null)?.url;
if (typeof url !== 'string' || !POST_URL.test(url)) {
  console.error(
    `POST.json does not name a real X post (expected https://x.com/<handle>/status/<id>, got ${JSON.stringify(url)}). ` +
      `Replace the placeholder with your posted meme's URL before submitting.`,
  );
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(postPath, join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied to ${OUTPUT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
console.log(`OK: ${url}`);
