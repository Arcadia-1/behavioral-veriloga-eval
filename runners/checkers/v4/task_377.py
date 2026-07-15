"""Task-specific checker for canonical v4 DUT 377."""
from __future__ import annotations

from ..api import Checker
from dataclasses import dataclass

VCM = 0.45
VDD = 0.9
VSS = 0.0
VTH = 0.45

@dataclass
class PropertyResult:
    property_id: str
    mismatch_count: int = 0
    first_time: float | None = None
    expected: str = "contract_satisfied"
    observed: str = "contract_satisfied"
    max_gap: float = 0.0

    def mismatch(
        self,
        time_s: float,
        *,
        expected: object,
        observed: object,
        gap: float = 1.0,
    ) -> None:
        self.mismatch_count += 1
        self.max_gap = max(self.max_gap, abs(float(gap)))
        if self.first_time is None:
            self.first_time = float(time_s)
            self.expected = str(expected)
            self.observed = str(observed)

    def diagnostic(self) -> str:
        sample_time = "none" if self.first_time is None else f"{self.first_time:.12g}"
        return (
            f"{self.property_id} mismatch_count={self.mismatch_count} "
            f"expected={self.expected} observed={self.observed} "
            f"sample_time={sample_time} metric_gap={self.max_gap:.6g}"
        )

def _missing(rows: list[dict[str, float]], required: Iterable[str]) -> list[str]:
    if not rows:
        return sorted(set(required))
    return sorted(set(required) - set(rows[0]))

def _value(row: dict[str, float], name: str) -> float:
    return float(row[name])

def _high(row: dict[str, float], name: str, threshold: float = VTH) -> bool:
    return _value(row, name) > threshold

def _logic(value: float, threshold: float = VTH) -> int:
    return int(value > threshold)

def _clip(value: float, lo: float = VSS, hi: float = VDD) -> float:
    return min(max(value, lo), hi)

def _clock_samples(
    rows: list[dict[str, float]], clock: str, *, threshold: float = VTH, settle_s: float = 7e-10
) -> list[dict[str, float]]:
    if len(rows) < 2:
        return []
    rising_times: list[float] = []
    previous = _value(rows[0], clock)
    for row in rows[1:]:
        now = _value(row, clock)
        if previous <= threshold < now:
            rising_times.append(_value(row, "time"))
        previous = now
    samples: list[dict[str, float]] = []
    cursor = 0
    for edge_time in rising_times:
        target = edge_time + settle_s
        while cursor + 1 < len(rows) and _value(rows[cursor], "time") < target:
            cursor += 1
        samples.append(rows[cursor])
    return samples

def _finish(results: list[PropertyResult], *, allowance: dict[str, int] | None = None) -> tuple[bool, str]:
    allowance = allowance or {}
    ok = all(item.mismatch_count <= allowance.get(item.property_id, 0) for item in results)
    return ok, "; ".join(item.diagnostic() for item in results)

def _missing_result(checker_id: str, missing: list[str]) -> tuple[bool, str]:
    return False, (
        f"P_TRACE_CONTRACT mismatch_count={len(missing)} expected=all_required_signals "
        f"observed=missing:{','.join(missing)} sample_time=none metric_gap={len(missing)} "
        f"checker={checker_id}"
    )

def check_v4_377_bidirectional_hybrid_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time","port_a","port_b","clk","rst","trim_2","trim_1","trim_0","sum_out","diff_out","forward_metric","reverse_metric","balance_ok"}
    missing = _missing(rows, required)
    if missing:
        return _missing_result("v4_377_bidirectional_hybrid_macro", missing)
    clear = PropertyResult("P_RESET_CLEAR")
    mapping = PropertyResult("P_SUM_DIFF_MAPPING")
    trim = PropertyResult("P_TRIM_RESPONSE")
    directional = PropertyResult("P_DIRECTIONAL_METRICS")
    balance = PropertyResult("P_BALANCE_QUALIFICATION")
    samples = _clock_samples(rows,"clk")
    streak = 0
    trim_codes: set[int] = set()
    for row in samples:
        t=_value(row,"time")
        if _high(row,"rst"):
            vals=[abs(_value(row,"sum_out")-VCM),abs(_value(row,"diff_out")-VCM),abs(_value(row,"forward_metric")),abs(_value(row,"reverse_metric")),abs(_value(row,"balance_ok"))]
            if max(vals)>0.08:
                clear.mismatch(t,expected="sum=diff=vcm,metrics=flags=0",observed=f"max_gap={max(vals):.6g}",gap=max(vals))
            streak=0
            continue
        code=4*_logic(_value(row,"trim_2"))+2*_logic(_value(row,"trim_1"))+_logic(_value(row,"trim_0"))
        trim_codes.add(code)
        corr=(code-3.0)*0.01
        a=_value(row,"port_a")-VCM; b=_value(row,"port_b")-VCM
        expected_sum=_clip(VCM+0.5*(a+b)-corr)
        expected_diff=_clip(VCM+0.5*(a-b)+corr)
        observed_sum=_value(row,"sum_out"); observed_diff=_value(row,"diff_out")
        sum_gap=observed_sum-expected_sum; diff_gap=observed_diff-expected_diff
        if abs(sum_gap)>0.025 or abs(diff_gap)>0.025:
            mapping.mismatch(t,expected=f"sum={expected_sum:.6g},diff={expected_diff:.6g}",observed=f"sum={observed_sum:.6g},diff={observed_diff:.6g}",gap=max(abs(sum_gap),abs(diff_gap)))
        if code != 3 and abs((observed_diff-observed_sum)-(expected_diff-expected_sum))>0.035:
            trim.mismatch(t,expected=f"trim_code={code},corr={corr:.6g}",observed=f"sum={observed_sum:.6g},diff={observed_diff:.6g}",gap=(observed_diff-observed_sum)-(expected_diff-expected_sum))
        expected_forward=_clip(VCM+0.5*((observed_sum-VCM)+(observed_diff-VCM)))
        expected_reverse=_clip(VCM+0.5*((observed_sum-VCM)-(observed_diff-VCM)))
        forward=_value(row,"forward_metric"); reverse=_value(row,"reverse_metric")
        fgap=forward-expected_forward; rgap=reverse-expected_reverse
        if abs(fgap)>0.04 or abs(rgap)>0.04:
            directional.mismatch(t,expected=f"forward={expected_forward:.6g},reverse={expected_reverse:.6g}",observed=f"forward={forward:.6g},reverse={reverse:.6g}",gap=max(abs(fgap),abs(rgap)))
        mismatch=abs((forward-VCM)-(reverse-VCM))
        streak=streak+1 if mismatch<=0.020+1e-6 else 0
        expected_ok=streak>=2
        observed_ok=_high(row,"balance_ok")
        if observed_ok != expected_ok:
            balance.mismatch(t,expected=f"balance_ok={int(expected_ok)},streak={streak}",observed=f"balance_ok={int(observed_ok)},mismatch={mismatch:.6g}",gap=abs(mismatch-0.02))
    if len(trim_codes)<2:
        trim.mismatch(0.0,expected="at_least_two_trim_codes",observed=f"codes={sorted(trim_codes)}",gap=2-len(trim_codes))
    return _finish([clear,mapping,trim,directional,balance],allowance={"P_DIRECTIONAL_METRICS":1,"P_BALANCE_QUALIFICATION":2})

CHECKER_ID = "v4_377_bidirectional_hybrid_macro"
CHECKER: Checker = check_v4_377_bidirectional_hybrid_macro
