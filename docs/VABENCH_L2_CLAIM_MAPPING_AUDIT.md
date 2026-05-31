# vaBench L2 Claim Mapping Audit

Date: 2026-05-25

This table is the working review surface for the 17 current L2 entries in
`benchmark-vabench-release-v1`. The purpose is to decide what each L2 row is
allowed to claim in the paper-facing benchmark:

- `core`: contributes to the 66-entry analog/mixed-signal circuit-function
  denominator.
- `support`: contributes to measurement, testbench, or stimulus Verilog-A
  support coverage, but must not inflate the core circuit count.
- `keep`: current prompt/checker/gold shape is conceptually acceptable, subject
  to fresh EVAS/Spectre certification.
- `revise`: concept is useful, but prompt/checker/gold needs tightening before
  a strong claim.
- `downgrade`: should not be treated as L2 unless redesigned.

Current EVAS/Spectre dual validation is complete for these rows; future edits
to prompt/checker/gold still require rerun before refreshed claims.

## L2 Background Conditions

A core L2 row is allowed to count as a circuit-function benchmark row only when
it satisfies all of these conditions:

1. It represents a composed behavioral circuit flow, measurement flow, or
   closed-loop update rather than a single shallow transfer function.
2. Its public prompt exposes the observables needed to see intermediate state,
   multi-stage behavior, or loop response.
3. Its checker validates at least one intermediate relation in addition to the
   final output value.
4. Its paper wording stays inside voltage-domain/event-driven behavioral
   Verilog-A. It must not imply transistor-level devices, layout, current-domain
   regulation, RF S-parameters, noise analysis, PSRR, jitter/noise performance,
   or full silicon implementation unless those are explicitly modeled and
   checked.

A support L2 row can still be valuable benchmark content, but it is reported as
measurement/stimulus infrastructure and is excluded from the core circuit score.

Prompt-only wording changes refresh the public task contract but do not change
the certified gold behavior. Checker, gold, or testbench behavior edits require
fresh EVAS/Spectre dual validation before refreshed certification claims.

## P0 L2 Review Table

