"""Task-specific checker for canonical v4 DUT 378."""
from __future__ import annotations

from ..api import Checker
from dataclasses import dataclass

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

def _clip(value: float, lo: float = VSS, hi: float = VDD) -> float:
    return min(max(value, lo), hi)

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

def check_v4_378_current_limited_regulator_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required={"time","vin","load_demand","enable","rst","vout","limit_metric","regulation_ok"}
    missing=_missing(rows,required)
    if missing:
        return _missing_result("v4_378_current_limited_regulator_macro",missing)
    clear=PropertyResult("P_RESET_DISABLE_CLEAR")
    normal=PropertyResult("P_NORMAL_REGULATION")
    dropout=PropertyResult("P_DROPOUT_CLAMP")
    limiting=PropertyResult("P_CURRENT_LIMITING")
    flag=PropertyResult("P_REGULATION_FLAG")
    # Evaluate a bounded, approximately 1 ns-spaced trace subset.
    next_t=0.0
    regimes=set()
    for row in rows:
        t=_value(row,"time")
        if t+1e-15<next_t: continue
        next_t=t+1e-9
        enabled=_high(row,"enable") and not _high(row,"rst")
        vout=_value(row,"vout"); metric=_value(row,"limit_metric"); ok=_high(row,"regulation_ok")
        if not enabled:
            gap=max(abs(vout),abs(metric),abs(_value(row,"regulation_ok")))
            if gap>0.025: clear.mismatch(t,expected="all_outputs_low",observed=f"vout={vout:.6g},metric={metric:.6g},ok={int(ok)}",gap=gap)
            continue
        vin=_value(row,"vin"); demand=_value(row,"load_demand")
        overload=max(0.0,demand-0.65); headroom=vin-0.08
        expected=_clip(min(0.75-overload,headroom))
        expected_ok=overload<=1e-9 and headroom>=0.75
        if overload>1e-6: regimes.add('limit')
        elif headroom<0.75: regimes.add('dropout')
        else: regimes.add('normal')
        if abs(metric-overload)>0.018:
            limiting.mismatch(t,expected=f"limit_metric={overload:.6g}",observed=f"limit_metric={metric:.6g}",gap=metric-overload)
        if abs(vout-expected)>0.025:
            target=limiting if overload>1e-6 else (dropout if headroom<0.75 else normal)
            target.mismatch(t,expected=f"vout={expected:.6g}",observed=f"vout={vout:.6g}",gap=vout-expected)
        if ok!=expected_ok:
            flag.mismatch(t,expected=f"regulation_ok={int(expected_ok)}",observed=f"regulation_ok={int(ok)}",gap=1)
    for regime,result in [('normal',normal),('dropout',dropout),('limit',limiting)]:
        if regime not in regimes: result.mismatch(0.0,expected=f"stimulus_activates_{regime}",observed=f"regimes={sorted(regimes)}",gap=1)
    return _finish([clear,normal,dropout,limiting,flag],allowance={"P_RESET_DISABLE_CLEAR":2})

CHECKER_ID = "v4_378_current_limited_regulator_macro"
CHECKER: Checker = check_v4_378_current_limited_regulator_macro
