"""Event tree analysis, with an evidence ledger.

Fault trees run backwards from one failure to the combinations that cause it. Event trees run
forwards from one initiating event through the barriers meant to stop it, to the several
outcomes that follow. The arithmetic is the published method; the recording layer is ours.
See METHOD.md and ATTRIBUTION.md.
"""
from .model import EventTree, ModelError, load_model
from .sequences import Sequence, sequences
from .quant import end_state_frequencies, dominant_sequences
from .evidence import event_tree_report

__all__ = ["EventTree", "ModelError", "load_model", "Sequence", "sequences",
           "end_state_frequencies", "dominant_sequences", "event_tree_report"]
__version__ = "0.1.0"
