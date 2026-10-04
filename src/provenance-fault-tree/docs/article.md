# Reverse-engineering failure: fault tree analysis in four steps

*Draft, 29 September 2026. Text CC BY 4.0.*

How much would it cost you if the lights went out for an hour? Not your lights – the ones in
the building where your workloads actually run. Somewhere in that building sits a diesel
generator that nobody has started since the last test, a fuel contract nobody has read, and a
battery that is meant to bridge the gap between the two. The interesting question is not
whether those things are reliable. It is which combinations of them failing would be enough,
on their own, to take the load down.

That question has a method attached to it, and the method is older than most of the equipment.
You start from the failure you want to prevent, work backwards through the ways it could come
about, and end with a list of combinations. Each combination is called a **cut set**: a set of
basic failures that is sufficient, by itself, to produce the failure at the top. Nothing about
it is forward-looking, and nothing about it is forensic. You are not explaining an outage that
happened. You are mapping the ones that could.

The pay-off comes after the analysis, and it is worth being clear that this part is not the
algorithm's. Once you know the cut sets, you know what kind of fix works. A cut set containing
a single event is a single point of failure: nothing else has to go wrong, so only removing or
duplicating that element helps. Adding redundancy is precisely the act of turning a one-event
cut set into a two-event one. And an element that appears in *every* cut set cannot be fixed by
adding more devices in parallel at all – that is a common-cause problem, and decoupling, not
duplication, is the answer.

There is a third lever, and in a standby system it is usually the cheapest one. Half the
equipment in our example spends its life doing nothing: the generator, the fuel line, the
battery. Their failures are **dormant** – they have already happened, and nobody knows, because
nothing has asked the equipment to work. The generator that cannot start may have been unable
to start since March. Three practices address this, and they are
worth keeping apart. **Preventive maintenance** services equipment on a schedule, by calendar
or by run hours, whether or not anything looks wrong – oil changes, filter swaps, batteries
replaced at end of design life. **Predictive**, or condition-based, maintenance acts on
indicators instead: vibration, oil analysis, battery impedance trending. And **proof testing**,
also called functional or surveillance testing, simply starts the thing to find out whether it
still starts – the monthly load-bank run, the quarterly transfer test. The test interval is
what sets how long a dormant failure can sit undiscovered. Which of the three a given component
deserves is itself a discipline, reliability-centred maintenance, and it is a discipline
precisely because doing all three everywhere is unaffordable.

None of this makes the equipment more reliable. It shortens the window in which the system is
already broken and the operator still believes otherwise – and in a fault tree, that window is
a large part of what the probability of a standby component's basic event actually measures.

The method tells you how the failure could happen. What to change remains a judgement, and it
remains yours.

## Whose method this is

Fault tree analysis was devised by H. A. Watson and colleagues at Bell Telephone Laboratories
in 1961–62, for the launch control system of the Minuteman missile, and developed further at
Boeing, notably by D. F. Haasl. Its standard reference is the *Fault Tree Handbook*
(NUREG-0492, 1981) by W. E. Vesely, F. F. Goldberg, N. H. Roberts and D. F. Haasl, written for
the U.S. Nuclear Regulatory Commission and in the public domain. The cut set expansion used
here is the procedure known as MOCUS, after J. B. Fussell, E. B. Henry and N. H. Marshall
(1974), and the importance measure is the Fussell–Vesely importance. Complete implementations
exist; [SCRAM](https://github.com/rakhimov/scram), by Olzhas Rakhimov, is the one we test
against. None of that is our work and we claim none of it. What we added is one layer, and it
comes at the end of this piece.

## The four steps, on one system

Take a small data centre: grid supply, a standby generator with its own fuel supply, and a UPS
to bridge between them. The failure we want to prevent is loss of the IT load. The method runs
in four steps, and the figure below shows all four on this one system.

![Reverse-engineering failure](https://oliverinderwildi.github.io/Briefings/fault-tree-analysis/fig3_cutsets_final.png)

**Step one** writes the failure as a tree. Loss of the load requires the grid to fail *and* the
backup to be unavailable – an AND gate, because both are needed. Backup power is unavailable if
the generator fails to start *or* the fuel supply fails *or* the UPS fails to bridge – an OR
gate, because any one of them is enough.

**Steps two and three** turn the tree into combinations. Begin with one row containing the
failure itself. Then replace each gate by its inputs: an AND gate makes a row wider, because
everything in it is needed, while an OR gate turns one row into several, because each input is
sufficient on its own.

**Step four** discards any row that contains another, because a bigger combination that
includes a smaller one is not minimal. Three rows survive: the grid outage with the generator
failing, with the fuel supply failing, or with the UPS failing.

Read that result against the prevention question and it becomes uncomfortable. Every row
contains the grid outage. Adding a fourth backup device would not change the structure of the
answer at all, because the structure says that grid supply is the common factor in every way
this system loses its load.

## The layer we added

Here is what the handbook, written in 1981 for an industry with data books and decades of
plant records, had no reason to discuss: where the numbers come from. A fault tree takes a
probability for each basic event, and the arithmetic treats them all alike. A failure rate
drawn from ten years of operating records and a figure somebody put in a slide deck enter the
calculation in the same way and leave it indistinguishable. In the places where these models
now get used – grid adequacy studies, availability claims, infrastructure policy – that gap is
often not filled at all.

So our version refuses to run without provenance. No basic event enters the analysis unless
the evidence ledger holds a row naming its origin, the method by which the number was produced,
and a verbatim excerpt locating it in that source. Every cut set then inherits the weakest
evidence class among its inputs: three well-measured numbers and one assumption make an
asserted cut set, because that is what it is. The top probability is never reported alone. It
arrives with the share of probability mass resting on each class of evidence, with a census of
what has no source at all, and with each event's importance set beside the quality of the
number behind it.

![Probability mass by evidence class](https://oliverinderwildi.github.io/Briefings/fault-tree-analysis/fig1_mass_by_evidence.png)

The example is deliberately unflattering. The headline figure looks precise to two significant
figures. Four-fifths of it rests on one number somebody modelled and one number somebody
assumed. That is not a criticism of the analyst – it is the ordinary condition of such models,
and it stays invisible unless the tool insists on showing it.

![Importance against evidence](https://oliverinderwildi.github.io/Briefings/fault-tree-analysis/fig2_importance_evidence.png)

The second figure is the one we reach for most. It puts each event's Fussell–Vesely importance
next to the evidence class of its probability, so the awkward case – the event that drives the
result and rests on the weakest evidence – is a single line rather than an exercise in
cross-referencing.

There is one more rule, and it is the reason this is a 2026 project rather than a 1981 one.
When a language model helps build the tree, reading outage reports and proposing what causes
what, the structure of the tree becomes a claim as much as its numbers are. So every gate and
every event records who put it there: a source document, the human analyst, or the model. The
report counts them. We know of no other fault tree tool that does this, and we suspect it will
soon be indefensible not to.

## What we are not claiming

The method is Vesely, Goldberg, Roberts and Haasl's. The expansion is Fussell, Henry and
Marshall's. The importance measure is Fussell–Vesely. The reference implementation is SCRAM,
and where our results differ from SCRAM's, SCRAM is right and we have a bug. Our contribution
is the evidence layer, and nothing else.

The current version assumes independent basic events, handles AND and OR gates only, and is
verified against hand calculations and against an independent exhaustive evaluation of the same
trees. It has not yet been checked against the handbook's own worked examples, which is the
next thing on the list. Code is MIT, prose CC BY 4.0, both at
`github.com/oliverinderwildi/systems-analysis` (folder `src/provenance-fault-tree`).
