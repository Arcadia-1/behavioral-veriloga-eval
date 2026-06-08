# vaBench Four-Way Reference Experiment

Date: 2026-06-08
Artifact: `vabench_release_fourway_reference_experiment`

## Scope

- Common rows across all four modes: `271`
- Behavior checker fields refreshed from existing CSVs: `True`
- Behavior refresh policy: refresh stale non-pass source rows from existing CSV checkers only
- Claim boundary: Cross-host Spectre/EVAS wall ratios are diagnostic unless the raw source artifact records a controlled same-host protocol. Use subprocess/E2E labels literally; subprocess wall is not pure simulator kernel time.
- Source raw JSONs listed below are hash-locked intermediate artifacts and are not committed in this split PR because they are large; use `--source-json` with archived raw artifacts to regenerate.
- Reuse rule: cite this derived JSON/Markdown together with its source raw JSONs; rerun only when EVAS code, benchmark rows, checker policy, host class, or Spectre settings change.
- `Reported tran` is simulator-reported diagnostic time and is not added into E2E percentages; for Spectre it can exceed subprocess wall because of tool reporting semantics.

## Frozen Claim Contract

- Experiment ID: `vabench-release-fourway-rust-evas2-spectreax-strict-20260606`
- Frozen on: `2026-06-08`
- Frozen report: `speed-optimization/reports/full_release_fourway_reference_after_cmp_delay_cross_time_fix_20260608.json`
- Row-set size: `271`
- Row-set SHA256: `5b2863c95ff4444869abb5bf1eef0b499285b4915a3a729eedce60594813ab08`
- Reuse rule: Use this report as the stable four-way reference until one of the rerun triggers fires; do not replace the conclusion with ad-hoc smoke numbers.

Allowed wording:
- On this frozen four-way vaBench release slice, Rust EVAS2 is faster than Spectre AX in aggregate E2E and subprocess wall time.
- Rust EVAS2 and Spectre AX both pass the Spectre-strict-referenced behavior/waveform equivalence gate on this slice.

Forbidden wording:
- Rust EVAS2 is more accurate than Spectre AX.
- Rust EVAS2 is faster than Spectre AX on every row.
- This four-way cross-host artifact alone is a final paper-facing same-server speed claim.
- Rust EVAS2 fully covers all Verilog-A language semantics.

Paper-facing boundary: `False` from this artifact alone. This artifact freezes the four-way engineering reference. A final paper-facing Rust-default speed claim still needs the same-slice same-host/approved-bridge protocol to be promoted as the paper speed artifact.

Rerun triggers:
- EVAS simulator code or Rust EVAS2 default/fastpath semantics change.
- Release row set, checker policy, or waveform equivalence policy changes.
- Spectre AX/strict options, host class, bridge route, or runner timing boundary changes.
- Any source artifact hash in this lock no longer matches the frozen source file.

## Source Raw Artifacts

| Source | Results | EVAS modes | Spectre modes | Backend | Host | SHA256 |
| --- | ---: | --- | --- | --- | --- | --- |
| `speed-optimization/reports/full_release_evas_py_rust_after_fixes_20260606.json` | 1084 | `strict_current, profile_fast_skip_source_error_control, profile_fast_rust_55, profile_fast_evas2` | - | `local` | `BucketsrandeMacBook-Air.local` | `631b232dd0d1` |
| `speed-optimization/reports/full_release_evas2_sidefx_persist_20260606.json` | 271 | `profile_fast_evas2` | - | `local` | `BucketsrandeMacBook-Air.local` | `d8772b1fe7fd` |
| `speed-optimization/reports/full_release_spectre_ax_strict_20260606.json` | 542 | - | `ax_speed, reference_strict_primary` | `sui-direct` | `BucketsrandeMacBook-Air.local` | `ec6367f9ff74` |
| `speed-optimization/reports/cmp_delay_cross_time_fix_evas2_allforms_20260608_r2.json` | 4 | `profile_fast_evas2` | - | `local` | `BucketsrandeMacBook-Air.local` | `493f0f0fe320` |

## Speed Overview

