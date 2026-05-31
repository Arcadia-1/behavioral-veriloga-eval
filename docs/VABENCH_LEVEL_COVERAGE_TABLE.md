# vaBench Category and Level Coverage Table

Date: 2026-05-24

This table is the current human-review view of the 79-entry vaBench release
after the weak/duplicate entry rebalance and the later bias/reference/power and
RF/AFE expansion. It is a coverage and taxonomy view; certification evidence
is maintained in the release reports.

## Selection Principle

The release set is chosen for analog/mixed-signal circuit-function coverage,
not only for simulation-speed relevance. A valid entry should be recognizable
as a real behavioral IC block, macro helper, measurement/testbench function,
source model, or composed mixed-signal flow. EVAS support constrains the
implementation subset and certification path, but it should not be the only
reason a function exists in the benchmark.

## Count Vocabulary

| Term | Count | Meaning |
| --- | ---: | --- |
| Current promoted L1 seeds | 22 | Current-seed L1 functions retained in the release package after duplicate/removal policy. |
| Promoted top-level L1 additions | 40 | Additional L1 functions selected as release coverage targets. |
| Selected L2 complete-circuit targets | 17 | System/flow targets that compose multiple L1 functions. |
| Top-level L1/L2 coverage target | 79 | 62 L1 + 17 L2 entries, before task-form multiplication. |
| Release task forms | 271 | Materialized `dut`, `tb`, `bugfix`, and/or `e2e` forms. |
| Core score denominator | 66 entries / 236 forms | Enabled for certified `track=core` rows; support rows are reported separately. |
| Support suite | 13 entries / 35 forms | Measurement/stimulus coverage excluded from the core circuit score. |
| Difficulty split | D1=7, D2=54, D3=18 | Difficulty is orthogonal to L1/L2 and core/support. |

The 79-entry target intentionally contains two roles: 66 core circuit entries
under converter, comparator, PLL/timing, calibration/control, signal
conditioning, sample/hold, bias/reference/power, and RF/AFE categories; and 13
support entries under measurement/testbench instrumentation plus
stimulus/sources. Support entries are valid benchmark content after
certification, but paper tables must not mix them into the core analog
circuit-function score denominator.

## L0 / L1 / L2 Rules

| Level | What it means | Current use | Counted in benchmark score |
| --- | --- | --- | --- |
| L0 conformance | Single-cause Verilog-A, simulator, source, event, sampling, or checker semantic. | EVAS/Spectre health and regression tests. | No. |
| L1 function | One reusable analog/mixed-signal behavioral circuit function with measurable behavior. | Main model-capability surface after certification. | Yes for `track=core`; support rows report separately. |
| L2 complete circuit | Multiple interacting L1 functions or a complete mixed-signal flow. | Higher-level benchmark expansions and true system e2e tasks. | Yes for `track=core`; support rows report separately. |

## Category Coverage

| Category | Entries | L1 | L2 | Core/support role |
| --- | ---: | ---: | ---: | --- |
| Data Converter Models | 13 | 9 | 4 | Core converter coverage. |
| Comparator and Decision Circuits | 8 | 7 | 1 | Core decision-block coverage. |
| PLL Clock and Timing Systems | 10 | 8 | 2 | Core event/timing mixed-signal coverage. |
| Calibration, DEM, and Control | 7 | 6 | 1 | Core calibration/control coverage after DEM deduplication. |
| Baseband Signal Conditioning | 8 | 7 | 1 | Core voltage-domain transform coverage. |
| Sampling and Analog Memory | 5 | 4 | 1 | Core sampled analog memory/front-end coverage. |
| Bias Reference and Power Management | 8 | 6 | 2 | Core bias, reference, reset, regulator, and power-state macromodel coverage. |
| RF and AFE Behavioral Macromodels | 7 | 5 | 2 | Core voltage-domain RF/AFE macro behavior, not transistor-level RF physics. |
| Measurement Instrumentation Flows | 7 | 5 | 2 | Support coverage for reusable measurement contracts. |
| Stimulus and Source Generators | 6 | 5 | 1 | Support coverage for reusable stimulus/source models. |

## L1 Function Coverage

