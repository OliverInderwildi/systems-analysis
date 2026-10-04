# ProvenanceACH

Heuer's Analysis of Competing Hypotheses, with an evidence ledger attached.

The method is Richards J. Heuer, Jr.'s, from *Psychology of Intelligence Analysis* (1999,
public domain) — judge hypotheses by what contradicts them, and discount evidence that fits
everything. **We claim none of it.** What this adds is the recording layer shared across these
modules ([`csakernel`](../csakernel)): no evidence without a source, the conclusion inherits the
weakest evidence that did the discriminating, an absence census, and — the part that is new —
a record of whether each hypothesis and each item of evidence came from a source, the analyst,
or a language model.

```
$ python3 -m pach.cli analyse examples/toy/matrix.json examples/toy/ledger.json

Hypotheses, least inconsistent first (Heuer: the one hardest to reject):
  H2       0.00  [analyst]  Workload was moved to another site
  H3       0.00  [model]    A metering change altered what is recorded
  H1       2.80  [analyst]  Efficiency upgrades reduced actual consumption
...
WARNING: H2 and H3 are equally hard to reject; the matrix does not separate them
WARNING: 3 item(s) of evidence do no work (E1, E4, E5): consistent with every hypothesis
WARNING: 2 element(s) of this matrix were proposed by a language model, not found in a source
```

`METHOD.md` — the method as published, our adaptations, what is ours.
`ATTRIBUTION.md` — credit and licences.
Tests: `PYTHONPATH=src python3 -m unittest discover -s tests`. Python 3.10+, standard library
plus `csakernel`.
