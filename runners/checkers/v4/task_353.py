"""Task-specific checker for canonical v4 DUT 353."""
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


def check_v4_ffe_transmitter_3tap(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "data", "clk", "rst", "pre_1", "pre_0", "post_1", "post_0", "vout", "main_dbg", "pre_dbg", "post_dbg"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, (
            f"P_TRACE checked=1 mismatch_count=1 expected=complete_trace "
            f"observed={missing} sample_time=0 metric_gap=1"
        )

    diagnostics = {
        name: PropertyDiagnostic(name)
        for name in ("P_MAIN_TAP", "P_PRE_TAP", "P_POST_TAP", "P_OUTPUT_SUM", "P_EXCITATION")
    }
    sym0 = 0
    sym1 = 0
    sym2 = 0
    checked = 0
    pre_codes: set[int] = set()
    post_codes: set[int] = set()
    out_values: list[float] = []
    for edge_t in _rising_times(rows, "clk"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        if edge_row["rst"] > 0.45:
            sym0 = sym1 = sym2 = 0
            expected_main = expected_pre = expected_post = expected_out = 0.45
        else:
            sym2 = sym1
            sym1 = sym0
            sym0 = 1 if edge_row["data"] > 0.45 else -1
            pre_code = _v4_code(edge_row, ["pre_0", "pre_1"])
            post_code = _v4_code(edge_row, ["post_0", "post_1"])
            pre_codes.add(pre_code)
            post_codes.add(post_code)
            expected_main = 0.45 + 0.18 * sym0
            expected_pre = 0.45 + 0.04 * pre_code * sym1
            expected_post = 0.45 - 0.04 * post_code * sym2
            expected_out = _v4_clip(0.45 + 0.18 * sym0 + 0.04 * pre_code * sym1 - 0.04 * post_code * sym2)
            out_values.append(expected_out)

        sample = _sample_after(rows, edge_t, 0.8e-9)
        checks = (
            ("P_MAIN_TAP", "main_dbg", expected_main, 0.07),
            ("P_PRE_TAP", "pre_dbg", expected_pre, 0.07),
            ("P_POST_TAP", "post_dbg", expected_post, 0.07),
            ("P_OUTPUT_SUM", "vout", expected_out, 0.08),
        )
        for property_id, signal, expected, tolerance in checks:
            diagnostic = diagnostics[property_id]
            diagnostic.checked += 1
            observed = float(sample[signal])
            if not _v4_close(observed, expected, tolerance):
                diagnostic.mismatch(
                    expected=f"{signal}={expected:.6g}",
                    observed=f"{signal}={observed:.6g}",
                    time=edge_t,
                    gap=abs(observed - expected),
                )
        checked += 1

    out_span = max(out_values, default=0.45) - min(out_values, default=0.45)
    diagnostics["P_EXCITATION"].checked = 1
    coverage_ok = checked >= 10 and len(pre_codes) >= 3 and len(post_codes) >= 3 and out_span > 0.25
    if not coverage_ok:
        diagnostics["P_EXCITATION"].mismatch(
            expected="checked>=10 pre_codes>=3 post_codes>=3 out_span>0.25",
            observed=(
                f"checked={checked} pre_codes={sorted(pre_codes)} "
                f"post_codes={sorted(post_codes)} out_span={out_span:.6g}"
            ),
            time=float(rows[-1]["time"]),
            gap=float(max(0, 10 - checked) + max(0, 3 - len(pre_codes)) + max(0, 3 - len(post_codes))),
        )
    ok = all(item.checked > 0 and item.mismatch_count == 0 for item in diagnostics.values())
    return ok, " ; ".join(item.render() for item in diagnostics.values())


CHECKER_ID = "v4_353_ffe_transmitter_3tap"
CHECKER: Checker = check_v4_ffe_transmitter_3tap
