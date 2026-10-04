"""Plain decimals, not exponents.

8e-07 is precise and unreadable to most people; 0.0000008 is the same number and needs no
translation. Frequencies here are small, so everything is written out in full.
"""
from __future__ import annotations


def decimal(x: float, sig: int = 3) -> str:
    """Format a probability or frequency as a plain decimal string."""
    if x == 0:
        return "0"
    if abs(x) >= 1:
        return f"{x:,.{sig}f}".rstrip("0").rstrip(".")
    # enough places to carry `sig` significant figures
    from math import floor, log10
    places = max(0, -int(floor(log10(abs(x)))) - 1 + sig)
    return f"{x:.{places}f}".rstrip("0").rstrip(".")


def percent(x: float, sig: int = 2) -> str:
    return decimal(x * 100, sig) + "%"
