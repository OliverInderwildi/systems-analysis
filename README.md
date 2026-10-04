# Systems analysis

Open tools for systems analysis. Each is a faithful implementation of a published method, with credit to its
authors, plus one thing the original does not have – most often a record of where every number came from.

| Tool | What it does | Method |
|---|---|---|
| [`csakernel`](src/csakernel) | The shared recording rules: nothing unsourced, weak evidence propagates, absence is an output | ours |
| [`provenance-fault-tree`](src/provenance-fault-tree) | Fault tree analysis with an evidence ledger | Watson (Bell Labs, 1961–62); Vesely et al., NUREG-0492 (1981) |
| [`provenance-event-tree`](src/provenance-event-tree) | Event tree analysis with an evidence ledger | Rasmussen, WASH-1400 (1975) |
| [`provenance-ach`](src/provenance-ach) | Analysis of competing hypotheses with an evidence ledger | Heuer, CIA (1999) |

Next: *Lexical Bridge* (`dictmatch`), linking texts that use different words.

Worked examples, figures and step-by-step animations are on the website: https://oliverinderwildi.github.io/code/

## Layout

- `src/<tool>/` – each tool with its own README, METHOD.md (what is published, what we adapted, what is ours),
  ATTRIBUTION.md, CITATION.cff, tests and small example inputs
- `docs/` – shared documentation
- `data/` – shared datasets

The provenance tools import `csakernel` from its sibling folder, so keep `src/` together.

## How to cite

Cite the collection with [`CITATION.cff`](CITATION.cff) (GitHub: "Cite this repository"), and the method of the tool you
used – each `src/<tool>/CITATION.cff` lists its references.

## Licence

Code: MIT ([`LICENSE`](LICENSE)). Prose in the tools' Markdown files: CC BY 4.0 where stated.
