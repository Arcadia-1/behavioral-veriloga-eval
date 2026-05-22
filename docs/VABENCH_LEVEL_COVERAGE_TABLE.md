# vaBench Category and Level Coverage Table

Date: 2026-05-15

This table is the current human-review view of the clean vaBench taxonomy after
the calibration merge and offset-calibration deletion decisions.

Counting decisions:

- `background_calibration_accumulator` is fully merged into
  `cdac_calibration` and is not counted separately.
- `offset_calibration_fsm` is removed from the release count for now.
- `thermometer_dac` remains trace evidence only after it is renamed as a simple
  4-bit binary-coded DAC.
- Current main120 e2e forms are treated as L1-form unless the task composes
  multiple interacting functions.

Coverage-count vocabulary:

| Term | Count | Meaning |
| --- | ---: | --- |
| Current promoted L1 seeds | 28 | Countable L1 functions inherited from current main120 after duplicate/removal policy. |
| Promoted top-level L1 additions | 32 | Additional L1 functions selected from examples, smoke tasks, and historical validated drafts as release coverage targets. They still require task materialization and certification before scoring. |
| Selected L2 complete-circuit targets | 15 | System/flow targets that compose multiple L1 functions after removing duplicate kernels. They still require task materialization and certification before scoring. |
| Top-level L1/L2 coverage target | 75 | 28 current L1 seeds + 32 promoted L1 additions + 15 L2 targets, before task-form multiplication. |
| Excluded historical bases | 2 | `background_calibration_accumulator` is merged; `offset_calibration_fsm` is removed pending redesign. |

So "28 seeds" means current promoted seed functions only. The top-level release
coverage target is larger: 28 current L1 seeds plus 32 promoted L1 additions
plus 15 L2 complete-circuit targets.

## L0 / L1 / L2 Rules

| Level | What it means | Current use | Counted in benchmark score |
| --- | --- | --- | --- |
| L0 conformance | Single-cause Verilog-A, simulator, source, event, sampling, or checker semantic. | EVAS/Spectre health and regression tests. | No. |
| L1 function | One reusable circuit function with a module contract and measurable behavior. | Main scored model-capability surface. | Yes. |
| L2 complete circuit | Multiple interacting L1 functions or a complete mixed-signal flow. | Higher-level benchmark expansions and true system e2e tasks. | Yes. |

## Complete Category Table

| Category | L0 conformance themes | Current L1 concrete circuits | Promoted L1 additions from examples/history | L2 complete-circuit targets |
| --- | --- | --- | --- | --- |
| Data Converters | Bus width guards; code saturation; decoder monotonicity; transition timing. | Simple 4-bit binary-coded DAC; segmented DAC; guarded thermometer-code decoder; 4-bit SAR logic. | Clocked ADC quantizer; unit-element thermometer DAC; capacitive/weighted SAR feedback DAC; DAC mismatch/unit-weighting model. | ADC/DAC reconstruction chain; weighted SAR ADC/DAC loop; flash ADC mini-array. |
| Comparators and Decision Circuits | `cross()` threshold touch; clock/reset ordering; output transition placement. | Offset comparator; StrongARM-style latch comparator behavior. | Ideal threshold comparator; propagation-delay comparator; hysteresis comparator; window comparator/detector. | Comparator measurement flow: stimulus + comparator + offset/delay/hysteresis metric. |
| PLL / Clock / Event Timing | `timer()` startup semantics; coincident events; `$abstime` sampling; divider edge ordering. | VCO phase integrator; PFD UP/DN reset-race behavior; resettable clock divider; lock detector. | PFD UP/DN core; PFD small phase-error response; XOR phase detector; bang-bang phase detector; digital phase accumulator with modulo wrap; voltage-domain charge-pump control abstraction; sampled loop-filter abstraction. | PLL timing slice; ADPLL lock/ratio-hop/timer flow; CPPLL tracking and frequency-step reacquire flow. |
| Calibration, DEM, and Control | Update ordering at clock edges; clamp bounds; pointer wrap boundaries. | Trim-voltage generator; gain trim controller; rotating DEM selector; windowed DEM pointer; deterministic element shuffler. | DWA/DEM encoder; calibration deadband controller; successive-approximation calibration/search FSM. | Complete calibration loop. |
| Digital and Event-Driven Logic | Empty branch legality; event initialization; reset precedence; one-shot pulse scheduling. | Edge detector; debounce latch; one-shot timer. | LFSR/PRBS generator; serializer/frame aligner; retriggerable one-shot pulse stretcher. | Event controller; serializer frame-alignment flow. |
| Measurement and Testbench Instrumentation | File I/O parsing; final-row sampling; CSV metric schema; tolerance-window semantics. | Crossing metric writer; settling-time measurement testbench; peak detector. | Gain estimator; edge interval timer. | Measurement flow; gain extraction/convergence measurement flow. |
| Stimulus and Sources | PWL/source continuation legality; breakpoint insertion; source row sampling. | No current countable release seed after clamp/slew are mapped to signal conditioning. | Ramp/step source; burst-clock source; deterministic noise/dither source; sine/periodic voltage source. | ADC/DAC source sweep flow. |
| Analog Behavioral Signal Conditioning | Continuous update timestep; transition smoothing; saturation edge cases; resettable state. | First-order lowpass; resettable integrator; precision rectifier; voltage clamp/limiter; slew-rate limiter. | Soft/hysteretic limiter; voltage gain amplifier; differential output driver; higher-order filter. | Amplifier/filter chain. |
| Sample, Hold, and Analog Memory | Track/sample edge timing; aperture delay; leakage/decay timestep semantics. | Aperture-delay track-and-hold; sample-and-hold with droop/leakage. | Clocked sample-and-hold. | Converter front-end. |

