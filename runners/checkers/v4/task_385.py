"""Task-specific checker for canonical v4 DUT 385."""
from __future__ import annotations

from checkers.api import Checker
from dataclasses import dataclass

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

def check_v4_385_switched_cap_phase_sequencer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required={"time","clk","rst","enable","phi1","phi2","phi3","phi4","sample_cmd","hold_cmd","phase_code_1","phase_code_0","valid"}
    missing=_missing(rows,required)
    if missing:
        return _missing_result("v4_385_switched_cap_phase_sequencer",missing)
    clear=PropertyResult("P_RESET_DISABLE_CLEAR")
    sequence=PropertyResult("P_ONE_HOT_SEQUENCE")
    commands=PropertyResult("P_COMMAND_MAPPING")
    code_result=PropertyResult("P_PHASE_CODE")
    valid_result=PropertyResult("P_VALID_AFTER_SEQUENCE")
    samples=_clock_samples(rows,"clk")
    previous_phase=None
    enabled_edges=0
    previous_enabled=False
    for row in samples:
        t=_value(row,"time")
        enabled=_high(row,"enable") and not _high(row,"rst")
        phase_bits=[_logic(_value(row,f"phi{i}")) for i in range(1,5)]
        if not enabled:
            outputs=phase_bits+[_logic(_value(row,n)) for n in ("sample_cmd","hold_cmd","phase_code_1","phase_code_0","valid")]
            # Disable/reset is consumed on a rising edge by the public state
            # machine.  The first sampled-low control point can follow an edge
            # that still saw the previous high control level.
            if (not previous_enabled) and any(outputs):
                clear.mismatch(t,expected="all_outputs_low",observed=f"bits={outputs}",gap=sum(outputs))
            previous_phase=None; enabled_edges=0
            previous_enabled=False
            continue
        enabled_edges+=1
        if sum(phase_bits)!=1:
            sequence.mismatch(t,expected="one_hot_phase",observed=f"phases={phase_bits}",gap=abs(1-sum(phase_bits)))
            active=None
        else:
            active=phase_bits.index(1)
            if previous_phase is not None and active!=(previous_phase+1)%4:
                sequence.mismatch(t,expected=f"phase={(previous_phase+1)%4}",observed=f"phase={active}",gap=1)
            previous_phase=active
        expected_sample=int(bool(phase_bits[0] or phase_bits[1])); expected_hold=int(bool(phase_bits[2] or phase_bits[3]))
        observed_sample=_logic(_value(row,"sample_cmd")); observed_hold=_logic(_value(row,"hold_cmd"))
        if (observed_sample,observed_hold)!=(expected_sample,expected_hold):
            commands.mismatch(t,expected=f"sample={expected_sample},hold={expected_hold}",observed=f"sample={observed_sample},hold={observed_hold}",gap=1)
        observed_code=2*_logic(_value(row,"phase_code_1"))+_logic(_value(row,"phase_code_0"))
        if active is not None and observed_code!=active:
            code_result.mismatch(t,expected=f"phase_code={active}",observed=f"phase_code={observed_code}",gap=abs(observed_code-active))
        observed_valid=_high(row,"valid")
        expected_valid=enabled_edges>=4
        if observed_valid!=expected_valid:
            valid_result.mismatch(t,expected=f"valid={int(expected_valid)},enabled_edges={enabled_edges}",observed=f"valid={int(observed_valid)}",gap=1)
        previous_enabled=True
    if len(samples)<8: sequence.mismatch(0.0,expected="at_least_8_clock_samples",observed=f"samples={len(samples)}",gap=8-len(samples))
    return _finish([clear,sequence,commands,code_result,valid_result],allowance={"P_VALID_AFTER_SEQUENCE":2})

CHECKER_ID = "v4_385_switched_cap_phase_sequencer"
CHECKER: Checker = check_v4_385_switched_cap_phase_sequencer
