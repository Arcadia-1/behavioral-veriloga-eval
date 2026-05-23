# vaBench Release Taxonomy

Date: 2026-05-15

This is the clean release-facing taxonomy for vaBench. It is the benchmark
coverage contract, not a report of how earlier experimental rows happened to be
generated.

The scored benchmark surface is L1/L2 behavioral circuit work. L0
EVAS/Spectre conformance cases are maintained separately because they validate
evaluator semantics rather than model capability on a circuit task.

## Level Rules

| Level | Meaning | Counted in vaBench score |
| --- | --- | --- |
| L0 conformance | Single-cause Verilog-A, simulator, event, source, or checker semantic. | No; report separately as EVAS/Spectre health. |
| L1 function | One reusable circuit function with a clear module contract and measurable behavior. | Yes. |
| L2 complete circuit | A composed circuit form with multiple interacting L1 functions or a complete mixed-signal flow. | Yes. |

Task form is orthogonal to level. A task may be `dut`, `tb`, `bugfix`, or
`e2e`; an `e2e` task counts as L2 only when it genuinely composes multiple
interacting functions.

## Certification Contract

Every released scored task must provide:

| Field | Requirement |
| --- | --- |
| Public prompt | Names behavior, ports, artifacts, and observables without leaking gold implementation. |
| Metadata | Includes release category, level, task form, source files, expected backend, and provenance. |
| Checker | Deterministic public validation contract tied to the prompt. |
| Gold assets | Gold Verilog-A and reference testbench or source artifacts. |
| Evidence | Static integrity, EVAS gold validation, and Spectre gold validation links. |

## Function-Level Checker Contract

Each L1/L2 function must define the circuit behavior from a verification angle
before a checker is treated as benchmark-strength. Public checks should target
stable circuit observables, while EVAS/Spectre conformance quirks stay outside
the scored benchmark denominator.

| Category | Verification angle | Key observables | Minimum checker metrics |
| --- | --- | --- | --- |
| Data Converters | Does the code, unit selection, or quantizer threshold map to the intended analog/code output? | Input code bits or unary segments, reference rails, reconstructed output, output code bits. | Code coverage across representative levels, monotonicity, endpoint behavior, saturation/clamping, and rejection of missing MSB/unit segments. |
| Comparators and Decision Circuits | Does the decision block switch at the intended threshold, hysteresis window, clock phase, or delay? | Input differential/single-ended waveform, clock/reset, output decision waveform. | Correct polarity, threshold or hysteresis transitions, bounded delay or evaluate/reset windows, no stuck output. |
| PLL / Clock / Event Timing | Does the event relation produce the intended phase, pulse, divider, or frequency response? | REF/DIV/clock edges, UP/DN pulses, phase state, divider output, VCO/lock signals. | Edge counts, pulse direction and overlap bounds, phase/frequency trend, wrap behavior, and late-window behavior rather than startup artifacts. |
| Calibration, DEM, and Control | Does the controller update state in the correct signed direction while respecting bounds and sequence rules? | Error inputs, trim/control state, selector or pointer outputs, actuator response. | Signed movement outside deadband, hold inside deadband, clamp behavior, wrap/rotation correctness, and convergence or monotonic improvement when specified. |
| Measurement and Testbench Instrumentation | Does the generated measurement match the waveform quantity it claims to report? | Waveform columns, metric files, crossing/settling/peak/gain outputs. | Numeric metric-to-waveform agreement, one-record artifact format where required, tolerance-window semantics, and no final-row or missing-file artifact passing. |
| Stimulus and Sources | Does the source generate the specified waveform schedule or deterministic sequence? | Source output waveform, clock/burst edges, seed/state when present. | Amplitude/range, timing, burst count, periodicity or deterministic variation, and reproducibility. |
| Analog Behavioral Signal Conditioning | Does the analog transform implement the intended gain, filter, limiting, integration, or slew behavior? | Input/output waveforms, reset/control signals, metric outputs when present. | Gain/slope/lag estimates, bounded output, state/reset behavior, limiting/slew constraints, and representative transient response. |
| Sample, Hold, and Analog Memory | Does the sampled value, held value, droop/leakage, or aperture timing match the contract? | Input waveform, sampling clock, held output, reset when present. | Sample instant alignment, hold stability, droop/leakage slope, aperture delay, and rejection of transparent-through behavior. |

