"""Tests. Hand calculations appear in the assertions so they can be checked by eye."""
import os
import sys
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "csakernel", "src"))

from csakernel import Ledger, LedgerError                      # noqa: E402
from pet.evidence import event_tree_report, sequence_evidence  # noqa: E402
from pet.model import EventTree, ModelError, load_model        # noqa: E402
from pet.quant import closure_error, end_state_frequencies     # noqa: E402
from pet.sequences import sequences                            # noqa: E402

EX = os.path.join(HERE, "..", "examples", "datacentre")


def tree():
    return load_model(os.path.join(EX, "model.json"))


def ledger():
    return Ledger.load(os.path.join(EX, "ledger.json"))


def walk(tree_, i=0, p=1.0, pattern=""):
    """Independent route: recurse down the tree instead of enumerating patterns."""
    if i == len(tree_.barriers):
        state = tree_.outcomes.get(pattern, tree_.default_outcome)
        return {state: p * tree_.initiator.frequency}
    b = tree_.barriers[i]
    out = {}
    for state, q in (("S", 1.0 - b.failure_probability), ("F", b.failure_probability)):
        for k, v in walk(tree_, i + 1, p * q, pattern + state).items():
            out[k] = out.get(k, 0.0) + v
    return out


class TestSequences(unittest.TestCase):
    def test_every_path_is_enumerated(self):
        self.assertEqual(len(sequences(tree())), 2 ** 3)

    def test_paths_close_to_one(self):
        self.assertLess(closure_error(tree()), 1e-12)

    def test_hand_calculation_of_the_success_path(self):
        s = next(s for s in sequences(tree()) if s.pattern == "SSS")
        # 0.02 x (1-0.004) x (1-0.01) x (1-0.005)
        self.assertAlmostEqual(s.frequency, 0.02 * 0.996 * 0.99 * 0.995, places=15)
        self.assertEqual(s.end_state, "Load maintained")

    def test_end_states_sum_to_the_initiating_frequency(self):
        t = tree()
        self.assertAlmostEqual(sum(end_state_frequencies(t).values()),
                               t.initiator.frequency, places=15)


class TestIndependentVerification(unittest.TestCase):
    def test_enumeration_agrees_with_a_recursive_walk(self):
        t = tree()
        a, b = end_state_frequencies(t), walk(t)
        self.assertEqual(set(a), set(b))
        for state in a:
            self.assertAlmostEqual(a[state], b[state], places=15)


class TestModelValidation(unittest.TestCase):
    def test_pattern_width_must_match_the_barriers(self):
        t = tree()
        t.outcomes["SS"] = "nonsense"
        with self.assertRaises(ModelError):
            t.validate()

    def test_duplicate_barrier_rejected(self):
        t = tree()
        t.barriers.append(t.barriers[0])
        with self.assertRaises(ModelError):
            t.validate()

    def test_missing_outcome_without_default_rejected(self):
        t = tree()
        t.outcomes.pop("FFF")
        with self.assertRaises(ModelError):
            t.validate()


class TestProvenanceLayer(unittest.TestCase):
    def test_refuses_an_unsourced_barrier(self):
        t = tree()
        t.barriers[0].ledger_ref = ""
        with self.assertRaises(LedgerError):
            event_tree_report(t, ledger())

    def test_path_inherits_the_weakest_failed_barrier(self):
        t, led = tree(), ledger()
        by_pattern = {s.pattern: s for s in sequences(t)}
        # generator is modelled, fuel asserted, UPS and the initiator demonstrated
        self.assertEqual(sequence_evidence(t, led, by_pattern["SFS"]), "modelled")
        self.assertEqual(sequence_evidence(t, led, by_pattern["SSF"]), "asserted")
        self.assertEqual(sequence_evidence(t, led, by_pattern["FSS"]), "demonstrated")

    def test_worst_end_state_is_chosen_by_severity_not_frequency(self):
        rep = event_tree_report(tree(), ledger())
        worst = rep["worst_end_state"]
        self.assertEqual(worst, "Immediate loss of processing power")
        # it is also the rarest - severity has to win, or the report misleads
        freqs = rep["end_state_frequencies"]
        self.assertEqual(min(freqs, key=lambda k: freqs[k]), worst)

    def test_model_authored_barrier_is_reported(self):
        rep = event_tree_report(tree(), ledger())
        self.assertEqual(rep["authorship"]["model"], 1)
        self.assertTrue(any("language model" in w for w in rep["warnings"]))


class TestSharedLedger(unittest.TestCase):
    def test_the_fault_tree_ledger_rows_are_the_same_rows(self):
        """One ledger, two methods - the point of the kernel."""
        ft_ledger = Ledger.load(os.path.join(HERE, "..", "..", "provenance-fault-tree",
                                             "examples", "processing_power_backed",
                                             "ledger.json"))
        led = ledger()
        for ref in ("C-001", "C-002", "C-003", "C-006"):
            self.assertEqual(led.get(ref)["claim"], ft_ledger.get(ref)["claim"])
            self.assertEqual(led.evidence_class(ref), ft_ledger.evidence_class(ref))


if __name__ == "__main__":
    unittest.main(verbosity=2)
