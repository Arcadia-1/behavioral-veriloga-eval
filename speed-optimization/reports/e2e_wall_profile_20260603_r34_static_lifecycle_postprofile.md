# Same-Server EVAS/Spectre Speed

Date: 2026-06-03
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host and the artifact emits checker/waveform Spectre-equivalence gates. Paper-facing speed claims should use only equivalence-gated rows and still need repeated cold/warm runs.

## Scope

- Host: `BucketsrandeMacBook-Air.local`
- Selected rows: 2
- Jobs: 1
- EVAS modes: `profile_fast_skip_source_error_control`
- Spectre modes: ``
- Output root: `results/e2e-wall-profile-20260603-r34-static-lifecycle-postprofile`

## Mode Summary

| Backend | Mode | Runs | Sim OK | Behavior PASS | Behavior non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_skip_source_error_control | 2 | 2 | 2 | 0 | 1.655 | 0.828 |

## Checker Policy Summary

Behavior checkers are shared by EVAS and Spectre through the same checker id. `streaming_validated` means the checker uses a parity-validated streaming implementation; `row_based` means the legacy row-list implementation was used.

| Backend | Mode | Checker implementation | Rows |
| --- | --- | --- | ---: |
| evas | profile_fast_skip_source_error_control | `streaming_validated` | 2 |

## Spectre-Equivalence Gate Summary

These gates check whether EVAS preserves task behavior and stays within accepted Spectre-equivalent waveform tolerance. They are not a higher-than-Spectre precision target.

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| profile_fast_skip_source_error_control | 2 | 0 | 0 | 2 | 0 |

## Per-Row Spectre-Equivalence Gates

| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |

## E2E Wall-Time Speedups

The primary `wall_time_s` now uses the same evaluator E2E boundary for both EVAS and Spectre: fixture materialization/staging, simulator subprocess, conversion/parsing, checker, and validation. Use `simulator_subprocess_wall_s` or `timing_split` for simulator-only analysis.

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |

## Timing Split Totals

These totals explain what is inside the unified E2E wall time. EVAS `run_case_*` fields come from `simulate_evas.run_case`; Spectre fields come from the direct Spectre runner.

| Backend | Mode | Field | Total s | Mean s |
| --- | --- | --- | ---: | ---: |
| evas | profile_fast_skip_source_error_control | `evaluator_e2e_wall_s` | 1.655453 | 0.827727 |
| evas | profile_fast_skip_source_error_control | `fixture_materialize_s` | 0.021733 | 0.010867 |
| evas | profile_fast_skip_source_error_control | `run_case_behavior_checker_s` | 0.036115 | 0.018057 |
| evas | profile_fast_skip_source_error_control | `run_case_copy_inputs_s` | 0.003657 | 0.001828 |
| evas | profile_fast_skip_source_error_control | `run_case_evas_subprocess_wall_s` | 1.584966 | 0.792483 |
| evas | profile_fast_skip_source_error_control | `run_case_metric_cleanup_s` | 0.000047 | 0.000023 |
| evas | profile_fast_skip_source_error_control | `run_case_outer_wall_s` | 1.633488 | 0.816744 |
| evas | profile_fast_skip_source_error_control | `run_case_output_setup_s` | 0.002110 | 0.001055 |
| evas | profile_fast_skip_source_error_control | `run_case_preflight_s` | 0.001401 | 0.000700 |
| evas | profile_fast_skip_source_error_control | `run_case_run_case_wall_s` | 1.633401 | 0.816700 |
| evas | profile_fast_skip_source_error_control | `run_case_side_output_validation_s` | 0.000013 | 0.000007 |
| evas | profile_fast_skip_source_error_control | `run_case_temp_cleanup_s` | 0.001766 | 0.000883 |
| evas | profile_fast_skip_source_error_control | `run_case_tempdir_create_s` | 0.001064 | 0.000532 |

## Spectre-Equivalence-Gated Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |

## Interpretation Guardrails

- Speedups use `simulation_ok`, so rows without a behavior checker can still contribute timing if the simulator produced waveforms.
- Equivalence-gated speedups require candidate behavior pass, strict-EVAS parity, and parity to every selected Spectre mode.
- `spectre/ax_speed` is the main fast Spectre speed baseline; `spectre/ax` remains a legacy alias for the same command-line preset.
- `spectre/ax_normalized` keeps `+preset=ax +mt` but rewrites the staged testbench to the shared precision settings before launch.
- `spectre/reference_strict_primary` uses the same staged `tran`/`simulatorOptions` settings without runner-added AX preset.
- `spectre/classic` is the stricter non-X reference path; AX/classic waveform differences are expected and should anchor EVAS tolerance rather than imply a single exact waveform truth.
- The waveform gate is an acceptance tolerance for Spectre-equivalent behavioral output, not a requirement that EVAS exceed Spectre precision.
- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.
- A `BLOCKED` gate is not evidence of wrong behavior; it means the checker or reference evidence is incomplete.
