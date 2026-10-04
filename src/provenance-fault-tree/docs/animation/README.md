# The cut-set animation

Designed page; the content is generated. `cutsets-data.js` comes from
`../gen_cutsets_data.py`, which runs `pft.cutsets.expand_steps` over the two example models —
so every row, every gate replacement and the struck row are engine output, not prose.

- `index.dc.html` — the source page (loads `support.js`, `cutsets-data.js`, `_ds/heritage`)
- `standalone.html` — self-contained bundle, opens with no server
- `cutsets.gif` — exported loop, 864x540, 19 settled frames

Regenerate the data after any model change:

    cd ../.. && PYTHONPATH=src python3 docs/gen_cutsets_data.py && cp docs/cutsets-data.js docs/animation/

Design and design system: heritage kit, Public Sans substituted for licensed Helvetica Neue.
Method credit is on the page itself: Vesely, Goldberg, Roberts & Haasl, NUREG-0492 (1981).