| Category | L1 functions |
| --- | --- |
| Data Converter Models | Simple 4-bit binary-coded DAC; unit-element thermometer DAC; segmented DAC; thermometer-code decoder; clocked ADC quantizer; capacitive/weighted SAR feedback DAC; DAC mismatch/unit-weighting model; SAR logic; pipeline ADC MDAC stage. |
| Comparator and Decision Circuits | Threshold comparator; propagation-delay comparator; hysteresis comparator; window comparator/detector; offset comparator; StrongARM-style latch comparator; comparator debounce latch. |
| PLL Clock and Timing Systems | VCO phase integrator; PFD UP/DN logic; bang-bang phase detector; digital phase accumulator with modulo wrap; clock divider; lock detector; voltage-domain charge-pump control abstraction; sampled loop-filter abstraction. |
| Calibration, DEM, and Control | Trim-voltage generator; gain trim controller; DWA/DEM encoder; calibration deadband controller; successive-approximation calibration/search FSM; element shuffler. |
| Baseband Signal Conditioning | First-order lowpass; resettable integrator; soft/hysteretic limiter; precision rectifier/envelope detector; higher-order filter; slew-rate limiter; programmable gain amplifier. |
| Sampling and Analog Memory | Aperture-delay track-and-hold; sample-and-hold with droop/leakage; clocked sample-and-hold; acquisition-limited sample-and-hold. |
| Bias Reference and Power Management | Bandgap reference macromodel; PTAT/CTAT reference generator; bias voltage generator with enable and trim; LDO regulator macromodel; UVLO/brownout detector; power-on reset detector. |
| RF and AFE Behavioral Macromodels | LNA gain-compression macromodel; RF mixer/downconverter macromodel; limiting amplifier front-end; log/RSSI power detector; PA compression macromodel. |
| Measurement Instrumentation Flows | Crossing metric writer; settling response measurement helper; peak detector; gain estimator; edge interval timer. |
| Stimulus and Source Generators | PRBS stimulus/dither generator; periodic phase-ramp guard source; burst clock source; dither or noise-like deterministic source; sine/periodic voltage source. |

## L2 Target Coverage

| Category | L2 target | Required components |
| --- | --- | --- |
| Data Converter Models | Converter static linearity measurement flow | Converter core plus lightweight meter covering ramp code coverage, monotonic reconstruction, visible step nonuniformity, and DNL/INL-like metrics derived from code/reconstruction history. |
| Data Converter Models | Weighted SAR ADC/DAC loop | SAR controller + weighted feedback DAC + comparator interaction. |
| Data Converter Models | Flash ADC mini-array | Multiple threshold comparators + thermometer/code output behavior. |
| Data Converter Models | Pipeline ADC residue chain | Two behavioral converter stages with exposed coarse decision, residue generation, backend decision, and final-code concatenation for one sampled input. |
| Comparator and Decision Circuits | Single-ramp comparator offset measurement flow | Ramp stimulus + comparator + input-referred offset measurement. |
| PLL Clock and Timing Systems | ADPLL lock/ratio-hop/timer flow | Digital phase/timer control + divider/VCO timing response. |
| PLL Clock and Timing Systems | CPPLL tracking and frequency-step reacquire flow | PFD + voltage-domain charge-pump/filter abstraction + VCO response to a frequency step. |
| Calibration, DEM, and Control | Complete calibration loop | Error source + controller + trim/actuator + convergence metric. |
| Baseband Signal Conditioning | Amplifier/filter chain | Gain or driver stage + filter/limiter + measured response. |
| Sampling and Analog Memory | Converter front-end | Sampling front-end + quantizer or comparator interaction. |
| Bias Reference and Power Management | Reference startup/enable flow | Enable/ramp behavior + reference startup + valid/reset-style observable state. |
| Bias Reference and Power Management | LDO load-step recovery flow | Regulator macromodel + load-step transient + recovery metric. |
| RF and AFE Behavioral Macromodels | I/Q downconversion chain | Mixer/downconversion behavior plus quadrature baseband observables. |
| RF and AFE Behavioral Macromodels | AGC receiver leveling loop | Gain-compression/front-end behavior plus gain-control convergence. |
| Measurement Instrumentation Flows | Measurement flow | Stimulus + DUT + metric artifact + checker. |
| Measurement Instrumentation Flows | Gain extraction/convergence measurement flow | Stimulus + gain estimator + convergence or trim metric artifact. |
| Stimulus and Source Generators | Programmable stimulus sequencer | Ramp, swept/chirp sine, and gated burst/PRBS schedule with mode-switch continuity checks; support/stimulus L2 reported separately from core circuit flows. |

## Rebalance Decisions

The release rebalance removed 10 weak or duplicate rows:
`vbr1_l1_adc_code_capture_register`,
`vbr1_l1_serializer_frame_aligner`,
`vbr1_l1_serial_readout_deserializer`,
`vbr1_l2_serializer_frame_alignment_flow`,
`vbr1_l2_event_controller`,
`vbr1_l1_pfd_small_phase_error_response`,
`vbr1_l1_xor_phase_detector`,
`vbr1_l2_pll_timing_slice`,
`vbr1_l1_rotating_dem_selector`, and
`vbr1_l1_windowed_dem_pointer`.

It then added stronger analog coverage, including:
`vbr1_l1_acquisition_limited_sample_and_hold` and
`vbr1_l1_programmable_gain_amplifier`, plus the CT07 bias/reference/power and
CT08 RF/AFE macromodel categories.