## Coverage Counts

| Pool | Count | Score status |
| --- | ---: | --- |
| Current promoted L1 seeds | 24 | Scored only after release-package certification. |
| Promoted top-level L1 additions | 32 | Main-table coverage targets; not scored until materialized and certified. |
| Selected L2 package targets | 16 | Main-table complete-circuit targets after removing duplicate kernels. |
| Top-level L1/L2 package target | 72 | 56 L1 + 16 L2 rows; the former standalone control/readout bucket has been split into concrete circuit families. |

## Release Coverage Table

| Category | Base function | Level | Complete circuit form | Required task forms | Score surface | Release status | Certification status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Data Converters | Simple 4-bit binary-coded DAC | L1 | Code-to-voltage reconstruction block using a mathematical code/15 transfer model | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Data Converters | Unit-element thermometer DAC | L1 | 4-bit-equivalent 15-segment unary DAC with endpoint-scaled voltage output | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Data Converters | Segmented DAC | L1 | Coarse/fine or binary/thermometer segmented reconstruction | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Data Converters | Thermometer-code decoder | L1 | Guarded monotonic binary-to-thermometer decode | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Data Converters | Clocked ADC quantizer | L1 | Voltage-to-code conversion with saturation and sampled output behavior | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Data Converters | Capacitive/weighted SAR feedback DAC | L1 | Trial-code feedback DAC for SAR-style conversion loops | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Data Converters | DAC mismatch/unit-weighting model | L1 | Code-to-voltage reconstruction with explicit unit weight or mismatch terms | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Data Converters | SAR logic | L1 | Successive approximation state machine | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Data Converters | Pipeline ADC MDAC stage | L1 | Sample/hold residue generation stage with sub-ADC decision and feedback DAC subtraction | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Data Converters | ADC code capture register | L1 | Capture and hold conversion-result code plus overrange status at the readout boundary | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Data Converters | ADC/readout serializer frame aligner | L1 | Parallel ADC/readout word to serial stream with frame marker alignment | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Data Converters | Serial readout deserializer | L1 | Reconstruct framed serial conversion words into parallel readout data | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Data Converters | ADC/DAC reconstruction chain | L2 | ADC quantizer + DAC reconstruction + source/checker flow | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Data Converters | Weighted SAR ADC/DAC loop | L2 | SAR controller + weighted feedback DAC + comparator interaction | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Data Converters | Flash ADC mini-array | L2 | Multiple threshold comparators + thermometer/code output behavior | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Data Converters | Pipeline ADC chain | L2 | Two-stage pipeline conversion flow with residue amplification and final code composition | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Data Converters | Conversion event controller | L2 | Start/comparator-done inputs drive sample/compare/readout/done control phases | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Data Converters | Readout frame-monitor flow | L2 | Serializer + frame monitor reconstructs and validates loaded ADC/readout words | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Comparators and Decision Circuits | Threshold comparator | L1 | Voltage decision with bounded output transition | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Comparators and Decision Circuits | Propagation-delay comparator | L1 | Threshold decision with input-dependent or fixed output delay | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Comparators and Decision Circuits | Hysteresis comparator | L1 | Comparator with separate rising/falling thresholds and state memory | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Comparators and Decision Circuits | Window comparator/detector | L1 | In-window or out-of-window binary decision on analog input | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Comparators and Decision Circuits | Offset comparator | L1 | Comparator with explicit offset threshold | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Comparators and Decision Circuits | StrongARM-style latch comparator | L1 | Clocked latch-like comparator abstraction | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Comparators and Decision Circuits | Comparator debounce latch | L1 | Comparator decision latch with delayed glitch qualification and reset behavior | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Comparators and Decision Circuits | Single-ramp comparator offset measurement flow | L2 | Single-ramp stimulus + comparator + offset measurement result | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | VCO phase integrator | L1 | Voltage-controlled phase/frequency accumulation | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | PFD UP/DN logic | L1 | UP/DN event relation with reset-race handling | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | PFD small phase-error response | L1 | Small REF/DIV phase error produces bounded UP/DN pulses with overlap reset | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | XOR phase detector | L1 | Logic-level phase detector with duty/phase dependent output | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | Bang-bang phase detector | L1 | Early/late phase decision for clock-data or digital PLL loops | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | Digital phase accumulator with modulo wrap | L1 | Phase word accumulation with wraparound and output event behavior | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | Clock divider | L1 | Resettable or programmable divider/counter | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | Lock detector | L1 | Windowed phase/frequency lock decision | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | Voltage-domain charge-pump control abstraction | L1 | Voltage-domain UP/DN current-effect abstraction without transistor-level current solving | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | Sampled loop-filter abstraction | L1 | Sampled voltage-domain approximation of continuous-time PI loop-filter trend | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | PLL timing slice | L2 | PFD + divider + VCO or loop-control interaction | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | ADPLL lock/ratio-hop/timer flow | L2 | Digital phase/timer control + divider/VCO timing response | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| PLL / Clock / Event Timing | CPPLL tracking and frequency-step reacquire flow | L2 | PFD + charge-pump/filter abstraction + VCO response to frequency step | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Calibration, DEM, and Control | Trim-voltage generator | L1 | Signed error accumulator or bounded trim controller | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Calibration, DEM, and Control | Gain trim controller | L1 | Bounded gain-control update block | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Calibration, DEM, and Control | Rotating DEM selector | L1 | Unit-element pointer or rotation selector | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Calibration, DEM, and Control | Windowed DEM pointer | L1 | Barrel/window pointer with wrap behavior | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Calibration, DEM, and Control | DWA/DEM encoder | L1 | Dynamic element matching selection sequence or thermometer-coded rotation | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Calibration, DEM, and Control | Calibration deadband controller | L1 | Bounded trim update that holds state inside an error deadband | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Calibration, DEM, and Control | Successive-approximation calibration/search FSM | L1 | Multi-step search controller for trim or offset calibration | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Calibration, DEM, and Control | Element shuffler | L1 | Deterministic element permutation or scramble sequence | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Calibration, DEM, and Control | Complete calibration loop | L2 | Sensor or error source + controller + actuator behavior | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Measurement and Testbench Instrumentation | Crossing metric writer | L1 | Waveform crossing detector with metric artifact | tb; dut; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Measurement and Testbench Instrumentation | Settling response measurement helper | L1 | Testbench measurement for tolerance-entry timing | tb; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Measurement and Testbench Instrumentation | Peak detector | L1 | Running extrema or peak metric block | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Measurement and Testbench Instrumentation | Gain estimator | L1 | Testbench or helper block that extracts gain metric | tb; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Measurement and Testbench Instrumentation | Edge interval timer | L1 | Measures time interval between event or crossing edges | tb; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Measurement and Testbench Instrumentation | Measurement flow | L2 | Stimulus + DUT + metric artifact + checker | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Measurement and Testbench Instrumentation | Gain extraction/convergence measurement flow | L2 | Stimulus + gain estimator + convergence or trim metric artifact | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Stimulus and Sources | PRBS stimulus/dither generator | L1 | Deterministic pseudo-random stimulus or dither bit sequence in voltage-domain logic | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Stimulus and Sources | Periodic phase-ramp guard source | L1 | Periodic phase-ramp source with guard-pulse timing | tb; dut; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Stimulus and Sources | Burst clock source | L1 | Timed pulse or burst stimulus generator | tb; dut; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Stimulus and Sources | Dither or noise-like deterministic source | L1 | Reproducible pseudo-random stimulus source | tb; dut; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Stimulus and Sources | Sine/periodic voltage source | L1 | Deterministic periodic voltage stimulus with controlled amplitude and frequency | tb; dut; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Stimulus and Sources | ADC/DAC source sweep flow | L2 | Source sweep + converter response + code or reconstruction checker | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Analog Behavioral Signal Conditioning | First-order lowpass | L1 | Voltage-domain filter abstraction | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Analog Behavioral Signal Conditioning | Resettable integrator | L1 | Integrator with reset or decay semantics | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Analog Behavioral Signal Conditioning | Soft/hysteretic limiter | L1 | Smooth or stateful limiting distinct from hard voltage clamp | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Analog Behavioral Signal Conditioning | Voltage gain amplifier | L1 | Voltage-domain gain block with bounded output behavior | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Analog Behavioral Signal Conditioning | Higher-order filter | L1 | Multi-pole or second-order voltage-domain filter abstraction | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Analog Behavioral Signal Conditioning | Slew-rate limiter | L1 | Bounded slope transform | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Analog Behavioral Signal Conditioning | Amplifier/filter chain | L2 | Gain block + filter or limiter with measured chain response | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |
| Sample, Hold, and Analog Memory | Aperture-delay track-and-hold | L1 | Clocked track/sample behavior with explicit aperture timing and held output | dut; tb; bugfix; e2e-form | model-capability | Required | Static + EVAS + Spectre |
| Sample, Hold, and Analog Memory | Sample-and-hold with droop/leakage | L1 | Held analog memory with decay or leakage | dut; tb; bugfix; e2e-form | model-capability | Required with review | Static + EVAS + Spectre |
| Sample, Hold, and Analog Memory | Clocked sample-and-hold | L1 | Held analog memory sampled on clock edges; no reset port in the current validated kernel | dut; tb; bugfix; e2e-form | model-capability | Required expansion | Static + EVAS + Spectre |
| Sample, Hold, and Analog Memory | Converter front-end | L2 | Sampling front-end + quantizer or comparator interaction | e2e; tb | benchmark-e2e | Required expansion | Static + EVAS + Spectre |

