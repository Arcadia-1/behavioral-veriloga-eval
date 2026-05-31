# DeepSeek Wrapper-v4 Failed-48 Drilldown

Generated: `2026-05-28T08:16:20.292821+00:00`

Scope: failed rows from the wrapper-v4 changed55 rerun. Failed rows: 48.

Manual review note: Two missing-disciplines rows are not clean model failures because wrapper-v4 rendered the Verilog-A include literal ambiguously; rerun them under release-runner-wrapper-v5.

## Status Counts

| Status | Count |
| --- | ---: |
| `FAIL_SIM_CORRECTNESS` | 37 |
| `FAIL_DUT_COMPILE` | 10 |
| `FAIL_TB_COMPILE` | 1 |

## Root Families

| Root family | Count |
| --- | ---: |
| Behavior: missing/incorrect event timing or stimulus coverage | 7 |
| Verilog-A subset: local declaration inside analog/procedural block | 7 |
| Behavior: wrong decision/code sequence | 6 |
| Behavior: calibration/control algorithm wrong | 5 |
| Spectre TB syntax: malformed instance/source line | 1 |
| Behavior: output stuck or reset/hold state wrong | 7 |
| Behavior: analog transfer/reference macro wrong | 10 |
| Wrapper-v4 text ambiguity: include literal missing Verilog-A backtick | 2 |
| Behavior: sample/hold droop or hold-window behavior wrong | 2 |
| Verilog-A subset: transition() used inside conditional/event block | 1 |

## By Form and Status

| Form | Status counts |
| --- | --- |
| `bugfix` | `{'FAIL_SIM_CORRECTNESS': 8, 'FAIL_DUT_COMPILE': 2}` |
| `dut` | `{'FAIL_DUT_COMPILE': 1, 'FAIL_SIM_CORRECTNESS': 3}` |
| `e2e` | `{'FAIL_SIM_CORRECTNESS': 18, 'FAIL_DUT_COMPILE': 6, 'FAIL_TB_COMPILE': 1}` |
| `tb` | `{'FAIL_SIM_CORRECTNESS': 8, 'FAIL_DUT_COMPILE': 1}` |

## Failed Rows

