# vaBench Precision Overview

Date: 2026-06-22
Status: `pass`
Precision source: `full300_current_summaries`

## Headline

- Bit-exact claim: `not_asserted`.
- Benchmark management rows: 300.
- Current common precision rows: 300.
- Precision evidence gap rows: 0.
- Surface-row comparisons passed: 900 / 900.
- Needs-review or blocked comparisons: 0.
- Task-metric comparisons: 12.
- Historical four-way reference rows: 271.
- Spectre AX/classic self-consistency: 1036 / 1036 pairs passed.

## Precision vs Spectre Strict

| Surface | Equivalent Rows | Task-Metric Rows | Effective Mean Rel RMS | Effective Worst-Signal Rel RMS | Raw Mean Rel RMS | Raw Worst-Signal Rel RMS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| EVAS Python full-300 | 300 / 300 | 4 | 0.0216667 | 0.147936 | 0.0878333 | 0.147936 |
| EVAS Rust full-300 | 300 / 300 | 4 | 0.0344157 | 0.0870492 | 0.0879235 | 0.132514 |
| Spectre AX full-300 | 300 / 300 | 4 | 0.0191667 | 0.0383333 | 0.0813656 | 0.124398 |

## Task-Metric Rows

| Surface | Row | Metric Delta | Diagnostic Waveform Status | Diagnostic Mean Rel RMS | Diagnostic Worst-Signal Rel RMS |
| --- | --- | ---: | --- | ---: | ---: |
| EVAS Python full-300 | vbr1_l1_gain_estimator:e2e | 2.012e-07 | passed | 6.940e-07 | 2.094e-06 |
| EVAS Python full-300 | vbr1_l1_gain_estimator:tb | 2.012e-07 | passed | 6.940e-07 | 2.094e-06 |
| EVAS Python full-300 | vbr1_l2_gain_extraction_convergence_measurement_flow:e2e | 0.0165043 | needs_review | 0.10203 | 0.154587 |
| EVAS Python full-300 | vbr1_l2_gain_extraction_convergence_measurement_flow:tb | 0.0165043 | needs_review | 0.10203 | 0.154587 |
| EVAS Rust full-300 | vbr1_l1_gain_estimator:e2e | 1.993e-07 | passed | 8.460e-08 | 3.909e-07 |
| EVAS Rust full-300 | vbr1_l1_gain_estimator:tb | 1.993e-07 | passed | 8.460e-08 | 3.909e-07 |
| EVAS Rust full-300 | vbr1_l2_gain_extraction_convergence_measurement_flow:e2e | 0.0171074 | needs_review | 0.102126 | 0.154587 |
| EVAS Rust full-300 | vbr1_l2_gain_extraction_convergence_measurement_flow:tb | 0.0171074 | needs_review | 0.102126 | 0.154587 |
| Spectre AX full-300 | vbr1_l1_gain_estimator:e2e | 7.401e-16 | passed | 1.648e-04 | 4.945e-04 |
| Spectre AX full-300 | vbr1_l1_gain_estimator:tb | 7.401e-16 | passed | 1.648e-04 | 4.945e-04 |
| Spectre AX full-300 | vbr1_l2_gain_extraction_convergence_measurement_flow:e2e | 9.300e-04 | passed | 1.983e-16 | 3.076e-16 |
| Spectre AX full-300 | vbr1_l2_gain_extraction_convergence_measurement_flow:tb | 9.300e-04 | passed | 1.983e-16 | 3.076e-16 |

## Spectre AX/Classic Self-Consistency Anchor

| Metric | Value |
| --- | ---: |
| compared pairs | 1036 |
| passed pairs | 1036 |
| needs review pairs | 0 |
| row mean relative RMS max | 0.0813656 |
| worst-signal relative RMS max | 0.124398 |
| max point absolute voltage | 1 |

## Pointwise Difference Taxonomy

### Solver sampling grid

- Why expected: Adaptive solvers choose output points differently even when the circuit-level trajectory is equivalent.
- What changes: EVAS and Spectre may save different accepted transient steps, so the report compares common signals on a resampled grid.
- Current shortcoming: Our comparison does not prove that EVAS reproduced Spectre's internal step acceptance history; it only compares saved observable signals after alignment.
- Current handling: The released report uses a fixed common sample grid and keeps both effective and raw RMS metrics visible.
- Bug signal: Treat it as a bug if the stable regions disagree, if the checker result changes, or if a row only passes after hiding a broad time interval.
- Useful feedback: Send the row id, both CSV traces, and the first time range where the aligned stable-region values diverge.
- Reporting rule: Use aligned-grid RMS as a diagnostic metric; do not read it as bit-exact equality.

### Event time and cross() localization

- Why expected: The two engines use different event scheduling and breakpoint-localization mechanics.
- What changes: cross() events and timer events can fire at slightly different localized times.
- Current shortcoming: EVAS does not yet claim full Spectre-equivalent ordering for every cross(), timer(), transition(), and simultaneous-event corner case.
- Current handling: Rows with event-heavy behavior are checked by behavior checkers first, then by waveform/event diagnostics on the supported subset.
- Bug signal: Treat it as a bug if an edge is missed, duplicated, ordered differently in a way that changes state, or if EVAS PASS / Spectre FAIL appears.
- Useful feedback: A minimal Verilog-A snippet with the triggering cross()/timer() statements is the most useful report.
- Reporting rule: Check behavior, event consistency, and edge-window metrics before calling this a mismatch.

### Edge and discontinuity window

