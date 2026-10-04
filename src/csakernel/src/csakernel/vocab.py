"""The vocabularies. Taken unchanged from the Provenance-Based Evidence Audit module so that
an evidence ledger and an analysis ledger can be read by the same tools."""
from __future__ import annotations

from typing import Iterable

# weakest first - the order is the inheritance order
EVIDENCE_CLASSES = ("asserted", "modelled", "demonstrated", "established")

GENERATION_METHODS = ("measured", "modelled", "estimated", "derived",
                      "argued", "excavated", "asserted")

# who put an element of a model where it is
AUTHORS = ("source", "analyst", "model")


def rank(evidence_class: str) -> int:
    """Position in the strength order; unknown classes count as weakest."""
    try:
        return EVIDENCE_CLASSES.index(evidence_class)
    except ValueError:
        return 0


def weakest(classes: Iterable[str]) -> str:
    """The weakest class present. Nothing known means 'asserted'."""
    ranks = [rank(c) for c in classes if c in EVIDENCE_CLASSES]
    return EVIDENCE_CLASSES[min(ranks)] if ranks else "asserted"


def is_weaker(a: str, b: str) -> bool:
    return rank(a) < rank(b)
