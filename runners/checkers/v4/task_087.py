"""Task-specific checker for canonical v4 DUT 087."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, event_label, pass_note, require_signals


PROPERTY_IDS = [
    "P_RESET_STATE",
    "P_FOUR_BIT_QUANTIZATION",
    "P_PUBLIC_RECONSTRUCTION_TABLE",
    "P_INL_METRIC",
    "P_DNL_INCREASING_STEP",
    "P_DNL_NO_STEP_BASELINE",
]


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

def check_converter_static_linearity_measurement_flow(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "code", "recon", "dnl", "inl"}
    missing = require_signals(rows, required, "P_RESET_STATE")
    if missing:
        return False, missing

    vth = 0.45
    edge_idx = [
        idx
        for idx in range(1, len(rows))
        if rows[idx - 1]["clk"] <= vth < rows[idx]["clk"] and rows[idx]["rst"] <= vth
    ]
    if len(edge_idx) < 12:
        return False, diagnostic(
            "P_FOUR_BIT_QUANTIZATION",
            "invalid_trace",
            expected="at_least_12_post_reset_clock_edges",
            observed=f"edges={len(edge_idx)}",
            event="clk_edges",
        )

    # Sample after the output transition has settled.  EVAS writes denser rows
    # than Spectre around transition breakpoints, so row-index offsets can land
    # in the middle of a transition and compare mixed old/new metric values.
    sample_times = [rows[idx]["time"] + 0.7e-9 for idx in edge_idx]
    samples = sample_rows_at_or_after_times(rows, sample_times)
    if len(samples) < 12:
        return False, diagnostic(
            "P_FOUR_BIT_QUANTIZATION",
            "invalid_trace",
            expected="at_least_12_settled_clock_edge_samples",
            observed=f"samples={len(samples)}",
            event="clk_edges",
        )
    codes = [max(0, min(15, round(r["code"] / 0.06))) for r in samples]
    distinct_codes = sorted(set(codes))
    if len(distinct_codes) < 13 or distinct_codes[0] > 1 or distinct_codes[-1] < 14:
        return False, diagnostic(
            "P_FOUR_BIT_QUANTIZATION",
            "behavior_mismatch",
            expected="codes_cover_at_least_13_levels_from_near_zero_to_near_full_scale",
            observed=f"codes={distinct_codes}",
            event=event_label("clk_edge", 0, rows[edge_idx[0]]["time"]),
        )
    code_drops = sum(1 for prev, cur in zip(codes, codes[1:]) if cur < prev)
    if code_drops:
        return False, diagnostic(
            "P_FOUR_BIT_QUANTIZATION",
            "behavior_mismatch",
            expected="monotonic_codes",
            observed=f"drops={code_drops}",
            event=event_label("clk_edge", 0, rows[edge_idx[0]]["time"]),
        )

    by_code: dict[int, list[dict[str, float]]] = {}
    for code, row in zip(codes, samples):
        by_code.setdefault(code, []).append(row)
    recon_by_code = {
        code: sum(row["recon"] for row in code_rows) / len(code_rows)
        for code, code_rows in by_code.items()
    }
    ordered_codes = sorted(recon_by_code)
    recon_vals = [recon_by_code[code] for code in ordered_codes]
    recon_drops = sum(1 for prev, cur in zip(recon_vals, recon_vals[1:]) if cur < prev - 0.015)
    if recon_drops:
        return False, f"converter_reconstruction_not_monotonic drops={recon_drops}"
    steps = [cur - prev for prev, cur in zip(recon_vals, recon_vals[1:])]
    if len(steps) < 8 or min(steps) < 0.025:
        return False, diagnostic(
            "P_PUBLIC_RECONSTRUCTION_TABLE",
            "behavior_mismatch",
            expected="at_least_8_positive_reconstruction_steps",
            observed=f"steps={steps}",
            event=event_label("clk_edge", 0, rows[edge_idx[0]]["time"]),
        )
    step_spread = max(steps) - min(steps)
    if step_spread < 0.010:
        return False, diagnostic(
            "P_DNL_INCREASING_STEP",
            "behavior_mismatch",
            expected="step_spread>=0.010",
            observed=f"step_spread={step_spread:.4f}",
            event=event_label("clk_edge", 0, rows[edge_idx[0]]["time"]),
        )

    first_edge_time = rows[edge_idx[0]]["time"]
    post = [r for r in rows if r["rst"] <= vth and r["time"] >= first_edge_time]
    dnl_vals = [r["dnl"] for r in post]
    inl_vals = [r["inl"] for r in post]
    if not dnl_vals or not inl_vals:
        return False, diagnostic(
            "P_INL_METRIC",
            "invalid_trace",
            expected="post_reset_metric_rows",
            observed="missing_metric_rows",
            event=event_label("clk_edge", 0, first_edge_time),
        )
    dnl_span = max(dnl_vals) - min(dnl_vals)
    inl_span = max(inl_vals) - min(inl_vals)
    if dnl_span < 0.035 or inl_span < 0.050:
        return False, diagnostic(
            "P_INL_METRIC",
            "behavior_mismatch",
            expected="dnl_span>=0.035_and_inl_span>=0.050",
            observed=f"dnl={dnl_span:.3f},inl={inl_span:.3f}",
            event=event_label("clk_edge", 0, first_edge_time),
        )

    metric_tol = 0.065
    max_inl_err = 0.0
    max_dnl_err = 0.0
    dnl_checks = 0
    prev_code: int | None = None
    prev_recon: float | None = None
    for row, code in zip(samples, codes):
        recon = row["recon"]
        expected_inl = max(0.05, min(0.85, 0.45 + 3.0 * (recon - 0.06 * code)))
        inl_err = abs(row["inl"] - expected_inl)
        max_inl_err = max(max_inl_err, inl_err)

        if prev_code is not None and prev_recon is not None and code > prev_code:
            ideal_step = 0.06 * (code - prev_code)
            expected_dnl = 0.45 + 4.0 * ((recon - prev_recon) - ideal_step)
            dnl_checks += 1
        else:
            expected_dnl = 0.45
        expected_dnl = max(0.05, min(0.85, expected_dnl))
        dnl_err = abs(row["dnl"] - expected_dnl)
        max_dnl_err = max(max_dnl_err, dnl_err)

        prev_code = code
        prev_recon = recon

    if max_inl_err > metric_tol:
        return False, diagnostic(
            "P_INL_METRIC",
            "behavior_mismatch",
            expected=f"max_inl_error<={metric_tol:.3f}",
            observed=f"err={max_inl_err:.3f}",
            event=event_label("clk_edge", 0, first_edge_time),
        )
    if dnl_checks < 8:
        return False, diagnostic(
            "P_DNL_INCREASING_STEP",
            "invalid_trace",
            expected="at_least_8_dnl_step_checks",
            observed=f"checks={dnl_checks}",
            event=event_label("clk_edge", 0, first_edge_time),
        )
    if max_dnl_err > metric_tol:
        return False, diagnostic(
            "P_DNL_INCREASING_STEP",
            "behavior_mismatch",
            expected=f"max_dnl_error<={metric_tol:.3f}",
            observed=f"err={max_dnl_err:.3f}",
            event=event_label("clk_edge", 0, first_edge_time),
        )

    return True, pass_note(
        PROPERTY_IDS,
        "converter_static_linearity_measurement_flow "
        f"codes={len(distinct_codes)} step_spread={step_spread:.4f} "
        f"dnl_span={dnl_span:.3f} inl_span={inl_span:.3f} "
        f"metric_err={max_dnl_err:.3f}/{max_inl_err:.3f}"
    )

CHECKER_ID = "v4_087_converter_static_linearity_measurement"
CHECKER: Checker = check_converter_static_linearity_measurement_flow