- Why expected: One-sample edge placement differences can produce large instantaneous voltage deltas while stable regions match.
- What changes: A few samples around fast edges, discontinuities, or digital thresholds can dominate raw pointwise error.
- Current shortcoming: The edge-window rule is a pragmatic acceptance gate. If used carelessly, it could mask a real timing or threshold bug.
- Current handling: Effective metrics may discount only a bounded localized window, and raw metrics remain visible next to the effective metrics.
- Bug signal: Treat it as a bug if the excluded window grows, repeats across many edges, changes a sampled decision, or affects a task metric.
- Useful feedback: Report the signal name, edge time, raw max error, and whether the post-edge state or checker output changed.
- Reporting rule: Effective metrics may discount a bounded localized window; raw metrics stay visible for audit.

### Interpolation on the common grid

- Why expected: Different native output times require interpolation to compare like with like.
- What changes: Saved waveforms are interpolated before RMS comparison.
- Current shortcoming: The current diagnostic uses simple common-grid interpolation; it can overstate or understate error for sparse outputs and very sharp transitions.
- Current handling: We report row-level and worst-signal RMS instead of hiding interpolation-sensitive rows behind a single pass/fail scalar.
- Bug signal: Treat it as a bug if a denser save grid or direct event-time comparison changes the conclusion for a row.
- Useful feedback: A suggested comparison method or a row where interpolation choice flips the result would be directly actionable.
- Reporting rule: Treat interpolation error as part of the precision diagnostic, not as the task's functional score.

### transition() smoothing

- Why expected: EVAS and Spectre do not promise identical internal smoothing schedules.
- What changes: transition() ramps can differ slightly in breakpoint placement and sampled slope.
- Current shortcoming: EVAS transition handling is aligned for the benchmark-supported cases, but it is not a complete public clone of Spectre's internal smoothing implementation.
- Current handling: Stable-region behavior, checker results, and raw/effective waveform metrics are shown together so transition artifacts are not silently ignored.
- Bug signal: Treat it as a bug if transition delay, rise/fall time, or target update semantics change a downstream decision or metric.
- Useful feedback: A small transition() example with expected timing, target updates, and saved waveforms is the best repair input.
- Reporting rule: Inspect stable-region behavior and checker metrics when transition edges inflate raw RMS.

### Noise-like or dithered stimulus

- Why expected: For these rows the design objective is usually an aggregate metric such as gain, lock, count, or convergence, not identical sample-by-sample noise phase.
- What changes: Rows with dither, pseudo-random control, or measurement stimulus can show poor pointwise phase agreement while preserving the extracted circuit metric.
- Current shortcoming: If the checker metric is too broad, it may miss waveform-level differences that a circuit designer would care about.
- Current handling: The page lists task-metric rows separately and keeps diagnostic waveform-only RMS visible for the same rows.
- Bug signal: Treat it as a bug if a different seed, window, or stimulus phase changes pass/fail, or if the aggregate metric hides visible functional drift.
- Useful feedback: Suggestions for stronger metric windows, deterministic seeds, or additional observables are especially useful here.
- Reporting rule: Use deterministic task metrics as the acceptance gate, with pointwise RMS reported as supporting evidence.

### Task-metric gate

- Why expected: Measurement-flow tasks can use dither/noise-like stimulus where pointwise phase is not the design objective.
- What changes: Some rows are accepted by extracted circuit metrics, such as gain or lock/frequency values, not by raw pointwise waveform equality.
- Current shortcoming: A task-metric gate is only as good as the checker behind it. Weak checkers can over-accept; overly tight checkers can reject valid simulator differences.
- Current handling: The report names the task-metric policy, metric delta, diagnostic waveform status, and raw/effective RMS side by side.
- Bug signal: Treat it as a bug if the metric tolerance is undocumented, if the metric is not circuit-meaningful, or if a row passes despite an obviously wrong waveform.
- Useful feedback: Concrete checker improvements are welcome: extra observables, better windows, stricter metric bounds, or task-specific edge cases.
- Reporting rule: Report the task metric and include pointwise waveform diagnostics only as explanatory context.


## Interpretation

- No. Bit-exact equality is not asserted.
- The full 300-row release has common-row precision evidence, and the compared surfaces pass the stated acceptance gates.
- Remaining numerical differences are dominated by solver sampling, event timing, edge/discontinuity windows, interpolation, transition/cross behavior, and task-specific metric extraction.
- Tolerance is not one global decimal precision. It is a set of acceptance gates, with Spectre AX/classic self-consistency used as an anchor for waveform drift that exists inside official Spectre modes.
- The benchmark management denominator and the current precision evidence row count are both 300. The older 271-row artifact is retained only as historical provenance.
- Rows such as gain extraction measurement flows are accepted by extracted circuit metrics; diagnostic pointwise RMS is shown only to prevent misreading waveform drift as a functional failure.

## Source Reports

- `full300_spectre_strict_summary`: `results/vabench-300-dual-reference-rust-checker29-full-20260622/summary.json`
- `full300_spectre_ax_summary`: `results/vabench-300-dual-ax-rust-checker29-full-20260622/summary.json`
- `full300_evas_python_summary`: `results/vabench-300-evas-python-full-checker29-metaraw-20260622/summary.json`
- `full300_evas_rust_summary`: `results/vabench-300-evas-rust-full-checker29-metaraw-20260622/summary.json`
- `spectre_ax_classic_self_consistency`: `speed-optimization/reports/spectre_ax_classic_self_consistency_clean_repeats_20260522.json`
- `historical_fourway_271_reference`: `speed-optimization/reports/full_release_fourway_reference_after_cmp_delay_cross_time_fix_20260608.json`
