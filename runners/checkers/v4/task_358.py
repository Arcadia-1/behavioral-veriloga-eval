"""Task-specific checker for canonical v4 DUT 358."""
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


def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold


def _v4_code_from_bits(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << idx) for idx, bit in enumerate(bits) if _v4_topup_logic_high(row, bit))


def _high_intervals(rows: list[dict[str, float]], signal: str, threshold: float = 0.45) -> list[tuple[float, float]]:
    """Find high intervals from the trace without relying on absolute timestamps."""
    if not rows:
        return []
    start = float(rows[0]["time"]) if _v4_topup_logic_high(rows[0], signal, threshold) else None
    intervals: list[tuple[float, float]] = []
    for previous, current in zip(rows, rows[1:]):
        was_high = _v4_topup_logic_high(previous, signal, threshold)
        is_high = _v4_topup_logic_high(current, signal, threshold)
        if not was_high and is_high:
            start = float(current["time"])
        elif was_high and not is_high and start is not None:
            intervals.append((start, float(current["time"])))
            start = None
    if start is not None:
        intervals.append((start, float(rows[-1]["time"])))
    return intervals


def check_v4_917_quadrature_phase_interpolator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_i", "clk_q", "rst", "code_0", "code_1", "code_2", "code_3", "code_4", "clk_out", "quadrant_0", "quadrant_1", "phase_metric"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, (
            "P_TRACE checked=1 mismatch_count=1 expected=complete_trace "
            f"observed=missing_columns={','.join(missing)} sample_time=0 metric_gap={len(missing)}"
        )

    diagnostics = {
        name: PropertyDiagnostic(name)
        for name in ("P_RESET_CLEAR", "P_PHASE_METRIC", "P_QUADRANT_CODE", "P_CLOCK_ACTIVITY")
    }
    checked = 0
    code_low = code_high = clk_activity = False
    clk_values: list[float] = []
    prev_code: int | None = None
    settle_until = 0.0

    reset_intervals = _high_intervals(rows, "rst")
    required_reset_count = 1
    diagnostics["P_RESET_CLEAR"].checked = max(1, len(reset_intervals))
    sampled_rows = rows[::6]
    for index, (start, end) in enumerate(reset_intervals):
        interval_rows = [row for row in sampled_rows if start <= float(row["time"]) <= end]
        clear = any(
            float(row["phase_metric"]) < 0.08
            and float(row["quadrant_0"]) < 0.08
            and float(row["quadrant_1"]) < 0.08
            and float(row["clk_out"]) < 0.12
            for row in interval_rows
        )
        if not clear:
            diagnostics["P_RESET_CLEAR"].mismatch(
                expected=f"reset_interval_{index + 1}=clear",
                observed=f"reset_interval_{index + 1}=not_clear",
                time=start,
                gap=1.0,
            )
    if len(reset_intervals) < required_reset_count:
        diagnostics["P_RESET_CLEAR"].mismatch(
            expected=f"reset_intervals>={required_reset_count}",
            observed=f"reset_intervals={len(reset_intervals)}",
            time=float(rows[-1]["time"]),
            gap=float(required_reset_count - len(reset_intervals)),
        )

    for row in sampled_rows:
        t = float(row["time"])
        if _v4_topup_logic_high(row, "rst"):
            prev_code = None
            settle_until = t
            continue
        code = _v4_code_from_bits(row, ["code_0", "code_1", "code_2", "code_3", "code_4"])
        if prev_code is None or code != prev_code:
            prev_code = code
            settle_until = t + 1.1e-9
            continue
        if t < settle_until:
            continue
        quadrant = code // 8
        expected_metric = 0.9 * code / 31.0
        expected_q1 = quadrant in (2, 3)
        expected_q0 = quadrant in (1, 3)
        code_low = code_low or code <= 4
        code_high = code_high or code >= 24
        clk_values.append(float(row["clk_out"]))
        checked += 1

        diagnostics["P_PHASE_METRIC"].checked += 1
        observed_metric = float(row["phase_metric"])
        metric_gap = abs(observed_metric - expected_metric)
        if metric_gap > 0.08:
            diagnostics["P_PHASE_METRIC"].mismatch(
                expected=f"phase_metric={expected_metric:.6g}",
                observed=f"phase_metric={observed_metric:.6g}",
                time=t,
                gap=metric_gap,
            )

        diagnostics["P_QUADRANT_CODE"].checked += 1
        observed_quadrant = (
            int(_v4_topup_logic_high(row, "quadrant_1")),
            int(_v4_topup_logic_high(row, "quadrant_0")),
        )
        expected_quadrant = (int(expected_q1), int(expected_q0))
        if observed_quadrant != expected_quadrant:
            diagnostics["P_QUADRANT_CODE"].mismatch(
                expected=f"quadrant_1/0={expected_quadrant[0]}/{expected_quadrant[1]}",
                observed=f"quadrant_1/0={observed_quadrant[0]}/{observed_quadrant[1]}",
                time=t,
                gap=float(sum(a != b for a, b in zip(observed_quadrant, expected_quadrant))),
            )

    if clk_values and max(clk_values) > 0.65 and min(clk_values) < 0.20:
        clk_activity = True
    diagnostics["P_PHASE_METRIC"].checked = max(1, diagnostics["P_PHASE_METRIC"].checked)
    diagnostics["P_QUADRANT_CODE"].checked = max(1, diagnostics["P_QUADRANT_CODE"].checked)
    diagnostics["P_CLOCK_ACTIVITY"].checked = 1
    coverage_ok = checked >= 12 and code_low and code_high and clk_activity
    if not coverage_ok:
        diagnostics["P_CLOCK_ACTIVITY"].mismatch(
            expected="checked>=12 code_low=true code_high=true clk_activity=true",
            observed=(
                f"checked={checked} code_low={code_low} code_high={code_high} "
                f"clk_activity={clk_activity}"
            ),
            time=float(rows[-1]["time"]),
            gap=float(max(0, 12 - checked) + int(not code_low) + int(not code_high) + int(not clk_activity)),
        )
    ok = all(item.checked > 0 and item.mismatch_count == 0 for item in diagnostics.values())
    return ok, " ; ".join(item.render() for item in diagnostics.values())


CHECKER_ID = "v4_358_quadrature_phase_interpolator"
CHECKER: Checker = check_v4_917_quadrature_phase_interpolator