| Entry | Role | Intended L2 claim | Composition or support evidence | Public/checker observables | Current decision | Fresh validation needed | Risk / reviewer note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l2_converter_static_linearity_measurement_flow` | core | Static-linearity measurement flow for a 4-bit converter pair. | Quantizes a ramp, reconstructs a deliberately nonideal DAC voltage, and derives DNL/INL-like metrics from code/reconstruction history. | `clk`, `rst`, `vin`, `code`, `recon`, `dnl`, `inl`; checks code coverage, monotonic reconstruction, nonuniform DNL, INL consistency, and DNL step-error consistency. | keep | no for current certified package; rerun after checker/gold behavior edits | Strong enough as a lightweight static-linearity flow. It should not be described as a full industrial histogram DNL/INL tester. |
| `vbr1_l2_flash_adc_mini_array` | core | Flash ADC mini-array. | Seven explicit comparator observables plus encoder output. | `vin`, `clk`, `cmp0..cmp6`, `dout0..dout2`; checks all 8 codes, threshold ladder, thermometer prefix, and binary count match. | keep | no for current certified package; rerun after checker/gold behavior edits | Good architectural distinction from a single comparator. Confirm prompt keeps comparator array visible without leaking implementation. |
| `vbr1_l2_pipeline_adc_chain` | core | Compact two-stage pipeline ADC residue chain. | Stage-1 decision, residue generation, stage-2 decision, and final code concatenation for the same sampled input. | `vin`, `clk`, `res1`, `res2`, `s1b*`, `s2b*`, `dout*`; checker verifies all 16 codes, stage decisions, residue values, final concatenation, monotonicity, and bounded residues. | keep | no for current certified package; rerun after checker/gold behavior edits | This is materially L2, but remains a compact single-sample behavioral pipeline rather than a full latency/redundancy/correction ADC. Paper wording should say "pipeline ADC residue chain", not full converter macro. |
| `vbr1_l2_weighted_sar_adc_dac_loop` | core | Weighted SAR ADC/DAC round-trip loop. | Sample/hold, MSB-first weighted SAR final-code decision, and weighted DAC reconstruction path are packaged together. | `vin`, `vin_sh`, `clks`, `vout`, `rst_n`, `dout_0..dout_7`; checker verifies code coverage, endpoint range, sampled-input/code consistency, code/DAC consistency, sampled-input monotonicity, and output bounds. | keep | no for current certified package; rerun after checker/gold behavior edits | Strong enough as a compact weighted SAR transfer loop. It should not be described as a full multi-cycle SAR controller with observable per-bit trials. |
| `vbr1_l2_comparator_measurement_flow` | core | Single-ramp comparator offset measurement flow. | Comparator decision plus measurement latches for trip voltage, offset estimate, and valid status during a controlled ramp. | `inp`, `inn`, `outp`, `trip_v`, `offset_est`, `valid`; checks low-before-trip, high-after-trip, first output/valid trip near the static offset, trip near `inn+offset`, offset estimate, and held measurement outputs. | keep | no for current certified package; rerun after checker/gold behavior edits | Strong L2 measurement flow for comparator characterization; appropriate as a common offset-measurement method. |
| `vbr1_l2_converter_front_end` | core | Converter front-end with aperture, hold, droop, coarse decision, and valid marking. | Aperture-delayed sample/hold behavior feeds a coarse decision and public valid pulse. | `clk`, `vin`, `vout`, `coarse`, `valid`; checks delayed sample tracking, bounded droop, decision from held sample, and valid timing. | keep | no for current certified package; rerun after checker/gold behavior edits | Useful mixed-signal front-end row. Confirm prompt does not overclaim it as a full ADC. |
| `vbr1_l2_amplifier_filter_chain` | core | Amplifier/filter signal-conditioning chain. | Amplifier target metric and lagged/bounded filtered output are both observable. | `clk`, `rst`, `vin`, `out`, `metric`; checks target metric, output lag, bounded range, mid/common-mode behavior, and falling response. | keep | no for current certified package; rerun after checker/gold behavior edits | Conceptually valid, but small. Keep as compact chain and avoid claiming high-order filter design coverage. |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | core | ADPLL lock, ratio-hop, and timer-driven DCO flow. | Reference clock, programmable ratio control, timer-driven oscillator output, feedback/lock behavior. | `ref_clk`, `ratio_ctrl`, `vout`, `fb_clk`, `vctrl_mon`, `lock`; checks pre-hop ratio, post-hop ratio, lock reacquisition, and bounded control. | keep | no for current certified package; rerun after checker/gold behavior edits | Strong enough for voltage-domain timing/control behavior. It is not a transistor-level PLL or jitter/noise benchmark. |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | core | CPPLL-style tracking and frequency-step reacquire flow. | Reference-step source plus loop output, feedback clock, control monitor, and lock indicator. | `ref_clk`, `fb_clk`, `dco_clk`, `vctrl_mon`, `lock`; checks pre-lock, disturbance lock drop, post-step relock, late tracking, and bounded control. | keep | no for current certified package; rerun after checker/gold behavior edits | Strong timing-flow row within voltage-domain abstraction. Paper wording must avoid current-domain charge-pump/KCL claims. |
| `vbr1_l2_complete_calibration_loop` | core | Closed calibration loop. | Error input drives controller/actuator trim output toward target. | `clk`, `rst`, `vin` or `err`, `out`, `metric`; checks reset, output span, signed movement with error, actuator direction, and convergence tendency. | keep | no for current certified package; rerun after checker/gold behavior edits | Good L2 calibration/control row. Check if `metric` is actually part of the public claim or only auxiliary. |
| `vbr1_l2_reference_startup_enable_flow` | core | Reference startup/enable flow. | Enable and supply/ramp behavior drive a reference macromodel plus valid/reset-style observable state. | Reference/output, enable or supply stimulus, valid/status metric; checks startup threshold, monotonic startup trend, valid assertion, and no stuck rail-only output. | keep | no | Strong enough as a compact reference/power-state flow; avoid overclaiming bandgap device physics. |
| `vbr1_l2_ldo_load_step_recovery_flow` | core | LDO load-step recovery flow. | Regulator macromodel responds to load-step stimulus with bounded droop and recovery behavior. | Regulated output, load step or load monitor, recovery/status metric; checks pre-step regulation, droop direction, recovery window, and bounded steady-state error. | keep | no | Appropriate L2 power-management transient row; do not claim transistor-level loop stability or PSRR. |
| `vbr1_l2_iq_downconversion_chain` | core | I/Q downconversion chain. | RF/mixer behavior produces quadrature baseband observables under LO scheduling. | `clk`, `rst`, `vin`, `out`, `metric`; `out` is the I-path baseband observable and `metric` is the Q-path observable. Checker validates the scheduled quadrature polarity and common-mode hold. | keep with constrained wording | no for current certified package; rerun after checker/gold behavior edits | Weakest core L2 because LO phase is implicit in the clocked schedule rather than a saved phase column. Keep only as a compact voltage-domain I/Q downconversion schedule macro, not a full RF receiver or S-parameter task. |
| `vbr1_l2_agc_receiver_leveling_loop` | core | AGC receiver leveling loop. | Front-end gain/compression behavior interacts with gain-control update toward target output level. | `clk`, `rst`, `vin`, `out`, `metric`; checker validates overload reduction, settled amplitude, and lock metric. | keep with constrained wording | no for current certified package; rerun after checker/gold behavior edits | Valid compact AFE/control flow, but gain control is internal rather than a saved column. Stronger future version could expose `gain_ctrl`; current paper wording should avoid detailed RF noise or loop-stability claims. |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | support | Gain extraction/convergence measurement support flow. | Dithered source path, LFSR/dither adder, fixed gain amplifier, and measurement by waveform statistics. | `vinp`, `vinn`, `vamp_p`, `vamp_n`; checker verifies gain amplification and differential gain threshold. | support-only | no for current certified package; rerun after checker/gold behavior edits | Useful as support/instrumentation, but should not count as a core amplifier benchmark because the measured circuit role overlaps CT04. |
| `vbr1_l2_measurement_flow` | support | Final-step/file-metric measurement flow. | Event counting plus final-step metric waveform/file side effect. | `ref`, `metric_out`, `candidate.out`; checks expected edge count grid, normalized final metric, and final-step file write. | support-only | no for current certified package; rerun after checker/gold behavior edits | Good support row if file metric is publicly specified. Not a core circuit function. |
| `vbr1_l2_programmable_stimulus_sequencer` | support | Programmable stimulus sequencer: ramp, swept/chirp sine, and gated burst/PRBS schedule. | Mode/gate-controlled waveform scheduler with observable output and metric. | `clk`, `rst`, `mode`, `gate`, `out`, `metric`; checks ramp monotonicity, increasing chirp frequency, burst/PRBS gate schedule, mode-switch continuity, and mode metric. | support-only | no for current certified package; rerun after checker/gold behavior edits | This is valuable Verilog-A stimulus infrastructure, but taxonomy/report/paper wording must keep it separate from core circuit-function coverage. |

## Immediate Reviewer Questions

Use these questions while reading each L2 prompt/gold/checker pair:

1. Can the claimed L2 behavior be explained as interaction between at least two
   meaningful blocks or as an explicit support flow?
2. Does the public prompt expose the same observables the checker relies on?
3. Could a wrong implementation pass by producing only a shallow final value?
4. Does the gold implementation match the public function name?
5. Is the row allowed to support a core circuit claim, or only a support
   measurement/stimulus claim?

## First-Round Decisions

Current P0 status:

- 14 core L2 entries: 12 `keep` and 2 `keep with constrained wording`
  (`vbr1_l2_agc_receiver_leveling_loop`,
  `vbr1_l2_iq_downconversion_chain`).
- `support-only`: 3 entries.
- `revise`: 0 entries.
- `downgrade`: 0 entries.

The SAR row is kept after tightening because the public prompt and checker now
match the intended compact claim: sampled input maps to the final weighted SAR
code, the code maps to the weighted DAC output, and the code is monotonic with
the sampled input. It still must not be claimed as a full multi-cycle SAR
controller with observable per-bit trial timing.
