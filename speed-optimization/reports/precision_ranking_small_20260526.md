# Same-Server EVAS/Spectre Speed

Date: 2026-05-26
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host and the artifact emits checker/waveform Spectre-equivalence gates. Paper-facing speed claims should use only equivalence-gated rows and still need repeated cold/warm runs.

## Scope

- Host: `thu-sui`
- Selected rows: 10
- Jobs: 5
- EVAS modes: `strict_current, profile_fast_skip_source_error_control`
- Spectre modes: `spectre_ax_default_speed, spectre_ax_equalized_precision, spectre_reference_strict_primary`
- Output root: `results/precision-ranking-small-20260526-r2`

## 本轮结论摘要

本轮是 10 个 e2e release gold 行的 smoke matrix，不是最终 release-wide 结论。矩阵包含 5 个条件：EVAS strict、EVAS fast、Spectre AX default speed、Spectre AX equalized precision、Spectre reference strict primary，共 50 次仿真。

- 仿真可运行性：50/50 都生成了波形；Spectre 30/30 `simulation_ok`，EVAS 20/20 `simulation_ok`。
- 行为检查：每个模式都是 9/10 通过。唯一失败是 `vbr1_l1_binary_weighted_voltage_dac`，且 strict Spectre、Spectre AX、EVAS 全部失败同一个 checker，因此先按任务/checker/gold 问题处理，不归因于 EVAS 精度。
- 波形精度：以 `spectre_reference_strict_primary` 为参考，EVAS fast、EVAS strict、Spectre AX default、Spectre AX equalized 四组 candidate 都是 10/10 通过等价门限。
- 精度口径：本轮可以说 EVAS fast 在这 10 行上满足等价门限；但不能说 EVAS fast 普遍比 Spectre AX 更精准，因为 `gain_estimator` 等行上 EVAS 相对 strict Spectre 的差异大于 AX。
- 速度口径：EVAS fast 相对 Spectre AX default 在 6/10 行更快，但总时间为 85.706s vs 14.174s，聚合速度比 `Spectre/EVAS = 0.165x`，所以本轮不能支撑“EVAS fast 比 Spectre AX 更快”的总体 claim。主要慢点集中在 PFD、CPPLL、gain、ramp/source 相关行。

## Mode Summary

| Backend | Mode | Runs | Sim OK | Behavior PASS | Behavior non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_skip_source_error_control | 10 | 10 | 9 | 1 | 85.706 | 8.571 |
| evas | strict_current | 10 | 10 | 9 | 1 | 282.524 | 28.252 |
| spectre | spectre_ax_default_speed | 10 | 10 | 9 | 1 | 14.174 | 1.417 |
| spectre | spectre_ax_equalized_precision | 10 | 10 | 9 | 1 | 15.527 | 1.553 |
| spectre | spectre_reference_strict_primary | 10 | 10 | 9 | 1 | 53.657 | 5.366 |

## Reference Comparison Summary

Each candidate is compared against the same-row strict Spectre reference. The waveform status uses the simulator-equivalence policy from `run_gold_dual_suite.py`.

| Candidate | Runs | Passed | Needs review | Blocked | Worst max abs V | Worst max relative RMS error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `evas/profile_fast_skip_source_error_control` | 10 | 10 | 0 | 0 | 1 | 0.127836 |
| `evas/strict_current` | 10 | 10 | 0 | 0 | 1 | 0.127836 |
| `spectre/spectre_ax_default_speed` | 10 | 10 | 0 | 0 | 1 | 0.122542 |
| `spectre/spectre_ax_equalized_precision` | 10 | 10 | 0 | 0 | 1 | 0.122542 |

## Per-Row Reference Comparisons

