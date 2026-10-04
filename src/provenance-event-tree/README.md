# ProvenanceEventTree

Event tree analysis — forwards from one initiating event, through the barriers, to the
outcomes — that refuses to run on numbers with no source.

The method is the one developed for the Reactor Safety Study (WASH-1400, 1975) and set out in
the *Fault Tree Handbook* (NUREG-0492, 1981), ch. III. **We claim none of it.** What this adds
is the shared recording layer: no barrier probability without its origin, each path carrying
the weakest evidence among the barriers that failed on it, and every element marked with who
put it there — a source, the analyst, or a language model.

<table>
<tr>
<th align="left" width="52%">The example</th>
<th align="left">What is in here</th>
</tr>
<tr valign="top">
<td>

```
$ python3 -m pet.cli analyse \
    examples/datacentre/model.json \
    examples/datacentre/ledger.json

Initiating event : Grid outage  0.02 per period (demonstrated)

End states, most severe first:
  Immediate loss of processing power     0.0000008      weakest: asserted
  Load lost when the battery depletes    0.000199       weakest: asserted
  Load lost when fuel runs out           0.000099       weakest: asserted
  Momentary interruption                 0.0000788      weakest: demonstrated
  Load maintained                        0.0196         weakest: demonstrated

Paths to 'Immediate loss of processing power':
  S07  FFS  0.000000796   modelled      failed: UPS bridges, Generator starts
  S08  FFF  0.000000004   asserted      failed: UPS bridges, Generator starts, Fuel holds


Closure check: paths sum to 1.000000000
```

</td>
<td>

```
provenance-event-tree/
├── README.md          this file
├── METHOD.md          published / adapted / ours
├── ATTRIBUTION.md     whose method this is
├── CITATION.cff       how to cite
├── LICENSE            MIT
├── src/pet/
│   ├── model.py       initiator, barriers, outcomes
│   ├── sequences.py   path enumeration
│   ├── quant.py       end states, closure check
│   ├── evidence.py    the provenance layer
│   └── cli.py         the command above
├── examples/datacentre/
│   ├── model.json     grid outage, 3 barriers
│   └── ledger.json    the fault tree's own rows
├── tests/             13 tests
└── skill/SKILL.md     how to build one from a corpus
```

**Runs with** Python 3.10+, the standard library,
and [`csakernel`](../csakernel).

```
PYTHONPATH=src python3 -m unittest discover -s tests
```

**Pairs with** [`provenance-fault-tree`](../provenance-fault-tree):
the same system, analysed backwards. The two
examples share ledger rows, which is the point —
one ledger, two methods.

</td>
</tr>
</table>

![The event tree](https://oliverinderwildi.github.io/Infographics/event-tree/event_tree.png)

![What survives each barrier](https://oliverinderwildi.github.io/Infographics/event-tree/survival.png)

Status: v0.1. Verified against hand calculations and against an independent recursive walk of
the same tree; the Open-PSA route to SCRAM is the next cross-check.
