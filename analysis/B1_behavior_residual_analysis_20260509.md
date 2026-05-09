# B1 Behavior-Repair Smoke Residual Analysis

Date: 2026-05-09

## Selection Summary

Selected 10 compile-OK behavior-fail tasks for a behavior-repair controller smoke. The selected set is drawn from S2 Spectre residuals with `FAIL_SIM_CORRECTNESS`; S2 compile failures are excluded. T1 residual behavior failures were inspected, but not selected because the S2 behavior-fail pool already provides broader coverage without mixing generated roots.

Source residual pool: S2 Spectre has 120 total tasks, 29 passes, 81 `FAIL_SIM_CORRECTNESS`, 9 `FAIL_DUT_COMPILE`, and 1 `FAIL_TB_COMPILE`.

## Counts

- Selected tasks: 10
- S2 Spectre behavior failures selected: 10
- Compile failures selected: 0
- By task form: {'bugfix': 2, 'spec-to-va': 6, 'tb-generation': 2}
- By core function: {'calibration/control': 1, 'data conversion/calibration': 1, 'continuous dynamics': 1, 'continuous dynamics/pll': 1, 'data conversion': 1, 'event/timing': 2, 'pointer/selection': 1, 'stateful analog memory': 1, 'threshold/static nonlinear': 1}

## Selected Tasks

| task_id | form | core_function | failure_family | checker/status notes | rationale |
| --- | --- | --- | --- | --- | --- |
| `vbm1_background_calibration_accumulator_bugfix` | bugfix | calibration/control | calibration trajectory / missing accumulation | S2 `FAIL_SIM_CORRECTNESS`; contract_save_pruned=removed:1,inserted:1,signals:4; spectre_strict:preflight_pass; spectre_csv_rows=523 cols=5; first=0.003 mid=0.004 late=0.006 | Small calibration trajectory remains near zero across first/mid/late probes; useful for controller fixes that must add missing state accumulation without changing interfaces. |
| `vbm1_cdac_calibration_dut` | spec-to-va | data conversion/calibration | calibration code/output saturation | S2 `FAIL_SIM_CORRECTNESS`; contract_save_pruned=removed:1,inserted:1,signals:4; spectre_strict:preflight_pass; spectre_csv_rows=585 cols=5; first=0.940 mid=0.930 late=0.940 | CDAC calibration output is stuck high across time probes; stresses data-conversion calibration semantics in a spec-to-VA DUT-only setting. |
| `vbm1_first_order_lowpass_dut` | spec-to-va | continuous dynamics | continuous dynamics mismatch | S2 `FAIL_SIM_CORRECTNESS`; contract_save_pruned=removed:1,inserted:1,signals:2; spectre_strict:preflight_pass; spectre_csv_rows=81396 cols=3; early=0.080 late=0.428 | Large transient waveform with early/late lowpass mismatch; useful for continuous-time dynamics and coefficient/time-constant repair. |
| `vbm1_vco_phase_integrator_dut` | spec-to-va | continuous dynamics/pll | PLL phase integration / edge generation | S2 `FAIL_SIM_CORRECTNESS`; contract_save_pruned=removed:1,inserted:1,signals:3; spectre_strict:preflight_pass; spectre_csv_rows=1815 cols=4; early_edges=26 late_edges=0 phase_span=105627.099 | PLL phase behavior shows pathological phase span and lost late edges; covers event/continuous interaction and phase wrapping behavior. |
| `vbm1_segmented_dac_tb` | tb-generation | data conversion | DAC stimulus/measurement value mismatch | S2 `FAIL_SIM_CORRECTNESS`; contract_save_pruned=removed:1,inserted:1,signals:6; gold_dut_include=segmented_dac.va; spectre_strict:preflight_pass; spectre_csv_rows=327 cols=7; vals=[1.0, 0.4, 0.333, 1.0, 0.667] | Gold DUT with generated testbench yields incorrect DAC sample values; isolates checker-facing stimulus/measurement behavior rather than DUT syntax. |
| `vbm1_edge_detector_dut` | spec-to-va | event/timing | pulse width / edge timing mismatch | S2 `FAIL_SIM_CORRECTNESS`; contract_save_pruned=removed:1,inserted:1,signals:3; spectre_strict:preflight_pass; spectre_csv_rows=424 cols=4; pulse_edges=4 high_frac=0.292 | Pulse edge count is plausible but high fraction is wrong; good for narrow-pulse timing behavior repair after compile success. |
| `vbm1_resettable_counter_divider_dut` | spec-to-va | event/timing | counter divide ratio mismatch | S2 `FAIL_SIM_CORRECTNESS`; contract_save_pruned=removed:3,inserted:1,signals:12; spectre_strict:preflight_pass; spectre_csv_rows=2348 cols=13; ratio=5 in_edges=80 out_edges=40 intervals=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] lock=1 | Counter divider produces too many output edges for ratio=5; exercises sequential timing/counting semantics with rich edge metrics. |
| `vbm1_barrel_pointer_window_bugfix` | bugfix | pointer/selection | pointer/window selection inactive | S2 `FAIL_SIM_CORRECTNESS`; contract_save_pruned=removed:1,inserted:1,signals:6; spectre_strict:preflight_pass; spectre_csv_rows=297 cols=7; count_range=(0, 0) | Selection window count remains zero; compact pointer/selection bugfix case for one-hot/window activation behavior. |
| `vbm1_leaky_hold_dut` | spec-to-va | stateful analog memory | stateful hold/decay mismatch | S2 `FAIL_SIM_CORRECTNESS`; contract_save_pruned=removed:1,inserted:1,signals:3; spectre_strict:preflight_pass; spectre_csv_rows=49281 cols=4; high=0.412 decayed=0.125 rst=0.000 | Hold/decay/reset probes are present but decay level mismatches; covers stateful analog memory with reset and leakage semantics. |
| `vbm1_offset_comparator_tb` | tb-generation | threshold/static nonlinear | threshold decision coverage mismatch | S2 `FAIL_SIM_CORRECTNESS`; spectre_strict:preflight_pass; spectre_csv_rows=1536 cols=5; clock_decisions=3; high_ok=1; low_ok=0 | Comparator testbench has high decision passing but low decision failing; isolates threshold/checker stimulus coverage in a tb-generation task. |

## Tasklist

The runnable smoke tasklist is `behavioral-veriloga-eval/tasklists/B1_behavior_repair_smoke_20260509.txt`.

## Notes

- Every selected task has S2 Spectre `FAIL_SIM_CORRECTNESS`, `spectre_strict:preflight_pass`, and waveform/checker metrics, so the list targets behavior repair rather than compile repair.
- The set intentionally spans calibration/control, data conversion/calibration, continuous dynamics, PLL phase integration, data conversion, event/timing, pointer/selection, stateful analog memory, and threshold/static nonlinear behavior.
- T1 residuals checked: 6 Spectre behavior failures, 1 TB compile failure, and 2 DUT compile failures. None were selected to keep this B1 smoke list S2-rooted and compile-OK.
