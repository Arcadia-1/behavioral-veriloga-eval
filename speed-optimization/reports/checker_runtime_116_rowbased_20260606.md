# EVAS/Spectre Speed

Date: 2026-06-06
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host and the artifact emits checker/waveform Spectre-equivalence gates. Paper-facing speed claims should use only equivalence-gated rows and still need repeated cold/warm runs.

## Scope

- Host: `BucketsrandeMacBook-Air.local`
- Spectre backend: `local`
- SUI host: `-`
- SUI work root: `-`
- Cadence cshrc: `-`
- Selected rows: 10
- Jobs: 1
- EVAS modes: `profile_fast_evas2`
- Spectre modes: ``
- Output root: `results/checker-runtime-116-rowbased`

## EVAS Mode Specs

| Mode | Phase | Default-off | Simulator options |
| --- | --- | --- | --- |
| `profile_fast_evas2` | `EVAS2` | `True` | `evas_profile=fast evas_skip_source_error_control=yes evas_engine=evas2` |

## Mode Summary

| Backend | Mode | Runs | Sim OK | Behavior PASS | Behavior non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_evas2 | 10 | 10 | 10 | 0 | 16.388 | 1.639 |

## Checker Policy Summary

Behavior checkers are shared by EVAS and Spectre through the same checker id. `streaming_validated` means the checker uses a parity-validated streaming implementation; `row_based` means the legacy row-list implementation was used.

| Backend | Mode | Checker implementation | Rows |
| --- | --- | --- | ---: |
| evas | profile_fast_evas2 | `row_based_streaming_disabled` | 10 |

## Spectre-Equivalence Gate Summary

These gates check whether EVAS preserves task behavior and stays within accepted Spectre-equivalent waveform tolerance. They are not a higher-than-Spectre precision target.

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| profile_fast_evas2 | 10 | 0 | 0 | 10 | 0 |

## Per-Row Spectre-Equivalence Gates

| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_precision_rectifier_envelope_detector` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_precision_rectifier_envelope_detector` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_precision_rectifier_envelope_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_programmable_stimulus_sequencer` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |

## E2E Wall-Time Speedups

The primary `wall_time_s` now uses the same evaluator E2E boundary for both EVAS and Spectre: fixture materialization/staging, simulator subprocess, conversion/parsing, checker, and validation. Use `simulator_subprocess_wall_s` or `timing_split` for simulator-only analysis.

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |

## Timing Split Totals

These totals explain what is inside the unified E2E wall time. EVAS `run_case_*` fields come from `simulate_evas.run_case`; Spectre fields come from the direct Spectre runner.

| Backend | Mode | Field | Total s | Mean s |
| --- | --- | --- | ---: | ---: |
| evas | profile_fast_evas2 | `evaluator_e2e_wall_s` | 16.387978 | 1.638798 |
| evas | profile_fast_evas2 | `fixture_materialize_s` | 0.114472 | 0.011447 |
| evas | profile_fast_evas2 | `run_case_behavior_checker_s` | 11.618031 | 1.161803 |
| evas | profile_fast_evas2 | `run_case_copy_inputs_s` | 0.017382 | 0.001738 |
| evas | profile_fast_evas2 | `run_case_evas_reported_total_elapsed_s` | 0.500000 | 0.050000 |
| evas | profile_fast_evas2 | `run_case_evas_reported_tran_elapsed_s` | 0.257900 | 0.025790 |
| evas | profile_fast_evas2 | `run_case_evas_runner_csv_write_s` | 0.136919 | 0.013692 |
| evas | profile_fast_evas2 | `run_case_evas_runner_derive_bus_signals_s` | 0.001569 | 0.000157 |
| evas | profile_fast_evas2 | `run_case_evas_subprocess_unattributed_s` | 4.078608 | 0.407861 |
| evas | profile_fast_evas2 | `run_case_evas_subprocess_wall_s` | 4.578608 | 0.457861 |
| evas | profile_fast_evas2 | `run_case_metric_cleanup_s` | 0.000026 | 0.000003 |
| evas | profile_fast_evas2 | `run_case_outer_wall_s` | 16.272494 | 1.627249 |
| evas | profile_fast_evas2 | `run_case_output_setup_s` | 0.010242 | 0.001024 |
| evas | profile_fast_evas2 | `run_case_preflight_s` | 0.005397 | 0.000540 |
| evas | profile_fast_evas2 | `run_case_required_trace_signal_count` | 44.000000 | 4.400000 |
| evas | profile_fast_evas2 | `run_case_run_case_wall_s` | 16.272247 | 1.627225 |
| evas | profile_fast_evas2 | `run_case_side_output_validation_s` | 0.000051 | 0.000005 |
| evas | profile_fast_evas2 | `run_case_temp_cleanup_s` | 0.012042 | 0.001204 |
| evas | profile_fast_evas2 | `run_case_tempdir_create_s` | 0.004615 | 0.000461 |

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
