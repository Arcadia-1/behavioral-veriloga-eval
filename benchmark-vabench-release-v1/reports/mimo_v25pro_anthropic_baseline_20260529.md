# MiMo v2.5 Pro Anthropic Baseline (2026-05-29)

## Scope

- Benchmark: vaBench release v1 scored 236 forms.
- API: Anthropic-compatible Messages API; key redacted.
- Runner wrapper: `release-runner-wrapper-v5`.
- Final judge: Spectre; EVAS is reported as fast first-stage/debug signal only.

## Main Results

| Metric | MiMo v2.5 Pro | DeepSeek v4-pro reference |
| --- | ---: | ---: |
| EVAS first-stage pass | 48/236 (20.3%) | n/a |
| Spectre final pass | 51/236 (21.6%) | 59/236 (25.0%) |
| Strict EVAS/Spectre dual pass | 44/236 (18.6%) | 59/236 (25.0%) |
| Completed Spectre rows | 212/236 | n/a |
| Skipped/missing artifact rows | 24/236 | n/a |
| EVAS PASS / Spectre FAIL | 6 | n/a |
| Spectre PASS / EVAS FAIL | 7 | n/a |

## Generation

| Item | Count |
| --- | ---: |
| `generated` | 215 |
| `no_code_extracted` | 21 |
| finish `max_tokens` | 23 |
| finish `end_turn` | 213 |
| input tokens | 430579 |
| output tokens | 1115395 |
| total tokens | 1545974 |

## By Form

| Form | Total | Spectre Pass | Strict Dual Pass | Skipped |
| --- | ---: | ---: | ---: | ---: |
| `bugfix` | 52 | 12 | 10 | 2 |
| `dut` | 52 | 15 | 13 | 3 |
| `e2e` | 66 | 6 | 5 | 18 |
| `tb` | 66 | 18 | 16 | 1 |

## By Category

| Category | Total | Spectre Pass | Strict Dual Pass | Skipped |
| --- | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 30 | 3 | 3 | 0 |
| Bias Reference and Power Management | 28 | 0 | 0 | 1 |
| Calibration, DEM, and Control | 26 | 4 | 3 | 3 |
| Comparator and Decision Circuits | 30 | 9 | 7 | 2 |
| Data Converter Models | 44 | 18 | 17 | 7 |
| PLL Clock and Timing Systems | 36 | 9 | 8 | 8 |
| RF and AFE Behavioral Macromodels | 24 | 3 | 1 | 2 |
| Sampling and Analog Memory | 18 | 5 | 5 | 1 |

## Skipped Rows

| Task | Form | Category | Generation | Finish |
| --- | --- | --- | --- | --- |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow:e2e` | `e2e` | PLL Clock and Timing Systems | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_bang_bang_phase_detector:e2e` | `e2e` | PLL Clock and Timing Systems | `generated` | `max_tokens` |
| `vbr1_l1_propagation_delay_comparator:e2e` | `e2e` | Comparator and Decision Circuits | `no_code_extracted` | `max_tokens` |
| `vbr1_l2_comparator_measurement_flow:e2e` | `e2e` | Comparator and Decision Circuits | `no_code_extracted` | `end_turn` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:e2e` | `e2e` | PLL Clock and Timing Systems | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_dwa_dem_encoder:e2e` | `e2e` | Calibration, DEM, and Control | `no_code_extracted` | `max_tokens` |
| `vbr1_l2_pipeline_adc_chain:e2e` | `e2e` | Data Converter Models | `no_code_extracted` | `max_tokens` |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `e2e` | Data Converter Models | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_lock_detector:dut` | `dut` | PLL Clock and Timing Systems | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_lock_detector:e2e` | `e2e` | PLL Clock and Timing Systems | `generated` | `max_tokens` |
| `vbr1_l1_clock_divider:dut` | `dut` | PLL Clock and Timing Systems | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_clock_divider:e2e` | `e2e` | PLL Clock and Timing Systems | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_segmented_dac:e2e` | `e2e` | Data Converter Models | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_aperture_delay_track_and_hold:e2e` | `e2e` | Sampling and Analog Memory | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:e2e` | `e2e` | Data Converter Models | `generated` | `max_tokens` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:tb` | `tb` | Data Converter Models | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_clock_divider:bugfix` | `bugfix` | PLL Clock and Timing Systems | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_dac_mismatch_unit_weighting_model:bugfix` | `bugfix` | Data Converter Models | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_dwa_dem_encoder:dut` | `dut` | Calibration, DEM, and Control | `no_code_extracted` | `max_tokens` |
| `vbr1_l1_pa_compression_macro:e2e` | `e2e` | RF and AFE Behavioral Macromodels | `no_code_extracted` | `max_tokens` |
| `vbr1_l2_agc_receiver_leveling_loop:e2e` | `e2e` | RF and AFE Behavioral Macromodels | `no_code_extracted` | `max_tokens` |
| `vbr1_l2_complete_calibration_loop:e2e` | `e2e` | Calibration, DEM, and Control | `no_code_extracted` | `max_tokens` |
| `vbr1_l2_converter_static_linearity_measurement_flow:e2e` | `e2e` | Data Converter Models | `no_code_extracted` | `max_tokens` |
| `vbr1_l2_ldo_load_step_recovery_flow:e2e` | `e2e` | Bias Reference and Power Management | `no_code_extracted` | `max_tokens` |