| Release task id | Form | Status | Root family | Evidence |
| --- | --- | --- | --- | --- |
| `vbr1_l1_bang_bang_phase_detector:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: missing/incorrect event timing or stimulus coverage | too_few_data_edges=0 |
| `vbr1_l1_dwa_dem_encoder:e2e` | `e2e` | `FAIL_DUT_COMPILE` | Verilog-A subset: local declaration inside analog/procedural block | ERROR: Failed to compile Verilog-A file dwa_ptr_gen.va: Parse error at L107:5: Spectre-incompatible local declaration inside analog/procedural statement; move declarations to module scope |
| `vbr1_l2_flash_adc_mini_array:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: wrong decision/code sequence | observed_codes=0,1,2,3,4,5,6,7 expected_codes=1,2,3,4,5,6,7 comparator_mismatches=7 thermometer_errors=0 encoder_mismatches=0 reversals=0 |
| `vbr1_l2_pipeline_adc_chain:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: wrong decision/code sequence | observed_codes=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 expected_codes=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 stage_bit_mismatches=0 final_concat_mismatches=0 final_code_mismatches=0 residue_mismatches=15 ... |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `e2e` | `FAIL_TB_COMPILE` | Verilog-A subset: local declaration inside analog/procedural block | ERROR: Failed to compile Verilog-A file sar_adc_weighted_8b.va: Parse error at L106:9: Spectre-incompatible local declaration inside analog/procedural statement; move declarations to module scope |
| `vbr1_l1_gain_trim_controller:bugfix` | `bugfix` | `FAIL_SIM_CORRECTNESS` | Behavior: calibration/control algorithm wrong | gain_trim_samples=0.500,0.700,1.000,1.000,0.800,0.000,0.000,0.000 reset_nominal=False low_meas_increases=False reaches_upper_clamp=False high_meas_decreases=True reaches_lower_clamp=False in_range=... |
| `vbr1_l1_gain_trim_controller:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: calibration/control algorithm wrong | gain_trim_samples=0.300,0.350,0.550,0.800,0.850,0.450,0.150,0.100 reset_nominal=True low_meas_increases=True reaches_upper_clamp=False high_meas_decreases=False reaches_lower_clamp=False in_range=True |
| `vbr1_l1_offset_comparator:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: wrong decision/code sequence | offset_decisions=LLLHHLL expected=LHHHLLL |
| `vbr1_l1_pfd_up_dn_logic:bugfix` | `bugfix` | `FAIL_SIM_CORRECTNESS` | Behavior: missing/incorrect event timing or stimulus coverage | up_first=0.0000 dn_first=0.0000 up_second=0.0000 dn_second=0.0000 up_pulses_first=0 dn_pulses_second=0 overlap_frac=0.0000 |
| `vbr1_l1_pfd_up_dn_logic:tb` | `tb` | `FAIL_SIM_CORRECTNESS` | Behavior: missing/incorrect event timing or stimulus coverage | up_first=0.0000 dn_first=0.0498 up_second=0.0000 dn_second=0.0000 up_pulses_first=0 dn_pulses_second=0 overlap_frac=0.0000 |
| `vbr1_l1_sar_logic:dut` | `dut` | `FAIL_DUT_COMPILE` | Verilog-A subset: local declaration inside analog/procedural block | ERROR: Failed to compile Verilog-A file sar_logic_4b.va: Parse error at L66:13: Spectre-incompatible local declaration inside analog/procedural statement; move declarations to module scope |
| `vbr1_l1_sar_logic:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: wrong decision/code sequence | sar_rdy_sequence=LLL expected=LHL code176=1000 expected_code=1010 |
| `vbr1_l1_segmented_dac:tb` | `tb` | `FAIL_DUT_COMPILE` | Spectre TB syntax: malformed instance/source line | ERROR: Failed to parse tb_segmented_dac_ref.scs: Spectre instance/source syntax expects exactly one name before the node list; got '* Stimulus for binary bits: b0' |
| `vbr1_l1_binary_weighted_voltage_dac:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: wrong decision/code sequence | simple_binary_dac_levels=0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000 expected=0.000,0.060,0.120,0.180,0.240,0.300,0.360,0.420,0.480,0.540,0.600,0... |
| `vbr1_l1_strongarm_style_latch_comparator:e2e` | `e2e` | `FAIL_DUT_COMPILE` | Verilog-A subset: local declaration inside analog/procedural block | ERROR: Failed to compile Verilog-A file cmp_strongarm.va: Parse error at L53:5: Spectre-incompatible local declaration inside analog/procedural statement; move declarations to module scope |
| `vbr1_l1_thermometer_code_decoder:tb` | `tb` | `FAIL_SIM_CORRECTNESS` | Behavior: wrong decision/code sequence | thermometer_sequence=-,-,0,01,012,- expected=-,-,0,01,012,012 |
| `vbr1_l1_acquisition_limited_sample_and_hold:bugfix` | `bugfix` | `FAIL_SIM_CORRECTNESS` | Behavior: output stuck or reset/hold state wrong | acq_hold_reset_out=0.000 |
| `vbr1_l1_acquisition_limited_sample_and_hold:dut` | `dut` | `FAIL_SIM_CORRECTNESS` | Behavior: output stuck or reset/hold state wrong | acq_hold_reset_out=0.000 |
| `vbr1_l1_acquisition_limited_sample_and_hold:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: output stuck or reset/hold state wrong | acq_hold_reset_out=0.000 |
| `vbr1_l1_aperture_delay_track_and_hold:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: output stuck or reset/hold state wrong | aperture_samples=0.000,0.000,0.000,0.000,0.000,0.000,0.000 expected=0.695,0.304,0.598,0.405,0.793,0.204,0.505 mismatches=7 span=0.000 |
| `vbr1_l1_bandgap_reference_macro_model:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | bandgap_reference_nominal_wrong=0.159 |
| `vbr1_l1_bang_bang_phase_detector:tb` | `tb` | `FAIL_SIM_CORRECTNESS` | Behavior: missing/incorrect event timing or stimulus coverage | lead_window_updn=1/23 |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | bias_low_trim_wrong=0.800 |
| `vbr1_l1_calibration_deadband_controller:bugfix` | `bugfix` | `FAIL_DUT_COMPILE` | Verilog-A subset: local declaration inside analog/procedural block | ERROR: Failed to compile Verilog-A file calibration_deadband_controller.va: Parse error at L79:7: Spectre-incompatible local declaration inside analog/procedural statement; move declarations to mod... |
| `vbr1_l1_calibration_deadband_controller:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: calibration/control algorithm wrong | trim_direction_mismatches=3/3 |
| `vbr1_l1_calibration_deadband_controller:tb` | `tb` | `FAIL_SIM_CORRECTNESS` | Behavior: calibration/control algorithm wrong | deadband_missing_hold_samples=0 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: missing/incorrect event timing or stimulus coverage | clk_edges=9 |
| `vbr1_l1_higher_order_filter:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: output stuck or reset/hold state wrong | two_pole_reset_out=0.000 |
| `vbr1_l1_ldo_regulator_macro_model:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | ldo_light_load_regulation_wrong=1.800 |
| `vbr1_l1_limiting_amplifier_frontend:tb` | `tb` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | limiter_small_gain_missing vin=0.445 out=0.450 |
| `vbr1_l1_lna_gain_compression_macro:e2e` | `e2e` | `FAIL_DUT_COMPILE` | Wrapper-v4 text ambiguity: include literal missing Verilog-A backtick | lna_gain_compression_macro.va:missing_disciplines_vams ; manual_review=wrapper-v4 rendered include rule ambiguously; rerun under release-runner-wrapper-v5 |
| `vbr1_l1_log_rssi_power_detector:bugfix` | `bugfix` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | rssi_floor_wrong=0.000 |
| `vbr1_l1_precision_rectifier_envelope_detector:bugfix` | `bugfix` | `FAIL_DUT_COMPILE` | Verilog-A subset: local declaration inside analog/procedural block | ERROR: Failed to compile Verilog-A file precision_rectifier_envelope_detector.va: Parse error at L75:7: Spectre-incompatible local declaration inside analog/procedural statement; move declarations ... |
| `vbr1_l1_programmable_gain_amplifier:bugfix` | `bugfix` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | pga_unclamped_range=(-0.000,1.000) |
| `vbr1_l1_programmable_gain_amplifier:dut` | `dut` | `FAIL_SIM_CORRECTNESS` | Behavior: output stuck or reset/hold state wrong | pga_reset_out=0.000 |
| `vbr1_l1_programmable_gain_amplifier:e2e` | `e2e` | `FAIL_DUT_COMPILE` | Wrapper-v4 text ambiguity: include literal missing Verilog-A backtick | programmable_gain_amplifier.va:missing_disciplines_vams ; manual_review=wrapper-v4 rendered include rule ambiguously; rerun under release-runner-wrapper-v5 |
| `vbr1_l1_rf_mixer_downconverter_macro:bugfix` | `bugfix` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | mixer_positive_lo_polarity_wrong hi=0.079 lo=-0.063 |
| `vbr1_l1_sample_and_hold_with_droop_leakage:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: sample/hold droop or hold-window behavior wrong | insufficient_droop_window_samples=0 |
| `vbr1_l1_sample_and_hold_with_droop_leakage:tb` | `tb` | `FAIL_SIM_CORRECTNESS` | Behavior: sample/hold droop or hold-window behavior wrong | vin_samples=0.500,0.800,0.200 held_samples=0.497,0.795,0.199 max_sample_err=0.005 expected_span=0.600 observed_span=0.596 droop=0.618 upward_steps=0 reset_clear=True |
| `vbr1_l1_soft_hysteretic_limiter:bugfix` | `bugfix` | `FAIL_SIM_CORRECTNESS` | Behavior: output stuck or reset/hold state wrong | soft_limiter_high_compression=0.000 |
| `vbr1_l1_soft_hysteretic_limiter:e2e` | `e2e` | `FAIL_DUT_COMPILE` | Verilog-A subset: transition() used inside conditional/event block | ERROR: Failed to compile Verilog-A file soft_hysteretic_limiter.va: Spectre-incompatible Verilog-A: transition() contribution is inside a conditional/event/loop/case statement |
| `vbr1_l1_successive_approximation_calibration_search_fsm:dut` | `dut` | `FAIL_SIM_CORRECTNESS` | Behavior: calibration/control algorithm wrong | sar_cal_reset_mean=0.773 |
| `vbr1_l1_uvlo_brownout_detector:bugfix` | `bugfix` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | uvlo_hysteresis_hold_failed good=0.000 hold=0.000 |
| `vbr1_l1_uvlo_brownout_detector:tb` | `tb` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | uvlo_brownout_or_lower_hold_failed brownout=0.900 hold=0.900 |
| `vbr1_l2_complete_calibration_loop:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: missing/incorrect event timing or stimulus coverage | complete_cal_loop_input_span_too_small=0.300 |
| `vbr1_l2_flash_adc_mini_array:tb` | `tb` | `FAIL_SIM_CORRECTNESS` | Behavior: missing/incorrect event timing or stimulus coverage | too_few_settled_samples=0 |
| `vbr1_l2_iq_downconversion_chain:e2e` | `e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | iq_positive_quadrature_missing i=0.300 q=0.300 |
| `vbr1_l2_ldo_load_step_recovery_flow:e2e` | `e2e` | `FAIL_DUT_COMPILE` | Verilog-A subset: local declaration inside analog/procedural block | ERROR: Failed to compile Verilog-A file ldo_load_step_recovery_flow.va: Parse error at L79:5: Spectre-incompatible local declaration inside analog/procedural statement; move declarations to module ... |