| Simulator | Mode | Rows | Sim OK | Behavior PASS | E2E total s | Subprocess total s | Geomean E2E/row s | vs AX E2E | vs AX subprocess |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EVAS1.0 Python strict | `strict_current` | 271 | 271 | 271 | 597.444 | 541.313 | 0.655 | 3.75x | 1.69x |
| EVAS2 Rust | `profile_fast_evas2` | 271 | 271 | 271 | 71.239 | 11.716 | 0.199 | 31.45x | 78.01x |
| Spectre AX | `ax_speed` | 271 | 271 | 271 | 2240.311 | 914.007 | 8.237 | 1.00x | 1.00x |
| Spectre strict | `reference_strict_primary` | 271 | 271 | 271 | 2646.507 | 1281.346 | 9.708 | 0.85x | 0.71x |

## Component Time Breakdown

| Simulator | E2E total | Subprocess | Reported tran | Checker | CSV/PSF | Fixture/staging | Parse/log | Other overhead | Checker % | Subprocess % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EVAS1.0 Python strict | 597.444 | 541.313 | 535.217 | 51.804 | 1.393 | 2.510 | 0.008 | 0.927 | 8.7% | 90.6% |
| EVAS2 Rust | 71.239 | 11.716 | 3.284 | 54.244 | 1.523 | 3.170 | 0.008 | 1.124 | 76.1% | 16.4% |
| Spectre AX | 2240.311 | 914.007 | 2609.282 | 21.153 | 8.885 | 2.542 | 0.253 | 1293.471 | 0.9% | 40.8% |
| Spectre strict | 2646.507 | 1281.346 | 4972.843 | 57.946 | 14.702 | 1.864 | 0.265 | 1290.384 | 2.2% | 48.4% |

## Precision Against Spectre Strict

Rows where Spectre strict itself fails the behavior checker are not treated as usable precision references.

`effective` metrics are the simulator-equivalence metrics after allowed edge-window treatment. `raw` metrics keep the original pointwise waveform difference for diagnosis. `abs saved units` is intentionally not called voltage because some saved columns are measurements such as `delay_ps`.

| Candidate | Reference usable | Candidate PASS | Compared | Equivalent | Needs review | Blocked | Worst abs saved units | Worst effective mean rel RMS | Worst effective signal rel RMS | Worst raw mean rel RMS | Worst raw signal rel RMS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EVAS1.0 Python strict | 271 | 271 | 271 | 271 | 0 | 0 | 1.000000 | 0.015833 | 0.147936 | 0.079693 | 0.147936 |
| EVAS2 Rust | 271 | 271 | 271 | 271 | 0 | 0 | 1.000000 | 0.015833 | 0.031667 | 0.079693 | 0.127719 |
| Spectre AX | 271 | 271 | 271 | 271 | 0 | 0 | 1.000000 | 0.006205 | 0.019167 | 0.072521 | 0.122542 |

## Precision Gate

| Gate | Meaning | Pass condition |
| --- | --- | --- |
| Behavior checker | Circuit-level functional acceptance | Current row checker returns PASS |
| Waveform absolute gate | Low-swing / near-zero guard for voltage-like saved signals | `max_rmse_v <= 0.05` and `max_abs_v <= 0.30` in the waveform comparator |
| Waveform relative gate | Simulator-style relative waveform agreement | effective row mean relative RMS and effective worst-signal relative RMS satisfy `spectre_equivalence_core_v2` |
| Special functional parity | PLL/gain/ADC rows where pointwise waveform is not the right acceptance metric | Task-specific parity helper in `run_gold_dual_suite.py` returns `passed` |

## Rust Runtime Coverage

