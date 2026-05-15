# vaBench Main120 Materialization Inventory

Generated: 2026-05-15

## Summary

This inventory treats `vabench-main-v1-main120` as validated result evidence
that still needs to be restored/materialized into source-controlled benchmark
tasks before it can serve as a release-quality benchmark source split.

| Metric | Value |
| --- | --- |
| EVAS pass tasks | 120 |
| Spectre pass tasks | 120 |
| Paired EVAS/Spectre task IDs | 120 |
| Dual PASS rows | 120 |
| Exact overlap with current `tasks/` IDs | 33 |
| Rows needing source task materialization | 87 |
| Rows with staged source assets in both runs | 120 |
| Rows where EVAS/Spectre staged source hashes match | 120 |
| Rows countable as model capability after current policy | 104 |
| Rows countable as bugfix claim after current policy | 14 |
| Row-level CSV | `docs/VABENCH_MAIN120_MATERIALIZATION.csv` |

## Source Evidence

| Evidence | Path |
| --- | --- |
| EVAS main120 summary | `results/vabench-main-v1-main120-gold-evas-2026-05-08/summary.json` |
| Spectre main120 summary | `results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08/summary.json` |

## Forms

| Form | Rows | Target family |
| --- | --- | --- |
| dut | 30 | spec-to-va |
| tb | 30 | tb-generation |
| bugfix | 30 | bugfix |
| e2e | 30 | end-to-end |

## Category Hints

| Category hint | Rows |
| --- | --- |
| calibration | 20 |
| dac | 16 |
| amplifier-filter | 12 |
| digital-logic | 12 |
| measurement | 12 |
| comparator | 8 |
| pll-clock | 8 |
| sample-hold | 8 |
| signal-source | 8 |
| adc-sar | 4 |
| analog-events | 4 |
| phase-detector | 4 |
| uncategorized | 4 |

## Promotion Policy State

These fields are policy gates, not final human-reviewed release labels.
`evidence-only` rows are retained in the inventory but excluded from
model-capability and bugfix-claim denominators until a reviewer approves
a real source task.

| Release form | Rows |
| --- | --- |
| normal | 90 |
| evidence-only | 16 |
| true-bugfix | 14 |

| Provenance status | Rows |
| --- | --- |
| clean | 90 |
| historical_bugfix_fixed_only | 15 |
| reconstructed_badcase | 14 |
| badcase_available | 1 |

## Base Circuit Groups

The 120 rows are organized as 30 base circuits times four task forms.
Candidate current tasks are fuzzy hints for manual deduplication; they are
not source-of-truth mappings.

| Base | Forms present | Candidate current tasks |
| --- | --- | --- |
| background_calibration_accumulator | dut,tb,bugfix,e2e | vbm1_background_calibration_accumulator_bugfix |
| barrel_pointer_window | dut,tb,bugfix,e2e | - |
| cdac_calibration | dut,tb,bugfix,e2e | cdac_cal;vbm1_cdac_calibration_bugfix |
| debounce_latch | dut,tb,bugfix,e2e | vbm1_debounce_latch_bugfix |
| edge_detector | dut,tb,bugfix,e2e | - |
| element_shuffler | dut,tb,bugfix,e2e | - |
| file_metric_writer | dut,tb,bugfix,e2e | - |
| first_order_lowpass | dut,tb,bugfix,e2e | - |
| gain_trim_controller | dut,tb,bugfix,e2e | - |
| leaky_hold | dut,tb,bugfix,e2e | sample_hold_smoke;vbm1_leaky_hold_bugfix |
| lock_detector | dut,tb,bugfix,e2e | - |
| offset_calibration_fsm | dut,tb,bugfix,e2e | - |
| offset_comparator | dut,tb,bugfix,e2e | comparator_offset_search_smoke;comparator_offset_tb |
| one_shot_timer | dut,tb,bugfix,e2e | vbm1_one_shot_timer_bugfix |
| peak_detector | dut,tb,bugfix,e2e | - |
| pfd_reset_race | dut,tb,bugfix,e2e | pfd_reset_race_smoke;vbm1_pfd_reset_race_bugfix |
| precision_rectifier | dut,tb,bugfix,e2e | - |
| resettable_counter_divider | dut,tb,bugfix,e2e | - |
| resettable_integrator | dut,tb,bugfix,e2e | - |
| rotating_element_selector | dut,tb,bugfix,e2e | - |
| sar_logic_4b | dut,tb,bugfix,e2e | gray_counter_4b_smoke;sar_logic;sar_logic_10b |
| segmented_dac | dut,tb,bugfix,e2e | - |
| settling_time_measurement_tb | dut,tb,bugfix,e2e | - |
| slew_rate_limiter | dut,tb,bugfix,e2e | - |
| strongarm_comparator_behavior | dut,tb,bugfix,e2e | - |
| thermometer_dac | dut,tb,bugfix,e2e | dac_ramp_tb;vbm1_thermometer_dac_15seg_bugfix;vbm1_thermometer_dac_bugfix |
| thermometer_decoder_guarded | dut,tb,bugfix,e2e | vbm1_thermometer_decoder_guarded_bugfix |
| track_hold_aperture | dut,tb,bugfix,e2e | sample_hold_aperture_tb;sample_hold_smoke;vbm1_track_hold_aperture_bugfix |
| vco_phase_integrator | dut,tb,bugfix,e2e | - |
| voltage_clamp | dut,tb,bugfix,e2e | - |

## Materialization Decision

The next safe action is to create source task directories from the staged
`.va`/`.scs` files and the recorded dual-pass evidence, while marking
`prompt.md`, `meta.json`, and `checks.yaml` as review targets rather than
pretending they already exist in `tasks/`.
