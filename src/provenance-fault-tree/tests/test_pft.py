"""Tests. Hand calculations are given in the assertions so they can be checked by eye."""
import copy
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pft.cutsets import minimal_cut_sets, minimise          # noqa: E402
from pft.evidence import Ledger, LedgerError, evidence_report, weakest  # noqa: E402
from pft.model import BasicEvent, FaultTree, Gate, ModelError, load_model  # noqa: E402
from pft.quant import fussell_vesely, top_probability        # noqa: E402

HERE = os.path.dirname(__file__)
EX = os.path.join(HERE, "..", "examples", "backup_power")


def simple_tree():
    return FaultTree(
        top="TOP",
        gates={"TOP": Gate("TOP", "OR", ["G1", "E3"]), "G1": Gate("G1", "AND", ["E1", "E2"])},
        events={"E1": BasicEvent("E1", probability=0.1, ledger_ref="C-001"),
                "E2": BasicEvent("E2", probability=0.2, ledger_ref="C-002"),
                "E3": BasicEvent("E3", probability=0.05, ledger_ref="C-003")},
    )


def ledger_for(classes):
    rows = []
    for i, cls in enumerate(classes, start=1):
        rows.append({
            "id": f"C-{i:03d}", "claim": "x", "excerpt": "quoted text",
            "provenance": {"origin": "some source", "generation_method": "measured",
                           "classification": "benign", "independent_origins": 2},
            "evidence_class": cls, "status": "verified",
        })
    return Ledger(rows)


class TestCutSets(unittest.TestCase):
    def test_or_of_and(self):
        cuts = [sorted(c) for c in minimal_cut_sets(simple_tree())]
        self.assertEqual(cuts, [["E3"], ["E1", "E2"]])

    def test_supersets_discarded(self):
        got = [sorted(s) for s in minimise([frozenset({"A"}), frozenset({"A", "B"}), frozenset({"B"})])]
        self.assertEqual(got, [["A"], ["B"]])

    def test_cycle_rejected(self):
        ft = FaultTree(top="TOP",
                       gates={"TOP": Gate("TOP", "OR", ["G1"]), "G1": Gate("G1", "OR", ["TOP"])},
                       events={})
        with self.assertRaises(ModelError):
            ft.validate()

    def test_undefined_input_rejected(self):
        ft = FaultTree(top="TOP", gates={"TOP": Gate("TOP", "OR", ["NOPE"])}, events={})
        with self.assertRaises(ModelError):
            ft.validate()


class TestQuant(unittest.TestCase):
    def test_exact_union(self):
        ft = simple_tree()
        cuts = minimal_cut_sets(ft)
        # P = P(E3) + P(E1)P(E2) - P(E1)P(E2)P(E3) = 0.05 + 0.02 - 0.001
        self.assertAlmostEqual(top_probability(cuts, ft), 0.069, places=12)

    def test_rare_event_is_upper_bound(self):
        ft = simple_tree()
        cuts = minimal_cut_sets(ft)
        self.assertAlmostEqual(top_probability(cuts, ft, exact=False), 0.07, places=12)
        self.assertGreater(top_probability(cuts, ft, exact=False), top_probability(cuts, ft))

    def test_fussell_vesely(self):
        ft = simple_tree()
        cuts = minimal_cut_sets(ft)
        fv = fussell_vesely(cuts, ft)
        # denominator 0.05 + 0.02 = 0.07; E3 carries 0.05, E1 and E2 carry 0.02 each
        self.assertAlmostEqual(fv["E3"], 0.05 / 0.07, places=12)
        self.assertAlmostEqual(fv["E1"], 0.02 / 0.07, places=12)


class TestProvenanceLayer(unittest.TestCase):
    def test_refuses_without_ledger_ref(self):
        ft = simple_tree()
        ft.events["E1"].ledger_ref = ""
        with self.assertRaises(LedgerError) as ctx:
            evidence_report(ft, ledger_for(["established"] * 3), minimal_cut_sets(ft))
        self.assertIn("no ledger reference", str(ctx.exception))

    def test_refuses_without_excerpt(self):
        ft = simple_tree()
        led = ledger_for(["established"] * 3)
        led.rows["C-001"]["excerpt"] = "   "
        with self.assertRaises(LedgerError) as ctx:
            evidence_report(ft, led, minimal_cut_sets(ft))
        self.assertIn("verbatim excerpt", str(ctx.exception))

    def test_cut_set_inherits_weakest_class(self):
        self.assertEqual(weakest(["established", "asserted", "modelled"]), "asserted")
        ft = simple_tree()
        # E1 established, E2 asserted, E3 established -> cut {E1,E2} is asserted
        led = ledger_for(["established", "asserted", "established"])
        rep = evidence_report(ft, led, minimal_cut_sets(ft))
        by_cut = {tuple(r["cut_set"]): r["evidence_class"] for r in rep["cut_sets"]}
        self.assertEqual(by_cut[("E1", "E2")], "asserted")
        self.assertEqual(by_cut[("E3",)], "established")

    def test_absence_census_flags_single_origin(self):
        ft = simple_tree()
        led = ledger_for(["established"] * 3)
        led.rows["C-002"]["provenance"]["independent_origins"] = 1
        rep = evidence_report(ft, led, minimal_cut_sets(ft))
        flagged = {r["event"] for r in rep["absence_census"]}
        self.assertEqual(flagged, {"E2"})

    def test_authorship_counted(self):
        ft = simple_tree()
        ft.events["E3"].authored_by = "model"
        rep = evidence_report(ft, ledger_for(["established"] * 3), minimal_cut_sets(ft))
        self.assertEqual(rep["structure_authorship"]["model"], 1)


