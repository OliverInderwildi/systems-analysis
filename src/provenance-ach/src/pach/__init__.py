"""Analysis of Competing Hypotheses, with an evidence ledger.

The method is Richards J. Heuer Jr's; the recording rules are csakernel's. See METHOD.md.
"""
from .model import Matrix, MatrixError, load_matrix, RATINGS
from .score import diagnosticity, inconsistency_scores, rank_hypotheses
from .report import ach_report

__all__ = ["Matrix", "MatrixError", "load_matrix", "RATINGS",
           "diagnosticity", "inconsistency_scores", "rank_hypotheses", "ach_report"]
__version__ = "0.1.0"
