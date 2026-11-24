// news-image-20261123 entry program (Node 22, standard library only).
//
// The poster is pre-rendered as entry.png next to this file. At grade time
// this program does exactly one thing: copy those bytes into the output
// directory. It renders nothing, reads no fonts, opens no network
// connection, and uses no randomness, so repeated runs write identical
// bytes.
//
// Run outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
