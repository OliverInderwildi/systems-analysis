# Fault tree analysis with an evidence ledger

*Prose in this file: CC BY 4.0. Code: MIT. The method described in §1 is not ours; see ATTRIBUTION.md.*

## 1. Origin — the method as published

Fault tree analysis was devised by H. A. Watson and colleagues at Bell Telephone Laboratories
for the Minuteman programme in 1961–62, and developed at Boeing, notably by D. F. Haasl. The
procedure implemented here follows the U.S. Nuclear Regulatory Commission's handbook:

> W. E. Vesely, F. F. Goldberg, N. H. Roberts, D. F. Haasl, *Fault Tree Handbook*,
> NUREG-0492, USNRC, January 1981.

Steps, with the chapters of that handbook in which they are set out:

| Step | Where |
|---|---|
| Fault/failure distinction, component fault categories, construction rules | ch. V |
| Boolean representation, normal forms, determining minimal cut sets and path sets | ch. VII |
| Worked example: pressure tank | ch. VIII |
| Worked example: three motors | ch. IX |
| Probabilistic and statistical evaluation | ch. X |
| Fault tree evaluation techniques | ch. XI |

The top-down cut set expansion implemented in `cutsets.py` is the procedure commonly called
MOCUS (Fussell, Henry and Marshall, 1974). The importance measure in `quant.py` is the
Fussell–Vesely importance.

**Citation status.** Chapter attributions above are confirmed against the handbook's own
contents. Page-level references are still to be added, from the PDF, before v1.0; this file
will not carry a page number that has not been read. Nothing here rests on a secondary
source's summary of the handbook.

## 2. What the code does, and where it departs from the handbook

Implemented: AND and OR gates; top-down minimal cut set expansion with superset elimination;
cut set probability as a product; top probability exactly by inclusion–exclusion for up to 16
cut sets, otherwise the rare-event sum (an upper bound); Fussell–Vesely importance; export to
the Open-PSA Model Exchange Format so that SCRAM can recompute the same model.

Our adaptations, stated as such:

1. **Independence assumed** between basic events. The handbook treats dependence and common
   cause; we do not, yet. Models with shared causes will be optimistic.
2. **No NOT gates** (non-coherent trees), no k-of-n gates, no event trees. SCRAM does all of
   these; where a model needs them, use SCRAM.
3. **Exactness threshold** of 16 cut sets before falling back to the rare-event approximation
   is our engineering choice, not the handbook's.
4. **No repair or time-dependent unavailability.** Probabilities are per-demand or
   per-period constants supplied by the analyst.

Where our result and SCRAM's differ, SCRAM is right and this is a bug.

## 3. What is ours

Only this: the handbook is silent on where the numbers come from. The layer in `evidence.py`
makes that question unavoidable.

- **P1 — no input without provenance.** A basic event may not enter an analysis unless the
  ledger holds a row for it naming an origin, a generation method, and a verbatim excerpt
  locating the number in that source. Otherwise the analysis is refused, not warned about.
- **P2 — inheritance.** Every minimal cut set carries the weakest evidence class among its
  inputs. A cut set of three established numbers and one asserted number is asserted.
- **P3 — no bare headline.** The top probability is reported alongside the distribution of
  probability mass across evidence classes.
- **P4 — absence census.** What has no source, what rests on a single origin, and what was
  asserted rather than derived, reported as a first-class output rather than a silent default.
- **P5 — importance against evidence.** Fussell–Vesely importance is reported next to the
  evidence class of the same event, so that a result driven by an asserted number is visible
  in one line.
- **P6 — authorship of the structure.** Every gate and event records who put it there:
  the source document, the human analyst, or a language model. The report counts them.

P6 is the part that belongs to the present decade. When a model proposes the shape of a fault
tree from a corpus, the tree's structure is itself a claim, and it needs provenance exactly as
its numbers do. We know of no fault tree tool that records it.

These rules are not implemented here. They live in `csakernel`, the shared kernel every module
in this family imports, so that P1-P6 are one statement applied to many methods rather than a
claim restated per tool. This module supplies only the fault-tree specifics: which items need
sourcing (the basic events), and how inheritance runs (through minimal cut sets).

The vocabularies (`generation_method`, `evidence_class`) are unchanged from the
Provenance-Based Evidence Audit module, so a fault tree ledger and an evidence ledger can be
read by the same tools.

## 4. Use

```
python3 -m pft.cli analyse examples/backup_power/model.json examples/backup_power/ledger.json
```

The bundled example is deliberately unflattering: every probability in it is asserted by the
analyst, and the report says so in the first three lines. That is what most fault trees look
like once the question is asked.
