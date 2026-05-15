"""Validate cmp_strongarm: clocked StrongARM comparator.

Testbench: VCM=0.45V (VDD/2), diff=1mV (VINP=450.5mV, VINN=449.5mV), polarity swaps at 2ns.
Clock: 1GHz, VDD=0.9V.

Expected:
  - Before swap (t < 2ns):  vinp > vinn (+1mV) -> out_p HIGH, out_n LOW
  - After  swap (t > 2ns):  vinp < vinn (-1mV) -> out_p LOW,  out_n HIGH
"""
from pathlib import Path

import numpy as np

OUT = Path(__file__).parent.parent.parent / 'output' / 'comparator' / 'cmp_strongarm'

_VTH = 0.45   # half of VDD=0.9


def _sample(t_s, values, t_query_s):
    return np.interp(t_query_s, t_s, values)


def validate_csv(out_dir: Path = OUT) -> int:
    data = np.genfromtxt(out_dir / 'tran.csv', delimiter=',', names=True, dtype=None, encoding='utf-8')
    failures = 0

    out_p  = data['out_p']
    out_n  = data['out_n']

    # Both outputs must toggle (non-trivial comparator decisions)
    if out_p.max() - out_p.min() < _VTH:
        print("FAIL: out_p never toggles")
        failures += 1
    if out_n.max() - out_n.min() < _VTH:
        print("FAIL: out_n never toggles")
        failures += 1

    # Sample away from clock/source transition boundaries. Row fractions depend
    # on each simulator's accepted transient points, but these decision points
    # describe the intended comparator behavior directly.
    decisions = []
    for t_sample_ns in (0.75, 1.75, 2.75, 3.75):
        p = _sample(data['time'], out_p, t_sample_ns * 1e-9)
        n = _sample(data['time'], out_n, t_sample_ns * 1e-9)
        if p > _VTH and n < _VTH:
            decisions.append('P')
        elif p < _VTH and n > _VTH:
            decisions.append('N')
        else:
            decisions.append('X')

    if decisions != ['P', 'P', 'N', 'N']:
        print(f"FAIL: decision samples {''.join(decisions)} (expected PPNN)")
        failures += 1

    if failures == 0:
        print("[CSV] All assertions passed.")
    return failures


if __name__ == '__main__':
    raise SystemExit(0 if validate_csv() == 0 else 1)