| Entry | Form | Variant | Candidate | Reference | Behavior OK | Waveform | Max abs V | Max relative RMS error | Signals |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.0569985 | 0.00630664 | 5 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.0569985 | 0.00630664 | 5 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre/spectre_ax_default_speed` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.0197224 | 0.00175035 | 5 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.0197224 | 0.00175035 | 5 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre/spectre_ax_default_speed` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.54543e-07 | 7.69535e-08 | 5 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.000487804 | 4.90351e-05 | 5 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre/spectre_ax_default_speed` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.43425e-05 | 5.70416e-06 | 5 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.43425e-05 | 5.70416e-06 | 5 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 8.95699e-08 | 9.50284e-09 | 3 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.93208e-05 | 2.21536e-06 | 3 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre/spectre_ax_default_speed` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 8.86545e-06 | 7.12526e-07 | 3 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 8.86545e-06 | 7.12526e-07 | 3 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.231542 | 0.127836 | 4 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.209265 | 0.127836 | 4 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre/spectre_ax_default_speed` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0433608 | 0.00221414 | 4 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0433608 | 0.00221414 | 4 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.56907e-08 | 5.34204e-09 | 4 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.56907e-08 | 5.46698e-09 | 4 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre/spectre_ax_default_speed` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 9.65894e-15 | 3.13341e-15 | 4 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 9.65894e-15 | 3.13341e-15 | 4 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.127719 | 2 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.127719 | 2 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre/spectre_ax_default_speed` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.122542 | 2 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.122542 | 2 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre/spectre_ax_default_speed` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | - | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | - | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre/spectre_ax_default_speed` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | - | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | - | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.46989e-07 | 2.16459e-07 | 13 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.52701e-06 | 3.62085e-07 | 13 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre/spectre_ax_default_speed` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 2.29049e-05 | 1.00009e-06 | 13 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 2.29049e-05 | 1.00009e-06 | 13 |

## Spectre Run Settings

This table records the final staged testbench settings used by Spectre. For normalized precision-ranking modes, `tran` and `simulatorOptions` are rewritten before Spectre is launched; speed-baseline modes keep the staged testbench unchanged.

