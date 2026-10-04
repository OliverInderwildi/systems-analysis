---
name: provenance-event-tree
description: Build an event tree from a document corpus and quantify it with an evidence ledger, so every barrier probability carries its origin and every element records who authored it. Use when asked what follows from a failure, to assess whether protections hold, or to turn incident and outage documentation into quantified sequences.
---

# Building an event tree that can be audited

The arithmetic is the published method. Your job is turning a corpus into a tree without
inventing anything, and marking what you authored.

## Procedure

1. **Name the initiating event** and the period ("a grid supply outage at site X, per year").
   Its frequency needs a source like any other number.
2. **List the barriers in the order they act**, not in order of importance. A UPS bridges
   before a generator starts; get that wrong and the sequences are wrong.
3. **Mark authorship as you go** — `source` when a document states the barrier exists,
   `analyst` when the human added it, `model` when you proposed it. Never mark your own
   proposal as `source`.
4. **One ledger row per number**: the initiating frequency and each barrier's probability of
   failing on demand, each with `origin`, `generation_method`, `evidence_class`,
   `independent_origins` and a verbatim `excerpt`.
5. **Assign an end state to every path.** If two paths differ only in a barrier that no longer
   matters once an earlier one failed, they may share an end state — say so, don't hide it.
6. **Rank the end states by severity**, so the report leads with the worst outcome rather than
   the most frequent. The rarest sequence is often the one that matters.
7. **Run it.** `python3 -m pet.cli analyse model.json ledger.json`. The closure check must
   read 1.000000000; if it does not, a probability is wrong.
8. **Report in this order:** the worst end state, the paths that reach it, the evidence those
   paths rest on, what is missing, and only then the frequencies.

## When a barrier probability comes from a fault tree

That is the normal case, and it is where provenance is usually lost. Record
`from_fault_tree` on the barrier, and carry the fault tree's weakest input class through — a
composed number must not read as a measured one.

## What not to do

- Do not invent a barrier because the sequence looks too short.
- Do not quietly assume independence between barriers that share a power supply, a control
  system or a maintenance crew; say the assumption out loud.
- Do not report an end-state frequency without the evidence class beneath it.
