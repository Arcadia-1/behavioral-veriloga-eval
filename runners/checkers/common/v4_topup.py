"""Pure helpers used by the migrated v4 303-319 checker slice."""
from __future__ import annotations

def _v4_code_from_bits(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << idx) for idx, bit in enumerate(bits) if _v4_topup_logic_high(row, bit))

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def _v4_topup_clip01(value: float, low: float = 0.0, high: float = 0.9) -> float:
    return max(low, min(high, value))

def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_topup_near(value: float, expected: float, tol: float) -> bool:
    return abs(float(value) - expected) <= tol

def _v4_topup_span(rows: list[dict[str, float]], name: str) -> float:
    vals = [float(row[name]) for row in rows if name in row]
    return max(vals) - min(vals) if vals else 0.0
