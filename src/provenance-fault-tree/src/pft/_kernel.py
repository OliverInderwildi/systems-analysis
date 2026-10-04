"""Locate csakernel.

Normally it is installed (`pip install csakernel`, or `pip install -e ../CSAKernel`).
If it is not, but a sibling checkout exists, use that, so the two repositories can be
developed side by side without installation.
"""
import os
import sys

try:  # pragma: no cover - exercised by whichever path is present
    import csakernel  # noqa: F401
except ImportError:
    _here = os.path.dirname(__file__)
    _candidates = [
        os.path.abspath(os.path.join(_here, "..", "..", "..", "csakernel", "src")),   # monorepo
        os.path.abspath(os.path.join(_here, "..", "..", "..", "..", "csakernel", "src")),
        os.path.abspath(os.path.join(_here, "..", "..", "..", "CSAKernel", "src")),   # side by side
    ]
    for _path in _candidates:
        if os.path.isdir(_path):
            sys.path.insert(0, _path)
            break
    else:
        raise ImportError(
            "csakernel is required. Install it (pip install -e ../csakernel) or keep a "
            "checkout of it beside this tool."
        )
    import csakernel  # noqa: F401