## EVAS/Spectre Mismatches

### EVAS PASS / Spectre FAIL

| Task | Form | Category | Dual Status | Spectre Backend |
| --- | --- | --- | --- | --- |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:dut` | `dut` | Data Converter Models | `FAIL_SPECTRE` | `error` |
| `vbr1_l1_debounce_latch:dut` | `dut` | Comparator and Decision Circuits | `FAIL_SPECTRE` | `error` |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | `dut` | Sampling and Analog Memory | `FAIL_SPECTRE` | `error` |
| `vbr1_l1_power_on_reset_detector:dut` | `dut` | Bias Reference and Power Management | `FAIL_SPECTRE` | `error` |
| `vbr1_l1_sample_and_hold_with_droop_leakage:e2e` | `e2e` | Sampling and Analog Memory | `FAIL_SPECTRE_BEHAVIOR` | `success` |
| `vbr1_l1_soft_hysteretic_limiter:bugfix` | `bugfix` | Baseband Signal Conditioning | `FAIL_SPECTRE_BEHAVIOR` | `success` |

### Spectre PASS / EVAS FAIL

| Task | Form | Category | EVAS Status |
| --- | --- | --- | --- |
| `vbr1_l1_threshold_comparator:e2e` | `e2e` | Comparator and Decision Circuits | `FAIL_SIM_CORRECTNESS` |
| `vbr1_l1_trim_calibration_controller:tb` | `tb` | Calibration, DEM, and Control | `FAIL_SIM_CORRECTNESS` |
| `vbr1_l1_clock_divider:tb` | `tb` | PLL Clock and Timing Systems | `FAIL_DUT_COMPILE` |
| `vbr1_l1_thermometer_code_decoder:dut` | `dut` | Data Converter Models | `FAIL_SIM_CORRECTNESS` |
| `vbr1_l1_lna_gain_compression_macro:bugfix` | `bugfix` | RF and AFE Behavioral Macromodels | `FAIL_SIM_CORRECTNESS` |
| `vbr1_l1_rf_mixer_downconverter_macro:dut` | `dut` | RF and AFE Behavioral Macromodels | `FAIL_SIM_CORRECTNESS` |
| `vbr1_l1_window_comparator_detector:bugfix` | `bugfix` | Comparator and Decision Circuits | `FAIL_SIM_CORRECTNESS` |

## Interpretation

- The conservative model score is Spectre-final `51/236 = 21.6%`, below the current DeepSeek overlay `59/236 = 25.0%`.
- MiMo has a larger generation-completion problem: 24 rows could not enter Spectre dual judgment, mostly `max_tokens` truncation in L2/e2e or support/timing rows.
- The 6 EVAS PASS / Spectre FAIL and 7 Spectre PASS / EVAS FAIL rows should be treated as evaluator/parity follow-up items before using EVAS-only numbers for claims.
