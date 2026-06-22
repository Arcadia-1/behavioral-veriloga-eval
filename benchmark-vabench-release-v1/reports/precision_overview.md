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

- **Solver sampling grid**: Use aligned-grid RMS as a diagnostic metric; do not read it as bit-exact equality.
- **Event time and cross() localization**: Check behavior, event consistency, and edge-window metrics before calling this a mismatch.
- **Edge and discontinuity window**: Effective metrics may discount a bounded localized window; raw metrics stay visible for audit.
- **Interpolation on the common grid**: Treat interpolation error as part of the precision diagnostic, not as the task's functional score.
- **transition() smoothing**: Inspect stable-region behavior and checker metrics when transition edges inflate raw RMS.
- **Task-metric gate**: Report the task metric and include pointwise waveform diagnostics only as explanatory context.

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
