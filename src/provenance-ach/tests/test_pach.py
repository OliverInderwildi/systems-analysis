import os
import sys
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "csakernel", "src"))

from csakernel import Ledger, LedgerError                       # noqa: E402
from pach.model import Matrix, MatrixError, load_matrix         # noqa: E402
from pach.report import ach_report                              # noqa: E402
from pach.score import (diagnosticity, inconsistency_scores,    # noqa: E402
                        rank_hypotheses, weights_from_ledger)

EX = os.path.join(HERE, "..", "examples", "toy")


class TestScoring(unittest.TestCase):
    def setUp(self):
        self.m = load_matrix(os.path.join(EX, "matrix.json"))

    def test_only_disconfirming_evidence_counts(self):
        scores = inconsistency_scores(self.m)   # unweighted
        # H1 is contradicted by E2 (II = 2) and E3 (I = 1); nothing else disconfirms it
        self.assertAlmostEqual(scores["H1"], 3.0)
        # H2 and H3 have no inconsistent ratings at all
        self.assertAlmostEqual(scores["H2"], 0.0)
        self.assertAlmostEqual(scores["H3"], 0.0)

    def test_ranking_puts_least_inconsistent_first(self):
        self.assertEqual(rank_hypotheses(self.m)[-1][0], "H1")

    def test_evidence_consistent_with_everything_is_not_diagnostic(self):
        diag = diagnosticity(self.m)
        self.assertEqual(diag["E5"], 0.0)   # consistent with all three
        self.assertGreater(diag["E2"], 0.0)

    def test_ledger_class_sets_the_weight(self):
        led = Ledger.load(os.path.join(EX, "ledger.json"))
        w = weights_from_ledger(self.m, led)
        self.assertEqual(w["E2"], 1.0)    # established
        self.assertEqual(w["E1"], 0.8)    # demonstrated
        self.assertEqual(w["E4"], 0.25)   # asserted


class TestMatrixValidation(unittest.TestCase):
    def test_needs_two_hypotheses(self):
        m = Matrix()
        with self.assertRaises(MatrixError):
            m.validate()

    def test_unrated_cell_rejected(self):
        m = load_matrix(os.path.join(EX, "matrix.json"))
        del m.ratings["E1"]["H2"]
        with self.assertRaises(MatrixError) as ctx:
            m.validate()
        self.assertIn("unrated", str(ctx.exception))


class TestReport(unittest.TestCase):
    def setUp(self):
        self.m = load_matrix(os.path.join(EX, "matrix.json"))
        self.led = Ledger.load(os.path.join(EX, "ledger.json"))

    def test_refuses_unsourced_evidence(self):
        self.m.evidence["E1"].ledger_ref = ""
        with self.assertRaises(LedgerError):
            ach_report(self.m, self.led)

    def test_reports_tie_and_model_authorship(self):
        rep = ach_report(self.m, self.led)
        joined = " ".join(rep["warnings"])
        self.assertIn("equally hard to reject", joined)
        self.assertIn("language model", joined)
        self.assertEqual(rep["authorship"]["model"], 2)

    def test_conclusion_inherits_weakest_working_evidence(self):
        rep = ach_report(self.m, self.led)
        # only E2 (established) and E3 (demonstrated) discriminate -> demonstrated
        self.assertEqual(rep["conclusion_evidence_class"], "demonstrated")


if __name__ == "__main__":
    unittest.main()
