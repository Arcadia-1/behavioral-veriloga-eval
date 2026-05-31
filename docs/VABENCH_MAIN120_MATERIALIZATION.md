# vaBench Main120 Materialization Inventory

Generated: 2026-05-15

## Summary

This inventory tracks `vabench-main-v1-main120` as validated result
evidence plus its source-controlled benchmark release state. It separates
materialized public tasks from fixed-only historical rows that are retained
as evidence-only.

| Metric | Value |
| --- | --- |
| EVAS pass tasks | 120 |
| Spectre pass tasks | 120 |
| Paired EVAS/Spectre task IDs | 120 |
| Dual PASS rows | 120 |
| Exact overlap with current `tasks/` IDs | 116 |
| Rows needing source task materialization | 0 |
| Evidence-only rows intentionally not materialized | 4 |
| Rows with staged source assets in both runs | 120 |
| Rows where EVAS/Spectre staged source hashes match | 120 |
| Rows countable as model capability after current policy | 115 |
| Rows countable as bugfix claim after current policy | 25 |
| Row-level CSV | `docs/VABENCH_MAIN120_MATERIALIZATION.csv` |

## Claim Wording

Use this conservative wording in paper-facing text and PR summaries:

- `main120` contains 120 EVAS/Spectre dual-validated evidence rows.
- 116 rows are materialized as source-controlled `prompt.md`/`meta.json`/`checks.yaml`/`gold/` benchmark tasks.
- 115 rows count toward model-capability evaluation under the current policy.
- 25 rows count as bugfix tasks because they have buggy/fixed provenance and EVAS/Spectre confirmation.
- 4 fixed-only historical rows are intentionally closed as evidence-only without release source tasks; all evidence-only rows are excluded from model-capability and bugfix denominators.

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
| calibration | 24 |
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

## Promotion Policy State

These fields are policy gates, not final human-reviewed release labels.
`evidence-only` rows are retained in the inventory but excluded from
model-capability and bugfix-claim denominators until a reviewer approves
a real source task.

| Release form | Rows |
| --- | --- |
| normal | 90 |
| true-bugfix | 25 |
| evidence-only | 5 |

| Provenance status | Rows |
| --- | --- |
| clean | 90 |
| reconstructed_badcase | 25 |
| historical_bugfix_fixed_only | 4 |
| badcase_available | 1 |

## Base Circuit Groups

The 120 rows are organized as 30 base circuits times four task forms.
Candidate current tasks are fuzzy hints for manual deduplication; they are
not source-of-truth mappings.

| Base | Forms present | Candidate current tasks |
| --- | --- | --- |
| background_calibration_accumulator | dut,tb,bugfix,e2e | - |
| barrel_pointer_window | dut,tb,bugfix,e2e | - |
| cdac_calibration | dut,tb,bugfix,e2e | - |
| debounce_latch | dut,tb,bugfix,e2e | - |
| edge_detector | dut,tb,bugfix,e2e | - |
| element_shuffler | dut,tb,bugfix,e2e | - |
| file_metric_writer | dut,tb,bugfix,e2e | vbm1_file_metric_writer_dut;vbm1_file_metric_writer_e2e;vbm1_file_metric_writer_tb |
| first_order_lowpass | dut,tb,bugfix,e2e | - |
| gain_trim_controller | dut,tb,bugfix,e2e | - |
| leaky_hold | dut,tb,bugfix,e2e | - |
| lock_detector | dut,tb,bugfix,e2e | - |
| offset_calibration_fsm | dut,tb,bugfix,e2e | - |
| offset_comparator | dut,tb,bugfix,e2e | - |
| one_shot_timer | dut,tb,bugfix,e2e | - |
| peak_detector | dut,tb,bugfix,e2e | - |
| pfd_reset_race | dut,tb,bugfix,e2e | - |
| precision_rectifier | dut,tb,bugfix,e2e | - |
| resettable_counter_divider | dut,tb,bugfix,e2e | vbm1_resettable_counter_divider_dut;vbm1_resettable_counter_divider_e2e;vbm1_resettable_counter_divider_tb |
| resettable_integrator | dut,tb,bugfix,e2e | - |
| rotating_element_selector | dut,tb,bugfix,e2e | - |
| sar_logic_4b | dut,tb,bugfix,e2e | - |
| segmented_dac | dut,tb,bugfix,e2e | - |
| settling_time_measurement_tb | dut,tb,bugfix,e2e | vbm1_settling_time_measurement_tb_dut;vbm1_settling_time_measurement_tb_e2e;vbm1_settling_time_measurement_tb_tb |
| slew_rate_limiter | dut,tb,bugfix,e2e | - |
| strongarm_comparator_behavior | dut,tb,bugfix,e2e | - |
| thermometer_dac | dut,tb,bugfix,e2e | - |
| thermometer_decoder_guarded | dut,tb,bugfix,e2e | - |
| track_hold_aperture | dut,tb,bugfix,e2e | - |
| vco_phase_integrator | dut,tb,bugfix,e2e | vbm1_vco_phase_integrator_dut;vbm1_vco_phase_integrator_e2e;vbm1_vco_phase_integrator_tb |
| voltage_clamp | dut,tb,bugfix,e2e | - |

## Materialization Decision

Ordinary `dut`, `tb`, and `e2e` rows now have source-controlled `prompt.md`, `meta.json`, `checks.yaml`, and `gold/` task directories. The only non-overlap rows are intentionally closed as evidence-only fixed-only bugfix history, so there is no remaining source-task materialization queue for main120.
