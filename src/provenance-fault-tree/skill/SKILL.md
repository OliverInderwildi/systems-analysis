---
name: provenance-fault-tree
description: Build a fault tree from a document corpus and analyse it with an evidence ledger, so that every probability carries its origin and every part of the tree records who authored it. Use when asked to assess how a system fails, to audit an existing reliability or risk claim, or to turn outage/failure documentation into a quantified model.
---

# Building a fault tree that can be audited

The arithmetic is the published method (NUREG-0492). Your job is the part a handbook cannot
do: turning a corpus into a model without inventing anything, and marking what you authored.

## Procedure

1. **Scope.** State the top event in one sentence, with its boundary and period
   ("loss of IT load at site X during a one-year period"). Record what is out of scope.
2. **Structure before numbers.** Develop the tree top-down: for each event ask what
   combination of lower events causes it, AND for co-requirements, OR for alternatives. Stop
   at events for which a probability can be sourced. Do not reach for numbers yet.
3. **Mark authorship as you go.** Every gate and event takes `authored_by`:
   - `source` — the structure is stated in a document you can quote
   - `analyst` — the human put it there
   - `model` — you proposed it
   Never mark your own proposal as `source`. If a document merely implies the relation, it is
   `model`, and say so in the report.
4. **One ledger row per basic event.** Each row needs: `origin` (the document, with locator),
   `generation_method` (measured, modelled, estimated, derived, argued, excavated, asserted),
   `evidence_class` (established, demonstrated, modelled, asserted), `independent_origins`,
   and an `excerpt` quoting the sentence or table cell the number comes from, verbatim.
5. **Do not fill gaps with plausible numbers.** If a probability has no source, either leave
   the event out of the quantified model and list it in the absence census, or enter it with
   `generation_method: asserted` and an excerpt saying whose assumption it is. Both are
   honest; a fabricated citation is not.
6. **Run it.** `python3 -m pft.cli analyse model.json ledger.json --json report.json`.
   The tool refuses to run on unsourced inputs — fix the ledger, never the check.
7. **Report in this order:** what drives the result, on what evidence, what is missing, and
   only then the number. If the weakest class carrying probability mass is `asserted`, say so
   in the first sentence.
8. **Offer the cross-check.** If SCRAM is installed, export with `--mef` and compare; report
   any disagreement as a defect in this tool.

## What not to do

- Do not present a top probability without its evidence distribution.
- Do not quietly repair a refused analysis by inventing an origin.
- Do not describe a structure you proposed as one the literature states.
- Do not treat repeated appearance of a number in several documents as confirmation; check
  whether they share one origin (that is the provenance audit's job, and cascades are common).