Promoted additions in this table are part of the top-level release coverage
contract. They are still not automatically scored tasks: each one must receive
prompt, metadata, gold assets, checks, and EVAS/Spectre certification before it
can enter a release package.

## Expansion Source Trace

| Source | Functions and variants extracted for promotion review |
| --- | --- |
| `veriloga-skills/evas-sim/examples/data-converter` | Ideal clocked ADC; ideal binary-weighted DAC; trim-code decoder for binary/one-hot/thermometer outputs; register-loaded binary-weighted DAC; unit-element thermometer DAC; capacitive/weighted DAC; weighted SAR ADC loop. |
| `veriloga-skills/evas-sim/examples/comparator` | Ideal threshold comparator; propagation-delay comparator; offset-search comparator; StrongARM-style latch comparator; edge interval timer. |
| `veriloga-skills/evas-sim/examples/digital-logic` | Clock divider; basic gates; DFF with reset; LFSR. |
| `veriloga-skills/evas-sim/examples/calibration` | DWA pointer generator; no-overlap pointer; wraparound-related DEM pointer behavior. |
| `veriloga-skills/evas-sim/examples/stimulus` | Ramp generator; burst-clock generator; deterministic noise generator. |
| `veriloga-skills/evas-sim/examples/measurement` | Gain estimator; gain calibration controller; gain extraction/convergence flow; dither source; differential SAR ADC helper. |
| Historical `benchmark-balanced` | Threshold detector; window detector; analog limiter; retriggerable pulse-stretcher seed. |
| Historical `benchmark-v2` | ADC/DAC shared quantized state; binary-weighted DAC versus thermometer/unit-cell distractors; DWA pointer perturbations; PFD/lock-window behavior; divider/counter ratio and encoding distractors; sample/hold plus calibration/system composition. |
| Existing smoke tasks under `tasks/end-to-end/voltage` | Flash ADC; ADPLL lock/ratio-hop/timer; CPPLL tracking/reacquire; PFD UP/DN/small-phase-error; gray counter; serializer; mux; comparator hysteresis; sample-hold droop; phase accumulator wrap. |

## Current L1 Seed List