| Entry | Form | Variant | Mode | Normalized | CLI args | tran line | simulatorOptions line | Result root |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_ax_default_speed` | `False` | `+preset=ax +mt` | `tran tran stop=165n maxstep=500p` | - | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_binary_weighted_voltage_dac/e2e/gold/vbm1_simple_binary_voltage_dac_4b_e2e/spectre_ax_default_speed` |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=165n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_binary_weighted_voltage_dac/e2e/gold/vbm1_simple_binary_voltage_dac_4b_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=165n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_binary_weighted_voltage_dac/e2e/gold/vbm1_simple_binary_voltage_dac_4b_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_default_speed` | `False` | `+preset=ax +mt` | `tran tran stop=3000n maxstep=5n` | - | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_burst_clock_source/e2e/gold/clk_burst_gen_smoke/spectre_ax_default_speed` |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=3000n maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_burst_clock_source/e2e/gold/clk_burst_gen_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=3000n maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_burst_clock_source/e2e/gold/clk_burst_gen_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_default_speed` | `False` | `+preset=ax +mt` | `tran tran stop=80n maxstep=0.5n` | - | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_calibration_deadband_controller/e2e/gold/vbr1_l1_calibration_deadband_controller_e2e/spectre_ax_default_speed` |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_calibration_deadband_controller/e2e/gold/vbr1_l1_calibration_deadband_controller_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_calibration_deadband_controller/e2e/gold/vbr1_l1_calibration_deadband_controller_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_default_speed` | `False` | `+preset=ax +mt` | `tran tran stop=1u maxstep=2n` | - | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_clocked_sample_and_hold/e2e/gold/sample_hold_smoke/spectre_ax_default_speed` |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=1u maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_clocked_sample_and_hold/e2e/gold/sample_hold_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=1u maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_clocked_sample_and_hold/e2e/gold/sample_hold_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_default_speed` | `False` | `+preset=ax +mt` | `tran tran stop=200u maxstep=8n` | - | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_gain_estimator/e2e/gold/gain_extraction_smoke/spectre_ax_default_speed` |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=200u maxstep=8n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_gain_estimator/e2e/gold/gain_extraction_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=200u maxstep=8n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_gain_estimator/e2e/gold/gain_extraction_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_default_speed` | `False` | `+preset=ax +mt` | `tran tran stop=300n maxstep=10p errpreset=conservative` | `simulatorOptions options reltol=1e-4 vabstol=1e-6 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_pfd_up_dn_logic/e2e/gold/vbm1_pfd_reset_race_e2e/spectre_ax_default_speed` |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=300n maxstep=10p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_pfd_up_dn_logic/e2e/gold/vbm1_pfd_reset_race_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=300n maxstep=10p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_pfd_up_dn_logic/e2e/gold/vbm1_pfd_reset_race_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_default_speed` | `False` | `+preset=ax +mt` | `tran tran stop=34n maxstep=20n errpreset=conservative` | `simulatorOptions options reltol=1e-4 vabstol=1e-6 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_ramp_or_step_source/e2e/gold/bound_step_period_guard_smoke/spectre_ax_default_speed` |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=34n maxstep=20n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_ramp_or_step_source/e2e/gold/bound_step_period_guard_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=34n maxstep=20n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_ramp_or_step_source/e2e/gold/bound_step_period_guard_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_default_speed` | `False` | `+preset=ax +mt` | `tran tran stop=30n maxstep=0.5n` | - | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_threshold_comparator/e2e/gold/comparator_smoke/spectre_ax_default_speed` |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=30n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_threshold_comparator/e2e/gold/comparator_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=30n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l1_threshold_comparator/e2e/gold/comparator_smoke/spectre_reference_strict_primary` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_default_speed` | `False` | `+preset=ax +mt` | `tran tran stop=6u maxstep=5n errpreset=conservative` | - | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow/e2e/gold/cppll_freq_step_reacquire_smoke/spectre_ax_default_speed` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=6u maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow/e2e/gold/cppll_freq_step_reacquire_smoke/spectre_ax_equalized_precision` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=6u maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow/e2e/gold/cppll_freq_step_reacquire_smoke/spectre_reference_strict_primary` |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_default_speed` | `False` | `+preset=ax +mt` | `tran tran stop=10u maxstep=5n` | - | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l2_weighted_sar_adc_dac_loop/e2e/gold/sar_adc_dac_weighted_8b_smoke/spectre_ax_default_speed` |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=10u maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l2_weighted_sar_adc_dac_loop/e2e/gold/sar_adc_dac_weighted_8b_smoke/spectre_ax_equalized_precision` |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=10u maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-small-20260526-r2/spectre/vbr1_l2_weighted_sar_adc_dac_loop/e2e/gold/sar_adc_dac_weighted_8b_smoke/spectre_reference_strict_primary` |

## Spectre-Equivalence Gate Summary

These gates check whether EVAS preserves task behavior and stays within accepted Spectre-equivalent waveform tolerance. They are not a higher-than-Spectre precision target.

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| profile_fast_skip_source_error_control | 10 | 9 | 1 | 0 | 0 |
| strict_current | 10 | 9 | 1 | 0 | 0 |

## Per-Row Spectre-Equivalence Gates

| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `strict_current` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_default_speed_parity:spectre_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_default_speed_parity:spectre_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |

## Simulation-Only Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 1.154 | 0.562 | 2.054 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 1.154 | 0.518 | 2.227 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.113 | 0.562 | 1.981 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.113 | 0.518 | 2.148 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.882 | 0.562 | 6.910 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.882 | 0.518 | 7.492 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 0.750 | 0.569 | 1.319 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 0.750 | 1.055 | 0.711 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.793 | 0.569 | 1.395 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.793 | 1.055 | 0.752 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.549 | 0.569 | 6.242 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.549 | 1.055 | 3.365 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 1.099 | 0.439 | 2.503 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 1.099 | 1.200 | 0.916 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.121 | 0.439 | 2.553 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.121 | 1.200 | 0.935 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.787 | 0.439 | 8.623 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.787 | 1.200 | 3.157 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 0.836 | 0.556 | 1.504 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 0.836 | 1.172 | 0.713 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.049 | 0.556 | 1.888 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.049 | 1.172 | 0.895 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.122 | 0.556 | 3.818 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.122 | 1.172 | 1.810 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 5.145 | 11.193 | 0.460 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 5.145 | 129.621 | 0.040 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 4.815 | 11.193 | 0.430 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 4.815 | 129.621 | 0.037 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 13.809 | 11.193 | 1.234 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 13.809 | 129.621 | 0.107 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 0.699 | 18.252 | 0.038 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 0.699 | 90.129 | 0.008 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.944 | 18.252 | 0.107 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.944 | 90.129 | 0.022 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 5.050 | 18.252 | 0.277 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 5.050 | 90.129 | 0.056 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 0.656 | 0.925 | 0.709 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 0.656 | 1.597 | 0.411 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.671 | 0.925 | 0.726 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.671 | 1.597 | 0.420 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.207 | 0.925 | 3.468 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.207 | 1.597 | 2.009 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 0.593 | 0.333 | 1.781 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 0.593 | 0.417 | 1.422 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.751 | 0.333 | 2.255 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.751 | 0.417 | 1.800 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.571 | 0.333 | 10.726 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.571 | 0.417 | 8.562 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 1.591 | 51.443 | 0.031 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 1.591 | 40.303 | 0.039 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.994 | 51.443 | 0.039 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.994 | 40.303 | 0.049 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 6.959 | 51.443 | 0.135 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 6.959 | 40.303 | 0.173 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 1.651 | 1.435 | 1.150 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 1.651 | 16.514 | 0.100 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.275 | 1.435 | 0.889 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.275 | 16.514 | 0.077 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 7.720 | 1.435 | 5.380 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 7.720 | 16.514 | 0.468 |

## Spectre-Equivalence-Gated Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 0.750 | 0.569 | 1.319 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 0.750 | 1.055 | 0.711 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.793 | 0.569 | 1.395 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.793 | 1.055 | 0.752 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.549 | 0.569 | 6.242 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.549 | 1.055 | 3.365 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 1.099 | 0.439 | 2.503 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 1.099 | 1.200 | 0.916 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.121 | 0.439 | 2.553 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.121 | 1.200 | 0.935 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.787 | 0.439 | 8.623 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.787 | 1.200 | 3.157 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 0.836 | 0.556 | 1.504 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 0.836 | 1.172 | 0.713 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.049 | 0.556 | 1.888 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.049 | 1.172 | 0.895 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.122 | 0.556 | 3.818 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.122 | 1.172 | 1.810 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 5.145 | 11.193 | 0.460 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 5.145 | 129.621 | 0.040 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 4.815 | 11.193 | 0.430 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 4.815 | 129.621 | 0.037 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 13.809 | 11.193 | 1.234 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 13.809 | 129.621 | 0.107 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 0.699 | 18.252 | 0.038 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 0.699 | 90.129 | 0.008 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.944 | 18.252 | 0.107 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.944 | 90.129 | 0.022 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 5.050 | 18.252 | 0.277 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 5.050 | 90.129 | 0.056 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 0.656 | 0.925 | 0.709 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 0.656 | 1.597 | 0.411 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.671 | 0.925 | 0.726 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.671 | 1.597 | 0.420 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.207 | 0.925 | 3.468 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.207 | 1.597 | 2.009 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 0.593 | 0.333 | 1.781 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 0.593 | 0.417 | 1.422 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.751 | 0.333 | 2.255 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.751 | 0.417 | 1.800 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.571 | 0.333 | 10.726 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.571 | 0.417 | 8.562 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 1.591 | 51.443 | 0.031 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 1.591 | 40.303 | 0.039 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.994 | 51.443 | 0.039 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.994 | 40.303 | 0.049 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 6.959 | 51.443 | 0.135 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 6.959 | 40.303 | 0.173 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_default_speed` | `profile_fast_skip_source_error_control` | 1.651 | 1.435 | 1.150 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_default_speed` | `strict_current` | 1.651 | 16.514 | 0.100 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.275 | 1.435 | 0.889 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.275 | 16.514 | 0.077 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 7.720 | 1.435 | 5.380 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 7.720 | 16.514 | 0.468 |

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
