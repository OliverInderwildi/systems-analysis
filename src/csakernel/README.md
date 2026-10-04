# csakernel

The recording rules shared by every module in this family of tools. It performs no analysis.
It says:

- **nothing enters an analysis unsourced** — every value needs a ledger row with an origin, a
  generation method, and a verbatim excerpt locating it in that source (`require_sourced`)
- **weak evidence propagates** — a result inherits the weakest evidence class among its
  inputs (`weakest`)
- **absence is an output** — what has no source, what was asserted rather than derived, and
  what rests on a single origin (`absence_census`)
- **changes are recorded** — an append-only evolution log (`EvolutionLog`)
- **authorship is recorded** — source, analyst or model (`AUTHORS`)

The vocabularies (`generation_method`, `evidence_class`) are unchanged from the
Provenance-Based Evidence Audit, so ledgers are interchangeable between modules.

Used by: `provenance-fault-tree`. Python 3.10+, standard library only. MIT.
