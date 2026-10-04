"""csakernel - the recording rules shared by every analysis module.

This is the layer that is ours. It holds no analysis of its own: it says what must be known
about a number before an analysis may use it, how weak evidence propagates through a result,
what is reported when evidence is absent, and who authored each part of a model.

Modules (fault trees, ACH, ISM, ...) import these rules instead of restating them.
"""
from .vocab import (EVIDENCE_CLASSES, GENERATION_METHODS, AUTHORS,
                    weakest, is_weaker, rank)
from .ledger import Ledger, LedgerError, require_sourced
from .census import absence_census
from .log import EvolutionLog

__all__ = [
    "EVIDENCE_CLASSES", "GENERATION_METHODS", "AUTHORS", "weakest", "is_weaker", "rank",
    "Ledger", "LedgerError", "require_sourced", "absence_census", "EvolutionLog",
]
__version__ = "0.1.0"
