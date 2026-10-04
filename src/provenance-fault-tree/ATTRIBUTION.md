# Attribution

This project is a thin layer on top of other people's work. The method is not ours; the
implementation of the classical algorithms is a re-implementation of published procedures.
What we add is stated in `METHOD.md` under "What is ours", and nowhere else.

## The method

**Fault Tree Analysis** as set out in:

> W. E. Vesely, F. F. Goldberg, N. H. Roberts and D. F. Haasl,
> *Fault Tree Handbook*, NUREG-0492, U.S. Nuclear Regulatory Commission, January 1981.
> https://www.nrc.gov/docs/ML1007/ML100780465.pdf (U.S. federal work, public domain)

Second, independent statement of the same method, used here as a cross-check:

> *Fault Tree Handbook with Aerospace Applications*, version 1.1,
> NASA Office of Safety and Mission Assurance, 2002. (U.S. federal work, public domain)

Fault tree analysis itself originates with H. A. Watson and colleagues at Bell Telephone
Laboratories (Minuteman programme, 1961–62) and was developed further by D. F. Haasl and
others at Boeing. The minimal cut set expansion implemented here follows the top-down
procedure described in NUREG-0492; the algorithm is commonly known as MOCUS, after
J. B. Fussell, E. B. Henry and N. H. Marshall (1974). The importance measure implemented
here is the Fussell-Vesely importance.

## The existing code we build on and interoperate with

> **SCRAM** — Probabilistic Risk Analysis Tool, by Olzhas Rakhimov and contributors.
> https://github.com/rakhimov/scram — GPL-3.0.

SCRAM is a complete, maintained implementation of fault tree and event tree analysis.
This project does **not** copy, modify or link against SCRAM. It writes models in the
**Open-PSA Model Exchange Format**, which SCRAM reads, so that any analysis run here can be
independently recomputed by SCRAM. Where the two disagree, SCRAM is right and we have a bug.

> **Open-PSA Model Exchange Format** — the Open-PSA initiative.

## Provenance vocabulary

The `generation_method` and `evidence_class` vocabularies are taken unchanged from the
Provenance-Based Evidence Audit module in this repository family, so that a fault tree
ledger and an evidence ledger can be read by the same tools.

## Licensing

Our own code: MIT (see `LICENSE`). Our own prose (METHOD.md, docs): CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
SCRAM: GPL-3.0, invoked as a separate program if present, never bundled or linked.
The handbooks above are U.S. federal works and carry no copyright in the United States;
they are cited, and quoted only briefly and with attribution.
