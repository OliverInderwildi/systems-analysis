"""What the sequences add up to."""
from __future__ import annotations

from typing import Dict, List

from .model import EventTree
from .sequences import Sequence, sequences


def end_state_frequencies(tree: EventTree, seqs: List[Sequence] | None = None) -> Dict[str, float]:
    """Total frequency of each end state - the answer an event tree exists to give."""
    seqs = seqs if seqs is not None else sequences(tree)
    out: Dict[str, float] = {}
    for s in seqs:
        out[s.end_state] = out.get(s.end_state, 0.0) + s.frequency
    order = sorted(out, key=lambda st: (-tree.severity.get(st, 0), -out[st]))
    return {st: out[st] for st in order}


def dominant_sequences(tree: EventTree, end_state: str,
                       seqs: List[Sequence] | None = None) -> List[Sequence]:
    """The paths to one end state, heaviest first."""
    seqs = seqs if seqs is not None else sequences(tree)
    return sorted((s for s in seqs if s.end_state == end_state),
                  key=lambda s: -s.frequency)


def closure_error(tree: EventTree, seqs: List[Sequence] | None = None) -> float:
    """Every path is accounted for, so the conditional probabilities must sum to one.

    This is the arithmetic's own check: a non-zero result means a barrier probability or the
    enumeration is wrong.
    """
    seqs = seqs if seqs is not None else sequences(tree)
    return abs(sum(s.conditional for s in seqs) - 1.0)
