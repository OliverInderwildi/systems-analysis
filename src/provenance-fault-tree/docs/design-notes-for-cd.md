# Notes back to the design — 30 Sep 2026 (second pass)

## Verified, again
`cutsets-data.js` arrived byte-identical to the generator's output (same MD5), the page reads
it via `window.CUTSETS`, and no hardcoded rows remain. The struck row renders exactly as the
data specifies — row 05, Grid outage · Hardware fault, "CONTAINS 01" — and the closing frame
carries the generated sentence verbatim. Both earlier items are closed: one legend, and a
scale wrapper instead of a hard 1440px.

## The change we want: a stepper, not autoplay
Drop autoplay. Put a long bar along the bottom with back / forward controls, so the reader
advances at their own pace. This also removes the export problem below.

Worth building into the bar rather than bolting on:
- **Segment it by step.** The 19 frames map onto the four steps; four labelled zones with
  tick marks inside each means the bar doubles as the step indicator now at the top.
- **Make the ticks clickable**, and bind the arrow keys.
- **Mark the two moments that matter:** the frame where the design changes (backup added)
  and the frame where the row is struck out. Jumping straight to those beats scrubbing.
- **Keep a first-frame cue** — without motion, a static first frame reads as a still image.
  A quiet "step through →" beside the bar earns its place.
- **It collides with the feedback strip**, which sits in that band today. Either the bar
  replaces it and the feedback line moves into the frame caption, or they stack.

## Why this also fixes the GIF
The exported GIF was 76 frames: 19 settled at 2,800 ms and 57 cross-fade frames at 60 ms.
A cross-fade cannot fade in a GIF, so those frames stack both states — ghosted, doubled text.
We have stripped them for the README copy: 19 frames, 2,600 ms each, 0.5 MB (was 2.5 MB).
With a stepper there is no timeline to export at all; the GIF stays only as the README
fallback, since GitHub will not run JavaScript.

If a fresh export is made, export the settled states only, with hard cuts.
