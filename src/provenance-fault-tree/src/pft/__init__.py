"""ProvenanceFaultTree - fault tree analysis that refuses to run without provenance.

The analysis itself is a re-implementation of published procedures (NUREG-0492).
The provenance layer is ours. See METHOD.md and ATTRIBUTION.md.
"""
from .model import FaultTree, load_model, ModelError
from .cutsets import minimal_cut_sets
from .quant import cutset_probability, top_probability, fussell_vesely
from .evidence import Ledger, LedgerError, evidence_report

__all__ = [
    "FaultTree", "load_model", "ModelError",
    "minimal_cut_sets",
    "cutset_probability", "top_probability", "fussell_vesely",
    "Ledger", "LedgerError", "evidence_report",
]
__version__ = "0.1.0"
