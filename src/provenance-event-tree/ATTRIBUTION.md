# Attribution

## The method

**Event tree analysis** grew out of the reactor safety study led by Norman C. Rasmussen —
*Reactor Safety Study: An Assessment of Accident Risks in U.S. Commercial Nuclear Power
Plants*, WASH-1400 / NUREG-75/014, U.S. Nuclear Regulatory Commission, 1975 — which paired
event trees with fault trees to quantify accident sequences. The procedure implemented here
follows the handbook account:

> W. E. Vesely, F. F. Goldberg, N. H. Roberts, D. F. Haasl, *Fault Tree Handbook*,
> NUREG-0492, USNRC, January 1981 — ch. III, on event trees and their relation to fault trees.
> (U.S. federal work, public domain)

Later treatments consulted for terminology only: NUREG/CR-2300, *PRA Procedures Guide* (1983),
also a U.S. federal work.

## The existing code we interoperate with

> **SCRAM** — Probabilistic Risk Analysis Tool, Olzhas Rakhimov and contributors,
> https://github.com/rakhimov/scram — GPL-3.0. SCRAM implements event trees as well as fault
> trees. It is neither bundled nor linked here.

## Provenance vocabulary
`generation_method` and `evidence_class` are unchanged from the Provenance-Based Evidence
Audit, via [`csakernel`](../csakernel), so one ledger serves every tool in this repository.
The worked example deliberately reuses the fault tree example's ledger rows.

## Licensing
Code MIT (`LICENSE`); prose CC BY 4.0. The source texts above are U.S. federal works in the
public domain; they are cited, and quoted only briefly with attribution.
