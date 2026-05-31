# Over-Abstracted Benchmark Audit - 2026-05-31

Scope: L2/core flow rows plus support L2 rows in `benchmark-vabench-release-v1`.

Audit rule: a row is over-abstracted when the public claim says loop, chain,
measurement flow, or composed behavior, but the gold/checker can pass by
scripted outputs or a direct target lookup without using the claimed
intermediate relation.

## Decision Summary

| Entry | Assessment | Evidence |
| --- | --- | --- |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | Fixed in this pass | Previous gold adjusted `ctrl_code` from a direct `ratio_ctrl` target and checker ignored `fb_clk`. New gold updates control from measured feedback/reference period; checker requires `vout/fb_clk` divider relation and `fb_clk/ref_clk` tracking. |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | Accept | Gold uses `fb_clk`, phase error, PI-like integrator, `vctrl_mon`, timer DCO, and divider. Checker verifies late reference/feedback frequency tracking, lock reacquisition, and bounded control. |
| `vbr1_l2_pipeline_adc_chain` | Accept | Gold exposes stage residues and stage bits. Checker verifies residue-stage consistency, final code concatenation, code coverage, and monotonicity. |
| `vbr1_l2_weighted_sar_adc_dac_loop` | Accept with scope note | Gold composes S/H, SAR quantizer, and weighted DAC reconstruction. Checker ties sampled input, SAR code, DAC output, and monotonicity. It is a behavioral one-clock SAR conversion, not a bit-cycle controller claim. |
| `vbr1_l2_converter_static_linearity_measurement_flow` | Accept | Checker requires code coverage, monotonic reconstruction, nonuniform DNL visibility, and DNL/INL metric consistency with reconstructed levels. |
| `vbr1_l2_flash_adc_mini_array` | Accept | Checker requires all flash codes, threshold-ladder behavior, thermometer-prefix comparator outputs, and binary code matching comparator count. |
| `vbr1_l2_comparator_measurement_flow` | Accept | Checker verifies comparator trip, valid latch timing, trip voltage, offset estimate, and held measurement outputs. |
| `vbr1_l2_converter_front_end` | Accept | Checker covers aperture-delayed sampling, droop, coarse decision, and valid pulses. |
| `vbr1_l2_amplifier_filter_chain` | Accept | Checker distinguishes preamplified metric from lagged filtered output and verifies settling/fall behavior. |
| `vbr1_l2_complete_calibration_loop` | Strengthened in this pass | Gold now exposes `trim_mon` and `residual_mon`; checker requires trim to move opposite the raw error and residual to be reduced after update, in addition to output correction and convergence metric. |
| `vbr1_l2_ldo_load_step_recovery_flow` | Strengthened with scope note | Gold now exposes `load_mon` and abstract `ctrl_mon`; checker requires load monitor tracking and control response across heavy/light load steps. Do not claim transistor/pass-device LDO behavior; this remains a voltage-domain behavioral recovery macro. |
| `vbr1_l2_reference_startup_enable_flow` | Accept | Macro startup/enable flow, not a closed-loop claim. Checker covers supply-off, pre-enable hold, startup settle, supply-dip reset, and recovery metric. |
| `vbr1_l2_agc_receiver_leveling_loop` | Strengthened in this pass | Gold now exposes `gain_mon` and `rssi_mon`; checker requires RSSI to rise on overload and gain monitor to decrease before leveled output and lock metric pass. |
| `vbr1_l2_iq_downconversion_chain` | Accept | Chain task, not loop task. Checker verifies quadrature sequence, distinct I/Q outputs, and common-mode hold. |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | Support category | Treat as measurement-support evidence, not a core circuit-function claim. |
| `vbr1_l2_measurement_flow` | Support category | Treat as instrumentation/support, not a core analog block claim. |
| `vbr1_l2_programmable_stimulus_sequencer` | Support category | Treat as stimulus-support, not a core analog block claim. |

## Follow-Up Rule

For future L2 rows, require at least one public checker relation that couples
intermediate observables to the claimed flow:

- loop rows: control/feedback observable must affect output or lock;
- chain rows: downstream output must be checked against upstream intermediate;
- measurement rows: reported metric must be checked against the measured signal;
- support rows: keep them outside core circuit-function claims.
