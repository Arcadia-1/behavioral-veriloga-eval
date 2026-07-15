"""Task-specific checker for canonical v4 DUT 096."""
from __future__ import annotations

from ..api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def sample_rows_at_or_after_times(
    rows: list[dict[str, float]],
    target_times: list[float],
    *,
    rst_key: str | None = None,
    rst_threshold: float = 0.45,
) -> list[dict[str, float]]:
    """Return rows whose time is the first sample at/after each target time.

    This function is linear in len(rows) + len(target_times). It replaces
    repeated per-target full scans that become O(n^2) on large tran.csv files.
    """
    if not rows or not target_times:
        return []

    sampled: list[dict[str, float]] = []
    row_idx = 0
    n_rows = len(rows)
    for t in target_times:
        while row_idx < n_rows and rows[row_idx]["time"] < t:
            row_idx += 1
        if row_idx >= n_rows:
            break
        row = rows[row_idx]
        if rst_key is None or row.get(rst_key, 0.0) > rst_threshold:
            sampled.append(row)
    return sampled

def _pipeline_adc_chain_stage_code(value: float, *, vrefp: float = 0.9, vrefn: float = 0.0) -> int:
    span = vrefp - vrefn
    if value < vrefn + span * 0.25:
        return 0
    if value < vrefn + span * 0.50:
        return 1
    if value < vrefn + span * 0.75:
        return 2
    return 3

def _pipeline_adc_chain_expected(vin: float, *, vrefp: float = 0.9, vrefn: float = 0.0) -> tuple[int, int, int, float, float]:
    span = vrefp - vrefn
    vin = min(vrefp, max(vrefn, vin))
    s1_code = _pipeline_adc_chain_stage_code(vin, vrefp=vrefp, vrefn=vrefn)
    center1 = vrefn + (s1_code + 0.5) * span / 4.0
    res1 = (vrefp + vrefn) / 2.0 + 4.0 * (vin - center1)
    res1 = min(vrefp, max(vrefn, res1))

    s2_code = _pipeline_adc_chain_stage_code(res1, vrefp=vrefp, vrefn=vrefn)
    center2 = vrefn + (s2_code + 0.5) * span / 4.0
    res2 = (vrefp + vrefn) / 2.0 + 4.0 * (res1 - center2)
    res2 = min(vrefp, max(vrefn, res2))

    final_code = 4 * s1_code + s2_code
    return s1_code, s2_code, final_code, res1, res2

def check_release_pipeline_adc_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """Release L2 pipeline ADC: verify two-stage decisions, residues, and final code."""
    required = {
        "time",
        "vin",
        "clk",
        "res1",
        "res2",
        "s1b1",
        "s1b0",
        "s2b1",
        "s2b0",
        "dout3",
        "dout2",
        "dout1",
        "dout0",
    }
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, f"missing_columns={','.join(missing)}"

    vth = 0.45
    times = [row["time"] for row in rows]
    edge_times = rising_edges([row["clk"] for row in rows], times, threshold=vth)
    sample_rows = sample_rows_at_or_after_times(rows, [edge_t + 0.8e-9 for edge_t in edge_times])
    if len(sample_rows) < 16:
        return False, f"too_few_settled_samples={len(sample_rows)}"

    observed_codes: list[int] = []
    expected_codes: list[int] = []
    stage_bit_mismatches = 0
    final_concat_mismatches = 0
    final_code_mismatches = 0
    residue_mismatches = 0
    bounded_failures = 0
    max_res1_err = 0.0
    max_res2_err = 0.0
    res2_values: list[float] = []

    for row in sample_rows:
        exp_s1, exp_s2, exp_final, exp_res1, exp_res2 = _pipeline_adc_chain_expected(row["vin"])
        got_s1 = ((1 if row["s1b1"] >= vth else 0) << 1) | (1 if row["s1b0"] >= vth else 0)
        got_s2 = ((1 if row["s2b1"] >= vth else 0) << 1) | (1 if row["s2b0"] >= vth else 0)
        got_final = (
            ((1 if row["dout3"] >= vth else 0) << 3)
            | ((1 if row["dout2"] >= vth else 0) << 2)
            | ((1 if row["dout1"] >= vth else 0) << 1)
            | (1 if row["dout0"] >= vth else 0)
        )
        got_concat = 4 * got_s1 + got_s2

        if got_s1 != exp_s1 or got_s2 != exp_s2:
            stage_bit_mismatches += 1
        if got_final != got_concat:
            final_concat_mismatches += 1
        if got_final != exp_final:
            final_code_mismatches += 1

        res1_err = abs(row["res1"] - exp_res1)
        res2_err = abs(row["res2"] - exp_res2)
        max_res1_err = max(max_res1_err, res1_err)
        max_res2_err = max(max_res2_err, res2_err)
        if res1_err > 0.04 or res2_err > 0.04:
            residue_mismatches += 1
        if row["res1"] < -0.02 or row["res1"] > 0.92 or row["res2"] < -0.02 or row["res2"] > 0.92:
            bounded_failures += 1

        observed_codes.append(got_final)
        expected_codes.append(exp_final)
        res2_values.append(row["res2"])

    observed_unique = sorted(set(observed_codes))
    expected_unique = sorted(set(expected_codes))
    reversals = sum(1 for prev, curr in zip(observed_codes, observed_codes[1:]) if curr < prev)
    res2_span = max(res2_values) - min(res2_values) if res2_values else 0.0
    ok = (
        observed_unique == list(range(16))
        and expected_unique == list(range(16))
        and stage_bit_mismatches == 0
        and final_concat_mismatches == 0
        and final_code_mismatches == 0
        and residue_mismatches == 0
        and bounded_failures == 0
        and reversals == 0
        and res2_span > 0.20
    )
    return ok, (
        f"observed_codes={','.join(str(code) for code in observed_unique)} "
        f"expected_codes={','.join(str(code) for code in expected_unique)} "
        f"stage_bit_mismatches={stage_bit_mismatches} "
        f"final_concat_mismatches={final_concat_mismatches} "
        f"final_code_mismatches={final_code_mismatches} "
        f"residue_mismatches={residue_mismatches} "
        f"max_res1_err={max_res1_err:.4f} "
        f"max_res2_err={max_res2_err:.4f} "
        f"res2_span={res2_span:.4f} "
        f"reversals={reversals} "
        f"bounded_failures={bounded_failures}"
    )

CHECKER_ID = "v4_096_pipeline_adc_chain_4b"
CHECKER: Checker = check_release_pipeline_adc_chain