| Category | Countable current L1 seeds |
| --- | --- |
| Data Converters | `simple_binary_voltage_dac_4b` as simple 4-bit binary-coded DAC after rename; `segmented_dac`; `thermometer_decoder_guarded`; `sar_logic_4b`. |
| Comparators and Decision Circuits | `offset_comparator`; `strongarm_comparator_behavior` as StrongARM-style latch behavior. |
| PLL / Clock / Event Timing | `vco_phase_integrator`; `pfd_reset_race` as PFD UP/DN reset-race behavior; `resettable_counter_divider`; `lock_detector`. |
| Calibration, DEM, and Control | `cdac_calibration`; `gain_trim_controller`; `rotating_element_selector`; `barrel_pointer_window`; `element_shuffler`. |
| Digital and Event-Driven Logic | `edge_detector`; `debounce_latch`; `one_shot_timer`. |
| Measurement and Testbench Instrumentation | `file_metric_writer`; `settling_time_measurement_tb`; `peak_detector`. |
| Stimulus and Sources | None currently counted after remapping clamp/slew to signal conditioning. |
| Analog Behavioral Signal Conditioning | `first_order_lowpass`; `resettable_integrator`; `precision_rectifier`; `voltage_clamp`; `slew_rate_limiter`. |
| Sample, Hold, and Analog Memory | `track_hold_aperture`; `leaky_hold` as sample-and-hold droop/leakage behavior. |

Current promoted countable L1 seeds: 28.

Excluded current historical bases:

| Base | Reason |
| --- | --- |
| `background_calibration_accumulator` | Fully merged into `cdac_calibration`; same signed trim-control kernel. |
| `offset_calibration_fsm` | Removed until redesigned as a true multi-state offset-search controller. |

## L0 Conformance Table

| L0 family | Concrete conformance cases to maintain |
| --- | --- |
| Syntax legality | Empty control branch; illegal or ambiguous module/source continuation; Spectre-rejected syntax that EVAS must reject. |
| Source parsing | Uncontinued PWL/source lines; breakpoint creation for source changes; source value row sampling. |
| Event scheduling | `cross()` threshold touch; coincident `cross()` and `timer()` events; reset-before-update ordering. |
| Sampling and timestep semantics | `$abstime` decay behavior; `timer(0)` startup sample; final-row value exclusion where it is simulator-artifact-sensitive. |
| Checker and artifact semantics | `metric.out` one-line parsing; waveform/metric consistency; CSV header and tolerance-window checks. |

## L2 Target Table

| Category | L2 target | Required components |
| --- | --- | --- |
| Data Converters | ADC/DAC reconstruction chain | ADC quantizer + DAC reconstruction + source/checker flow. |
| Data Converters | Weighted SAR ADC/DAC loop | SAR controller + weighted feedback DAC + comparator interaction. |
| Data Converters | Flash ADC mini-array | Multiple threshold comparators + thermometer/code output behavior. |
| Comparators and Decision Circuits | Comparator measurement flow | Stimulus + comparator + offset/delay measurement. |
| PLL / Clock / Event Timing | PLL timing slice | PFD + divider + VCO or loop-control interaction. |
| PLL / Clock / Event Timing | ADPLL lock/ratio-hop/timer flow | Digital phase/timer control + divider/VCO timing response. |
| PLL / Clock / Event Timing | CPPLL tracking and frequency-step reacquire flow | PFD + voltage-domain charge-pump/filter abstraction + VCO response to a frequency step. |
| Calibration, DEM, and Control | Complete calibration loop | Error source + controller + trim/actuator + convergence metric. |
| Digital and Event-Driven Logic | Event controller | Event inputs + state machine + timed outputs. |
| Digital and Event-Driven Logic | Serializer frame-alignment flow | Serializer + framing stimulus + alignment/error checker. |
| Measurement and Testbench Instrumentation | Measurement flow | Stimulus + DUT + metric artifact + checker. |
| Measurement and Testbench Instrumentation | Gain extraction/convergence measurement flow | Stimulus + gain estimator + convergence or trim metric artifact. |
| Stimulus and Sources | ADC/DAC source sweep flow | Source model + converter response + checker. |
| Analog Behavioral Signal Conditioning | Amplifier/filter chain | Gain or driver stage + filter/limiter + measured response. |
| Sample, Hold, and Analog Memory | Converter front-end | Sampling front-end + quantizer or comparator interaction. |
