"""Enumerate the paths through the tree.

Each barrier is asked in turn; the tree branches on whether it works. A path of n barriers is
a string of n characters - S where the barrier did its job, F where it did not - and carries
the product of the probabilities along it. Independence between barriers is assumed, as in the
published method; common-cause coupling is not modelled here (see METHOD.md).
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import List

from .model import EventTree


@dataclass
class Sequence:
    index: int
    pattern: str            # e.g. "SF" - first barrier held, second failed
    end_state: str
    conditional: float      # probability of this path, given the initiating event
    frequency: float        # conditional x initiator frequency
    failed: List[str]       # ids of the barriers that failed on this path

    @property
    def id(self) -> str:
        return f"S{self.index:02d}"


def sequences(tree: EventTree) -> List[Sequence]:
    out: List[Sequence] = []
    for i, combo in enumerate(product("SF", repeat=len(tree.barriers)), start=1):
        pattern = "".join(combo)
        p = 1.0
        failed = []
        for barrier, state in zip(tree.barriers, combo):
            if state == "F":
                p *= barrier.failure_probability
                failed.append(barrier.id)
            else:
                p *= 1.0 - barrier.failure_probability
        out.append(Sequence(index=i, pattern=pattern,
                            end_state=tree.outcomes.get(pattern, tree.default_outcome),
                            conditional=p, frequency=p * tree.initiator.frequency,
                            failed=failed))
    return out
