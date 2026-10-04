# Analysis of Competing Hypotheses, with an evidence ledger

*Prose CC BY 4.0; code MIT. The method in §1 is Heuer's — see ATTRIBUTION.md.*

## 1. Origin — the method as published

Richards J. Heuer, Jr. set out ACH in *Psychology of Intelligence Analysis* (CIA Center for the
Study of Intelligence, 1999), ch. 8, and it is restated in *A Tradecraft Primer* (U.S.
Government, 2009). Its central move is to judge hypotheses by the evidence **against** them
rather than for them, because evidence consistent with several hypotheses discriminates
between none of them. The procedure:

1. Enumerate the plausible hypotheses, including ones you disbelieve.
2. List the significant evidence and arguments.
3. Build the matrix: evidence down the side, hypotheses across the top.
4. Rate each cell for consistency with that hypothesis.
5. Refine: drop evidence consistent with everything; it does no work.
6. Draw conclusions by seeking to **disprove**: the surviving hypothesis is the one hardest
   to reject, not the one with the most support.
7. Report the relative likelihood of all hypotheses, and what would change the conclusion.

**Citation status.** Chapter-level attribution confirmed; page-level references to be added
from the primary PDFs before v1.0.

## 2. What the code does, and where it departs

Implemented: the matrix with Heuer's rating scale (CC, C, N, I, II, NA); weighted
inconsistency scores counting only disconfirming ratings (II = 2, I = 1); ranking by least
inconsistency; a diagnosticity measure over the spread of ratings across hypotheses.

Our adaptations, stated as such:

1. **Weights come from the ledger, not from judgement.** Heuer has the analyst assign each
   item a credibility weight. Here the weight is derived from the evidence class recorded in
   the ledger (established 1.0, demonstrated 0.8, modelled 0.5, asserted 0.25), so the
   weighting is traceable to a source. Explicit weights can still be supplied.
2. **Diagnosticity is scored, not eyeballed.** The published method asks the analyst to notice
   which evidence discriminates; we compute a number from the spread of ratings. It is a
   convenience, not part of Heuer's method.
3. **Every cell must be rated or marked NA.** The tool refuses a matrix with holes; the
   handbook tolerates them.
4. No Bayesian update, no sensitivity sweep over ratings yet.

## 3. What is ours

Only the recording layer, which lives in `csakernel` and is shared with the other modules:

- **no item of evidence without a source** — origin, generation method and a verbatim excerpt,
  or the analysis is refused;
- **the conclusion inherits the weakest evidence class among the items that actually
  discriminate** — a verdict resting on one asserted item is reported as asserted;
- **an absence census** of what has no source, what is asserted, and what rests on a single
  origin;
- **authorship of the matrix itself**: each hypothesis and each item of evidence records
  whether a source, the analyst, or a language model put it there. A model-proposed hypothesis
  is a legitimate part of the analysis and an illegitimate thing to hide, and the report says
  how many there are.

The last point matters more here than in most methods: a language model will happily generate
a plausible fifth hypothesis, and ACH's own logic means an unsourced hypothesis can change
which of the others survives.

## 4. Use

```
python3 -m pach.cli analyse examples/toy/matrix.json examples/toy/ledger.json
```