| Metric | Value |
| --- | ---: |
| Runtime rows | 271 |
| Rust full-model enabled rows | 271 |
| RustSimProgram enabled rows | 269 |
| RustSimProgram rejection rows | 2 |
| Rust full-model fallback rows | 0 |
| Static compile-pass model rows | 357 |
| Static strict RustSimProgram supported rows | 357 |
| `rust_full_model_fastpath_enabled` | 271 |
| `rust_full_model_fastpath_fallbacks_total` | 0 |
| `rust_sim_program_enabled` | 269 |
| `rust_sim_program_rejections` | 2 |
| `rust_sim_program_event_count` | 755 |
| `rust_sim_program_body_stmt_ops` | 7679 |
| `rust_sim_program_body_expr_ops` | 24549 |
| `rust_sim_program_transition_count` | 756 |
| `rust_sim_program_record_count` | 1517 |
| `rust_sim_program_event_fires` | 252776 |
| `rust_sim_program_points` | 347215 |
| `rust_sim_program_side_effects` | 12 |
| `rust_sim_program_lower_elapsed_s` | 0 |
| `rust_sim_program_abi_build_elapsed_s` | 0 |
| `rust_sim_program_time_grid_elapsed_s` | 0 |
| `rust_sim_program_runtime_elapsed_s` | 0 |
| `rust_sim_program_runtime_attempts` | 4 |
| `rust_sim_program_final_capacity` | 55264 |
| `rust_sim_program_record_replay_elapsed_s` | 0 |
| `rust_sim_program_state_sync_elapsed_s` | 0 |
| `rust_sim_program_fastpath_total_elapsed_s` | 0 |

## Top Rust EVAS2 E2E Rows

| Entry | Form | Rust E2E s | Rust subprocess s | Dominant Rust cost | Py strict / Rust | AX / Rust | Strict / Rust | RustSimProgram |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `vbr1_l1_precision_rectifier_envelope_detector` | `dut` | 1.368 | 0.059 | `checker_s` | 4.37x | 6.78x | 7.67x | 1 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `bugfix` | 1.266 | 0.061 | `checker_s` | 4.13x | 6.99x | 7.71x | 1 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `tb` | 1.250 | 0.058 | `checker_s` | 4.86x | 6.90x | 7.72x | 1 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | 1.191 | 0.068 | `checker_s` | 7.17x | 5.98x | 8.59x | 1 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | 0.917 | 0.111 | `checker_s` | 1.66x | 8.17x | 11.14x | 1 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | 0.891 | 0.080 | `checker_s` | 10.52x | 8.05x | 11.49x | 1 |
| `vbr1_l2_programmable_stimulus_sequencer` | `tb` | 0.850 | 0.042 | `checker_s` | 4.59x | 10.50x | 11.90x | 1 |
| `vbr1_l2_measurement_flow` | `e2e` | 0.844 | 0.054 | `checker_s` | 2.19x | 9.91x | 12.19x | 1 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | 0.840 | 0.040 | `checker_s` | 9.54x | 9.54x | 12.22x | 1 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | 0.832 | 0.059 | `checker_s` | 1.96x | 11.33x | 12.21x | 1 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | 0.830 | 0.065 | `checker_s` | 2.50x | 11.63x | 12.97x | 1 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | 0.804 | 0.035 | `checker_s` | 0.98x | 10.56x | 13.07x | 1 |
| `vbr1_l1_window_comparator_detector` | `e2e` | 0.800 | 0.027 | `checker_s` | 6.96x | 8.97x | 12.71x | 1 |
| `vbr1_l1_gain_trim_controller` | `e2e` | 0.796 | 0.038 | `checker_s` | 1.16x | 11.18x | 11.03x | 1 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | 0.792 | 0.032 | `checker_s` | 7.12x | 9.14x | 13.44x | 1 |
| `vbr1_l1_clock_divider` | `dut` | 0.789 | 0.045 | `checker_s` | 5.14x | 9.32x | 12.61x | 1 |
| `vbr1_l1_window_comparator_detector` | `tb` | 0.783 | 0.028 | `checker_s` | 6.96x | 9.78x | 13.68x | 1 |
| `vbr1_l1_window_comparator_detector` | `dut` | 0.781 | 0.029 | `checker_s` | 8.32x | 9.18x | 14.09x | 1 |
| `vbr1_l1_clock_divider` | `bugfix` | 0.761 | 0.055 | `checker_s` | 5.41x | 10.30x | 12.89x | 1 |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `bugfix` | 0.741 | 0.633 | `subprocess_wall_s` | 1.96x | 11.91x | 13.02x | 1 |
