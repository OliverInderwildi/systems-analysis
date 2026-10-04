# ProvenanceFaultTree

Fault tree analysis — backwards from one failure to the combinations that cause it — that
refuses to run on numbers with no source.

The method is the classical one: devised by H. A. Watson and colleagues at Bell Telephone
Laboratories (1961–62), developed at Boeing by D. F. Haasl, and set out by Vesely, Goldberg,
Roberts and Haasl in the *Fault Tree Handbook* (NUREG-0492, 1981). Complete implementations
exist — see [SCRAM](https://github.com/rakhimov/scram). **We claim none of it.** What this adds
is a layer the handbook has no reason to discuss: where the numbers come from.

<table>
<tr>
<th align="left" width="52%">The example</th>
<th align="left">What is in here</th>
</tr>
<tr valign="top">
<td>

```
$ python3 -m pft.cli analyse \
    examples/processing_power_backed/model.json \
    examples/processing_power_backed/ledger.json

Top event probability : 0.0006777
Weakest evidence class carrying
probability: asserted

Minimal cut sets:
  E_HW               0.0003    asserted
  E_GEN AND E_GRID   0.0002    modelled
  E_FUEL AND E_GRID  0.0001    asserted
  E_BATT AND E_GRID  0.00008   demonstrated

Probability mass by evidence class:
  asserted       58.8%
  modelled       29.4%
  demonstrated   11.8%

Importance (Fussell-Vesely) against evidence:
  E_GRID   55.9%  demonstrated  measured
  E_HW     44.1%  asserted      asserted
  E_GEN    29.4%  modelled      modelled
  E_FUEL   14.7%  asserted      asserted
  E_BATT   11.8%  demonstrated  measured
```

Small numbers are written out in full, never as
exponents.

</td>
<td>

```
provenance-fault-tree/
├── README.md          this file
├── METHOD.md          published / adapted / ours
├── ATTRIBUTION.md     whose method this is
├── CITATION.cff       how to cite
├── LICENSE            MIT
├── src/pft/
│   ├── model.py       gates, events, authorship
│   ├── cutsets.py     MOCUS expansion
│   ├── quant.py       probability, importance
│   ├── verify.py      independent check
│   ├── evidence.py    the provenance layer
│   ├── mef.py         Open-PSA export for SCRAM
│   └── cli.py         the command opposite
├── examples/
│   ├── processing_power/         as built
│   ├── processing_power_backed/  after the fix
│   └── backup_power{,_mixed}/    smaller cases
├── docs/
│   ├── article.md     the draft write-up
│   ├── figures.py     the three charts
│   ├── gen_cutsets_data.py   animation data
│   └── animation/     the designed page + GIF
├── tests/             19 tests
└── skill/SKILL.md     building one from a corpus
```

**Runs with** Python 3.10+, the standard library,
and [`csakernel`](../csakernel).

```
PYTHONPATH=src python3 -m unittest discover -s tests
```

**Pairs with**
[`provenance-event-tree`](../provenance-event-tree):
the same system, forwards. The two examples share
ledger rows — one ledger, two methods.

</td>
</tr>
</table>

![From tree to cut sets](https://oliverinderwildi.github.io/Infographics/fault-tree/cutsets.gif)

Status: v0.1. Verified against hand calculations and against an independent exhaustive
evaluation of the same trees; the Open-PSA export exists so SCRAM can check our arithmetic.
Where we disagree with SCRAM, SCRAM is right.
