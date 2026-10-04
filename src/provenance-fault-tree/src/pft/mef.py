"""Export to the Open-PSA Model Exchange Format, so SCRAM can recompute the same model.

SCRAM (Olzhas Rakhimov, GPL-3.0) is a separate program; we write a file it reads and, if it
is installed, run it and compare. We never link against it. See ATTRIBUTION.md.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from xml.etree import ElementTree as ET

from .model import FaultTree


def to_mef(ft: FaultTree, name: str = "model") -> str:
    root = ET.Element("opsa-mef")
    ftree = ET.SubElement(root, "define-fault-tree", {"name": name})
    for gid, gate in ft.gates.items():
        d = ET.SubElement(ftree, "define-gate", {"name": gid})
        op = ET.SubElement(d, "and" if gate.type == "AND" else "or")
        for child in gate.inputs:
            tag = "gate" if child in ft.gates else "basic-event"
            ET.SubElement(op, tag, {"name": child})
    modeldata = ET.SubElement(root, "model-data")
    for eid, ev in ft.events.items():
        d = ET.SubElement(modeldata, "define-basic-event", {"name": eid})
        f = ET.SubElement(d, "float", {"value": repr(ev.probability)})
        f.text = None
    return ET.tostring(root, encoding="unicode")


def scram_available() -> bool:
    return shutil.which("scram") is not None


def run_scram(ft: FaultTree, name: str = "model", extra_args=()) -> str:
    """Run SCRAM on this model if it is installed. Returns its report XML."""
    if not scram_available():
        raise RuntimeError("scram is not installed; install it separately (GPL-3.0)")
    with tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False) as fh:
        fh.write(to_mef(ft, name))
        path = fh.name
    proc = subprocess.run(["scram", "--probability", "true", *extra_args, path],
                          capture_output=True, text=True, check=True)
    return proc.stdout
