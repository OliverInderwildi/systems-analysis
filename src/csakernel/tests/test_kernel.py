import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from csakernel import (EvolutionLog, Ledger, LedgerError, absence_census,  # noqa: E402
                       is_weaker, require_sourced, weakest)


def row(rid, cls="established", gm="measured", origin="a source", excerpt="quoted", origins=2):
    return {"id": rid, "claim": "x", "excerpt": excerpt,
            "provenance": {"origin": origin, "generation_method": gm,
                           "classification": "benign", "independent_origins": origins},
            "evidence_class": cls, "status": "verified"}


class TestVocab(unittest.TestCase):
    def test_weakest(self):
        self.assertEqual(weakest(["established", "modelled"]), "modelled")
        self.assertEqual(weakest([]), "asserted")
        self.assertEqual(weakest(["nonsense"]), "asserted")
        self.assertTrue(is_weaker("asserted", "established"))


class TestRequireSourced(unittest.TestCase):
    def setUp(self):
        self.led = Ledger([row("C-001"), row("C-002", excerpt="  "),
                           row("C-003", origin=""), row("C-004", gm="telepathy")])

    def test_passes_when_sourced(self):
        require_sourced({"a": "C-001"}, self.led)

    def test_reports_every_problem_at_once(self):
        with self.assertRaises(LedgerError) as ctx:
            require_sourced({"a": "", "b": "C-002", "c": "C-003", "d": "C-004", "e": "C-999"}, self.led)
        msg = str(ctx.exception)
        for expected in ["no ledger reference", "verbatim excerpt", "origin is empty",
                         "generation_method", "no row 'C-999'"]:
            self.assertIn(expected, msg)

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(LedgerError):
            Ledger([row("C-001"), row("C-001")])


class TestCensus(unittest.TestCase):
    def test_flags_assertion_and_single_origin(self):
        led = Ledger([row("C-001"), row("C-002", cls="asserted", gm="asserted", origins=0)])
        out = {r["item"]: r["missing"] for r in absence_census({"a": "C-001", "b": "C-002"}, led)}
        self.assertNotIn("a", out)
        self.assertIn("asserted", out["b"])
        self.assertIn("single origin", out["b"])


class TestLog(unittest.TestCase):
    def test_append_and_roundtrip(self):
        import tempfile
        log = EvolutionLog()
        log.record("added E_FUEL", "reviewer asked for the fuel path", "analyst", when="2026-09-23")
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "log.json")
            log.save(p)
            again = EvolutionLog.load(p)
        self.assertEqual(len(again), 1)
        self.assertEqual(again.entries[0]["by"], "analyst")


if __name__ == "__main__":
    unittest.main()


class TestCensusAssertedClass(unittest.TestCase):
    def test_flags_asserted_evidence_class_even_when_argued(self):
        led = Ledger([row("C-009", cls="asserted", gm="argued", origins=2)])
        out = absence_census({"x": "C-009"}, led)
        self.assertIn("evidence class is asserted", out[0]["missing"])
