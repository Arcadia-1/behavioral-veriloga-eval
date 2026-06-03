# Same-Server EVAS/Spectre Speed

Date: 2026-06-03
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host and the artifact emits checker/waveform Spectre-equivalence gates. Paper-facing speed claims should use only equivalence-gated rows and still need repeated cold/warm runs.

## Scope

- Host: `BucketsrandeMacBook-Air.local`
- Selected rows: 10
- Jobs: 1
- EVAS modes: `profile_fast_skip_source_error_control, profile_fast_static_branch`
- Spectre modes: ``
- Output root: `results/e2e-wall-profile-20260603-r37-static-branch-top10-ab`

## EVAS Mode Specs

| Mode | Phase | Default-off | Simulator options |
| --- | --- | --- | --- |
| `profile_fast_skip_source_error_control` | `P3` | `True` | `evas_profile=fast evas_skip_source_error_control=yes` |
| `profile_fast_static_branch` | `P4` | `True` | `evas_profile=fast evas_skip_source_error_control=yes evas_static_branch_fastpath=yes` |

## Mode Summary

| Backend | Mode | Runs | Sim OK | Behavior PASS | Behavior non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_skip_source_error_control | 10 | 10 | 10 | 0 | 14.253 | 1.425 |
| evas | profile_fast_static_branch | 10 | 10 | 10 | 0 | 14.126 | 1.413 |

## Checker Policy Summary

Behavior checkers are shared by EVAS and Spectre through the same checker id. `streaming_validated` means the checker uses a parity-validated streaming implementation; `row_based` means the legacy row-list implementation was used.

| Backend | Mode | Checker implementation | Rows |
| --- | --- | --- | ---: |
| evas | profile_fast_skip_source_error_control | `row_based` | 2 |
| evas | profile_fast_skip_source_error_control | `streaming_validated` | 8 |
| evas | profile_fast_static_branch | `row_based` | 2 |
| evas | profile_fast_static_branch | `streaming_validated` | 8 |

## Spectre-Equivalence Gate Summary

These gates check whether EVAS preserves task behavior and stays within accepted Spectre-equivalent waveform tolerance. They are not a higher-than-Spectre precision target.

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| profile_fast_skip_source_error_control | 10 | 0 | 0 | 10 | 0 |
| profile_fast_static_branch | 10 | 0 | 0 | 10 | 0 |

## Per-Row Spectre-Equivalence Gates

| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `profile_fast_static_branch` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `profile_fast_static_branch` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_static_branch` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_fast_static_branch` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `profile_fast_static_branch` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `profile_fast_static_branch` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `profile_fast_static_branch` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast_static_branch` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `profile_fast_static_branch` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `profile_fast_static_branch` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |

## E2E Wall-Time Speedups

The primary `wall_time_s` now uses the same evaluator E2E boundary for both EVAS and Spectre: fixture materialization/staging, simulator subprocess, conversion/parsing, checker, and validation. Use `simulator_subprocess_wall_s` or `timing_split` for simulator-only analysis.

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |

## Timing Split Totals

These totals explain what is inside the unified E2E wall time. EVAS `run_case_*` fields come from `simulate_evas.run_case`; Spectre fields come from the direct Spectre runner.

| Backend | Mode | Field | Total s | Mean s |
| --- | --- | --- | ---: | ---: |
| evas | profile_fast_skip_source_error_control | `evaluator_e2e_wall_s` | 14.252866 | 1.425287 |
| evas | profile_fast_skip_source_error_control | `fixture_materialize_s` | 0.101934 | 0.010193 |
| evas | profile_fast_skip_source_error_control | `run_case_behavior_checker_s` | 3.628957 | 0.362896 |
| evas | profile_fast_skip_source_error_control | `run_case_copy_inputs_s` | 0.020829 | 0.002083 |
| evas | profile_fast_skip_source_error_control | `run_case_evas_subprocess_wall_s` | 10.460526 | 1.046053 |
| evas | profile_fast_skip_source_error_control | `run_case_metric_cleanup_s` | 0.000028 | 0.000003 |
| evas | profile_fast_skip_source_error_control | `run_case_outer_wall_s` | 14.149921 | 1.414992 |
| evas | profile_fast_skip_source_error_control | `run_case_output_setup_s` | 0.009719 | 0.000972 |
| evas | profile_fast_skip_source_error_control | `run_case_preflight_s` | 0.007895 | 0.000790 |
| evas | profile_fast_skip_source_error_control | `run_case_run_case_wall_s` | 14.149573 | 1.414957 |
| evas | profile_fast_skip_source_error_control | `run_case_side_output_validation_s` | 0.000051 | 0.000005 |
| evas | profile_fast_skip_source_error_control | `run_case_temp_cleanup_s` | 0.009444 | 0.000944 |
| evas | profile_fast_skip_source_error_control | `run_case_tempdir_create_s` | 0.003498 | 0.000350 |
| evas | profile_fast_static_branch | `evaluator_e2e_wall_s` | 14.126473 | 1.412647 |
| evas | profile_fast_static_branch | `fixture_materialize_s` | 0.070859 | 0.007086 |
| evas | profile_fast_static_branch | `run_case_behavior_checker_s` | 3.660903 | 0.366090 |
| evas | profile_fast_static_branch | `run_case_copy_inputs_s` | 0.018365 | 0.001837 |
| evas | profile_fast_static_branch | `run_case_evas_subprocess_wall_s` | 10.347043 | 1.034704 |
| evas | profile_fast_static_branch | `run_case_metric_cleanup_s` | 0.000027 | 0.000003 |
| evas | profile_fast_static_branch | `run_case_outer_wall_s` | 14.054882 | 1.405488 |
| evas | profile_fast_static_branch | `run_case_output_setup_s` | 0.003222 | 0.000322 |
| evas | profile_fast_static_branch | `run_case_preflight_s` | 0.005866 | 0.000587 |
| evas | profile_fast_static_branch | `run_case_run_case_wall_s` | 14.054556 | 1.405456 |
| evas | profile_fast_static_branch | `run_case_side_output_validation_s` | 0.000061 | 0.000006 |
| evas | profile_fast_static_branch | `run_case_temp_cleanup_s` | 0.009151 | 0.000915 |
| evas | profile_fast_static_branch | `run_case_tempdir_create_s` | 0.002449 | 0.000245 |

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
