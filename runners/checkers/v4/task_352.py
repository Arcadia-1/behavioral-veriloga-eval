"""Task-specific checker for canonical v4 DUT 352."""
from __future__ import annotations

from dataclasses import dataclass

from ..api import Checker


@dataclass
class PropertyDiagnostic:
    property_id: str
    checked: int = 0
    mismatch_count: int = 0
    expected: str = "contract_satisfied"
    observed: str = "contract_satisfied"
    sample_time: float = 0.0
    metric_gap: float = 0.0

    def mismatch(self, *, expected: object, observed: object, time: float, gap: float = 0.0) -> None:
        self.mismatch_count += 1
        if self.mismatch_count == 1:
            self.expected = str(expected)
            self.observed = str(observed)
            self.sample_time = float(time)
            self.metric_gap = float(gap)

    def render(self) -> str:
        return (
            f"{self.property_id} checked={self.checked} mismatch_count={self.mismatch_count} "
            f"expected={self.expected} observed={self.observed} "
            f"sample_time={self.sample_time:.12g} metric_gap={self.metric_gap:.6g}"
        )


def _rising_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if not last and cur:
            times.append(row["time"])
        last = cur
    return times


def _sample_after(rows: list[dict[str, float]], t: float, delay: float = 5e-9) -> dict[str, float]:
    target = t + delay
    return min(rows, key=lambda row: abs(row["time"] - target))


def _v4_missing_columns(rows: list[dict[str, float]], required: set[str]) -> str | None:
    if not rows:
        return "missing_columns=" + ",".join(sorted(required)[:16])
    missing = sorted(required - set(rows[0].keys()))
    if missing:
        return "missing_columns=" + ",".join(missing[:16])
    return None


def _v4_code(row: dict[str, float], names_lsb_first: list[str], vth: float = 0.45) -> int:
    return sum((1 << bit) for bit, name in enumerate(names_lsb_first) if row[name] > vth)


def _v4_clip(value: float, lo: float = 0.0, hi: float = 0.9) -> float:
    return max(lo, min(hi, value))


def _v4_close(actual: float, expected: float, tol: float = 0.07) -> bool:
    return abs(actual - expected) <= tol


def check_v4_ctle_equalizer_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clk", "rst", "boost_2", "boost_1", "boost_0", "vout", "edge_metric", "sat_flag"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, (
            f"P_TRACE checked=1 mismatch_count=1 expected=complete_trace "
            f"observed={missing} sample_time=0 metric_gap=1"
        )

    diagnostics = {
        name: PropertyDiagnostic(name)
        for name in ("P_OUTPUT_TRANSFER", "P_EDGE_METRIC", "P_SATURATION", "P_EXCITATION")
    }
    prev_in = 0.45
    checked = 0
    codes_seen: set[int] = set()
    sat_seen = False
    metric_seen = False
    for edge_t in _rising_times(rows, "clk"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        if edge_row["rst"] > 0.45:
            prev_in = 0.45
            expected_out = 0.45
            expected_metric = 0.0
            expected_sat = 0.0
        else:
            code = _v4_code(edge_row, ["boost_0", "boost_1", "boost_2"])
            codes_seen.add(code)
            edge = edge_row["vin"] - prev_in
            raw = 0.45 + (edge_row["vin"] - 0.45) + 0.08 * code * edge
            expected_sat = 0.9 if raw > 0.9 or raw < 0.0 else 0.0
            expected_out = _v4_clip(raw)
            expected_metric = min(0.9, abs(0.08 * code * edge))
            sat_seen = sat_seen or expected_sat > 0.45
            metric_seen = metric_seen or expected_metric > 0.03
            prev_in = edge_row["vin"]

        sample = _sample_after(rows, edge_t, 0.8e-9)
        diagnostics["P_OUTPUT_TRANSFER"].checked += 1
        if not _v4_close(sample["vout"], expected_out, 0.08):
            diagnostics["P_OUTPUT_TRANSFER"].mismatch(
                expected=f"vout={expected_out:.6g}",
                observed=f"vout={sample['vout']:.6g}",
                time=edge_t,
                gap=abs(sample["vout"] - expected_out),
            )
        diagnostics["P_EDGE_METRIC"].checked += 1
        if not _v4_close(sample["edge_metric"], expected_metric, 0.07):
            diagnostics["P_EDGE_METRIC"].mismatch(
                expected=f"edge_metric={expected_metric:.6g}",
                observed=f"edge_metric={sample['edge_metric']:.6g}",
                time=edge_t,
                gap=abs(sample["edge_metric"] - expected_metric),
            )
        diagnostics["P_SATURATION"].checked += 1
        if (sample["sat_flag"] > 0.45) != (expected_sat > 0.45):
            diagnostics["P_SATURATION"].mismatch(
                expected=f"sat_flag={int(expected_sat > 0.45)}",
                observed=f"sat_flag={int(sample['sat_flag'] > 0.45)}",
                time=edge_t,
                gap=1.0,
            )
        checked += 1

    diagnostics["P_EXCITATION"].checked = 1
    coverage_ok = checked >= 8 and len(codes_seen) >= 4 and metric_seen and sat_seen
    if not coverage_ok:
        diagnostics["P_EXCITATION"].mismatch(
            expected="checked>=8 codes>=4 metric_seen=true sat_seen=true",
            observed=(
                f"checked={checked} codes={sorted(codes_seen)} "
                f"metric_seen={metric_seen} sat_seen={sat_seen}"
            ),
            time=float(rows[-1]["time"]),
            gap=float(max(0, 8 - checked) + max(0, 4 - len(codes_seen))),
        )
    ok = all(item.checked > 0 and item.mismatch_count == 0 for item in diagnostics.values())
    return ok, " ; ".join(item.render() for item in diagnostics.values())


CHECKER_ID = "v4_352_ctle_equalizer_macro"
CHECKER: Checker = check_v4_ctle_equalizer_macro