class TestExample(unittest.TestCase):
    def test_example_is_wholly_asserted(self):
        ft = load_model(os.path.join(EX, "model.json"))
        led = Ledger.load(os.path.join(EX, "ledger.json"))
        cuts = minimal_cut_sets(ft)
        rep = evidence_report(ft, led, cuts)
        self.assertEqual(rep["weakest_class_carrying_mass"], "asserted")
        self.assertAlmostEqual(rep["share_by_evidence_class"]["asserted"], 1.0, places=12)
        self.assertEqual(len(cuts), 3)
        # P(TOP) = P(grid) * P(any backup failure), backup = OR of three
        self.assertAlmostEqual(top_probability(cuts, ft), 0.02 * (1 - 0.99 * 0.995 * 0.996), places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestIndependentVerification(unittest.TestCase):
    """The cut-set route and exhaustive state enumeration must agree."""

    def test_agrees_on_simple_tree(self):
        from pft.verify import exact_top_probability
        ft = simple_tree()
        cuts = minimal_cut_sets(ft)
        self.assertAlmostEqual(top_probability(cuts, ft), exact_top_probability(ft), places=12)

    def test_agrees_on_example(self):
        from pft.verify import exact_top_probability
        ft = load_model(os.path.join(EX, "model.json"))
        cuts = minimal_cut_sets(ft)
        self.assertAlmostEqual(top_probability(cuts, ft), exact_top_probability(ft), places=12)

    def test_agrees_on_a_harder_tree(self):
        from pft.verify import exact_top_probability
        # shared event across branches: the case where the rare-event sum goes wrong
        ft = FaultTree(
            top="TOP",
            gates={"TOP": Gate("TOP", "OR", ["G1", "G2"]),
                   "G1": Gate("G1", "AND", ["E1", "E2"]),
                   "G2": Gate("G2", "AND", ["E2", "E3", "E4"])},
            events={"E1": BasicEvent("E1", probability=0.3, ledger_ref="C-001"),
                    "E2": BasicEvent("E2", probability=0.4, ledger_ref="C-002"),
                    "E3": BasicEvent("E3", probability=0.25, ledger_ref="C-003"),
                    "E4": BasicEvent("E4", probability=0.5, ledger_ref="C-004")},
        )
        ft.validate()
        cuts = minimal_cut_sets(ft)
        self.assertEqual([sorted(c) for c in cuts], [["E1", "E2"], ["E2", "E3", "E4"]])
        self.assertAlmostEqual(top_probability(cuts, ft), exact_top_probability(ft), places=12)
        # and the rare-event approximation overstates it, as it must
        self.assertGreater(top_probability(cuts, ft, exact=False), exact_top_probability(ft))


class TestRepeatedEvent(unittest.TestCase):
    """A basic event appearing in two branches: the case that makes a row non-minimal.

    Mirrors the worked example: the UPS bridges through the same hardware, so the hardware
    fault sits both at the top and under the UPS. {grid, hardware} must then be discarded,
    because {hardware} alone is already sufficient.
    """

    def setUp(self):
        self.ft = load_model(os.path.join(HERE, "..", "examples", "processing_power_backed",
                                          "model.json"))

    def test_repeated_event_makes_a_row_non_minimal(self):
        cuts = [sorted(c) for c in minimal_cut_sets(self.ft)]
        self.assertIn(["E_HW"], cuts)
        self.assertNotIn(["E_GRID", "E_HW"], cuts)   # struck: contains E_HW
        self.assertEqual(len(cuts), 4)

    def test_expansion_produces_then_discards_it(self):
        from pft.cutsets import expand_steps
        steps = list(expand_steps(self.ft))
        before_min = [sorted(s) for s in steps[-2]["sets"]]
        after_min = [sorted(s) for s in steps[-1]["sets"]]
        self.assertIn(["E_GRID", "E_HW"], before_min)
        self.assertNotIn(["E_GRID", "E_HW"], after_min)

    def test_both_routes_still_agree(self):
        from pft.verify import exact_top_probability
        cuts = minimal_cut_sets(self.ft)
        self.assertAlmostEqual(top_probability(cuts, self.ft),
                               exact_top_probability(self.ft), places=12)
