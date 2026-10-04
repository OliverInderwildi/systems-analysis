# Event tree analysis, with an evidence ledger

*Prose CC BY 4.0; code MIT. The method in §1 is not ours — see ATTRIBUTION.md.*

## 1. Origin — the method as published

Where a fault tree works backwards from one failure to the combinations that cause it, an
event tree works forwards from one initiating event through the barriers meant to contain it,
to the several outcomes that follow. The technique was developed for the Reactor Safety Study
(WASH-1400, 1975) under Norman C. Rasmussen, and is set out alongside fault trees in the
*Fault Tree Handbook* (NUREG-0492, 1981), ch. III.

The procedure:

1. Name the **initiating event** and its frequency.
2. List the **barriers** in the order they would actually act.
3. Branch on each: it works, or it does not. A tree of *n* barriers has 2ⁿ paths.
4. Multiply along each path — the barrier's failure probability where it failed, its
   complement where it held — and by the initiating frequency.
5. Assign an **end state** to each path, and total the frequency of each end state.

**Citation status.** Chapter-level attribution confirmed. Page-level references to be added
from the primary PDFs before v1.0; nothing here rests on a secondary summary.

## 2. What the code does, and where it departs

Implemented: enumeration of all paths; path and end-state frequencies; ranking of the paths to
the worst end state; a closure check that the conditional probabilities sum to one; severity
ranking of end states.

Our adaptations, stated as such:

1. **Barriers are assumed independent.** The published method treats dependence and common
   cause explicitly; we do not, yet. A tree whose barriers share a support system will be
   optimistic.
2. **Binary branches only.** No partial success, no multi-state branches.
3. **End states are assigned by pattern** (`SSF`, `FFS`, …) rather than drawn as a table of
   consequences. Same content, terser input.
4. **Severity is a declared integer rank**, ours, so the report can lead with the worst
   outcome rather than the most frequent.
5. No time dependence, no recovery actions, no uncertainty propagation.

Where our result and SCRAM's differ, SCRAM is right and this is a bug.

## 3. What is ours

The recording layer, which lives in [`csakernel`](../csakernel) and is shared across the tools.
Applied here it means:

- **no path is quantified on an unsourced number** — the initiating frequency and every
  barrier probability need an origin, a generation method and a verbatim excerpt, or the
  analysis is refused;
- **a path inherits the weakest evidence class among the initiator and the barriers that
  *failed* on it.** This is our reading, and it deserves its reason: a barrier that held
  contributes its complement, which is insensitive to the same degree of error, so counting it
  would flatten every path to one class and say nothing. The numbers that carry a path's
  probability are the ones that failed;
- **absence is reported** — what has no source, what was asserted, what rests on a single
  origin;
- **authorship is recorded** — initiator and each barrier carry whether a source, the analyst,
  or a language model put them there;
- **coupling is flagged** — a barrier probability taken from a fault tree's top event inherits
  that tree's weakest input, and the report says so rather than letting a composed number look
  like a measured one.

That last point is where the pair earns its keep. In practice an event tree's barrier
probabilities *are* fault tree results, and the composition is exactly where provenance gets
lost.

## 4. Use

```
python3 -m pet.cli analyse examples/datacentre/model.json examples/datacentre/ledger.json
```

The example is the same data centre the fault tree module analyses backwards, and it uses the
same ledger rows — one ledger, two methods.