## Promotion Source Trace

The clean release table above now includes the selected top-level coverage
targets. The rows below record where the added functions were discovered and
which nearby variants remain useful for future extension. A selected target is
still not a scored release task until it has reviewed prompt, metadata, gold,
checker, and EVAS/Spectre certification evidence.

| Category | Source-backed additions and deferred variants | Source-backed L2 additions and deferred variants |
| --- | --- | --- |
| Data Converters | Ideal clocked ADC; trim-code decoder for binary/one-hot/thermometer outputs; register-loaded binary-weighted DAC; unit-element thermometer DAC; capacitive/weighted DAC for SAR feedback; flash ADC; ADC code capture register; ADC/readout serializer; serial readout deserializer. | Ideal ADC/DAC chain; weighted SAR ADC/DAC loop; source-swept converter verification flow; flash ADC mini-array; conversion event controller flow; readout serializer frame-monitor flow. |
| Comparators and Decision Circuits | Ideal threshold comparator; propagation-delay comparator; hysteresis comparator; threshold detector; window detector; offset-search comparator; comparator debounce latch. | Comparator offset/delay/hysteresis measurement flow. |
| PLL / Clock / Event Timing | PFD UP/DN core; PFD small phase-error characterization; XOR phase detector; bang-bang phase detector; digital phase accumulator with modulo wrap; multimode divider ratio switch; voltage-domain charge-pump control abstraction; sampled loop-filter abstraction. | ADPLL lock/ratio-hop/timer flow; CPPLL tracking and frequency-step reacquire flow; PLL timing slice. |
| Calibration, DEM, and Control | DWA pointer generator; no-overlap DWA pointer; thermo-DWA encoder; gain calibration controller; calibration deadband controller; true offset-search FSM if redesigned. | Complete calibration loop. |
| Measurement and Testbench Instrumentation | Gain estimator; gain extraction metric; edge interval timer; waveform metric aggregator. | Gain extraction and convergence measurement flow; DUT plus metric-artifact flow. |
| Stimulus and Sources | Ramp source; burst-clock source; deterministic noise source; voltage/sine input source; PRBS/dither source. | ADC/DAC source sweep flow. |
| Analog Behavioral Signal Conditioning | Soft/hysteretic limiter; gain amplifier; higher-order filter; slew-rate limiter; resettable integrator. | Amplifier/filter chain. |
| Sample, Hold, and Analog Memory | Ideal sample-and-hold; clocked sample-and-hold; aperture/noise hold variant. | Converter front-end with sample/hold plus quantizer or comparator. |

## Non-Scored Conformance Surface

The following are deliberately outside the scored vaBench denominator:

| Conformance type | Purpose |
| --- | --- |
| Syntax legality | Ensure EVAS rejects code that Spectre rejects. |
| Source parsing | Isolate PWL/source continuation and breakpoint behavior. |
| Event scheduling | Isolate `cross()`, `timer()`, and coincident event ordering. |
| Sampling/timestep semantics | Isolate startup samples, `$abstime`, decay, and output row timing. |
| Checker semantics | Isolate CSV parsing, file metric parsing, tolerance windows, and result labeling. |
