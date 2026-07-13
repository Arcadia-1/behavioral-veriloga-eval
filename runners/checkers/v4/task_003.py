"""Task-specific checker for canonical v4 DUT 003."""
from __future__ import annotations

from checkers.api import Checker
def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

def _v4_edge_times(
    rows: list[dict[str, float]], signal: str, *, rising: bool, threshold: float = 0.45
) -> list[float]:
    times: list[float] = []
    for previous, current in zip(rows, rows[1:]):
        before = previous[signal]
        after = current[signal]
        if rising and before < threshold <= after:
            times.append(current["time"])
        elif not rising and before > threshold >= after:
            times.append(current["time"])
    return times

def check_v4_pipeline_stage(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vdd", "vss", "vref", "phi1", "phi2", "vin", "vres", "d1", "d0"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)

    phi1_edges = _v4_edge_times(rows, "phi1", rising=True)
    phi2_edges = _v4_edge_times(rows, "phi2", rising=True)
    mismatches: list[str] = []
    regions = {"upper": 0, "middle": 0, "lower": 0}
    paired_samples = 0
    sample_hold_cases = 0
    clamp_cases = 0
    max_residue_error = 0.0
    for phi2_time in phi2_edges:
        previous_phi1 = [time_s for time_s in phi1_edges if time_s < phi2_time]
        if not previous_phi1:
            continue
        phi1_time = previous_phi1[-1]
        vin_sampled = sample_signal_at(rows, "vin", phi1_time + 0.25e-9)
        vin_live = sample_signal_at(rows, "vin", phi2_time)
        vdd = sample_signal_at(rows, "vdd", phi2_time)
        vss = sample_signal_at(rows, "vss", phi2_time)
        vref = sample_signal_at(rows, "vref", phi2_time)
        vres = sample_signal_at(rows, "vres", phi2_time + 0.90e-9)
        d1 = sample_signal_at(rows, "d1", phi2_time + 0.90e-9)
        d0 = sample_signal_at(rows, "d0", phi2_time + 0.90e-9)
        values = (vin_sampled, vin_live, vdd, vss, vref, vres, d1, d0)
        if any(value is None for value in values):
            mismatches.append(f"missing_sample@{phi2_time * 1e9:.3f}ns")
            continue
        assert all(value is not None for value in values)
        paired_samples += 1
        if abs(vin_sampled - vin_live) > 0.05:
            sample_hold_cases += 1
        if vin_sampled < vss - 0.02 or vin_sampled > vdd + 0.02:
            clamp_cases += 1

        vcm = vdd / 2.0
        vin_rel = vin_sampled - vcm
        if vin_rel > vref / 4.0:
            region = "upper"
            expected_d1, expected_d0 = vdd, vss
            expected_vres = vcm + 2.0 * vin_rel - vref / 2.0
        elif vin_rel < -vref / 4.0:
            region = "lower"
            expected_d1, expected_d0 = vss, vss
            expected_vres = vcm + 2.0 * vin_rel + vref / 2.0
        else:
            region = "middle"
            expected_d1, expected_d0 = vss, vdd
            expected_vres = vcm + 2.0 * vin_rel
        regions[region] += 1
        expected_vres = min(vdd, max(vss, expected_vres))
        residue_error = abs(vres - expected_vres)
        max_residue_error = max(max_residue_error, residue_error)
        decision_error = max(abs(d1 - expected_d1), abs(d0 - expected_d0))
        bounded = vss - 0.02 <= vres <= vdd + 0.02
        if residue_error > 0.04 or decision_error > 0.09 or not bounded:
            mismatches.append(
                f"phi2@{phi2_time * 1e9:.3f}ns_region={region}_vin_sampled={vin_sampled:.3f}_"
                f"vin_live={vin_live:.3f}_vres={vres:.3f}/{expected_vres:.3f}_"
                f"d={d1:.3f},{d0:.3f}/{expected_d1:.3f},{expected_d0:.3f}"
            )

    coverage_ok = (
        paired_samples >= 4
        and sample_hold_cases >= 2
        and clamp_cases >= 1
        and all(count > 0 for count in regions.values())
    )
    ok = coverage_ok and not mismatches
    return ok, (
        f"paired_samples={paired_samples} sampled_vs_live_cases={sample_hold_cases} "
        f"clamp_cases={clamp_cases} regions=upper:{regions['upper']},middle:{regions['middle']},lower:{regions['lower']} "
        f"mismatches={len(mismatches)} max_residue_error={max_residue_error:.4f}"
        + (" mismatch_detail=" + ";".join(mismatches[:5]) if mismatches else "")
    )

CHECKER_ID = "v4_003_pipeline_adc_stage"
CHECKER: Checker = check_v4_pipeline_stage
