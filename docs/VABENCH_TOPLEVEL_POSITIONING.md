# vaBench Top-Level Positioning

Date: 2026-05-15

This is the current top-level wording for vaBench after reviewing duplicate
function risk, analog/mixed-signal IC terminology, historical examples, and
EVAS/Spectre validation needs.

## One-Sentence Positioning

vaBench is a Verilog-A behavioral benchmark for analog/mixed-signal IC modeling,
organized by circuit function and certified with EVAS/Spectre evidence; EVAS is
the fast debug evaluator, while Spectre remains the reference simulator for
gold promotion and paper-facing claims.

## Scoring Surface

| Surface | What it contains | Counted in vaBench score | Paper role |
| --- | --- | --- | --- |
| L1 core circuit functions | Reusable behavioral IC blocks such as DACs, ADC quantizers, comparators, VCO/PFD/dividers, calibration/DEM, filters, limiters, and sample/hold blocks. | Yes | Main model-capability score. |
| L2 complete circuit flows | Multi-block or closed-loop flows such as converter chains, PLL slices, calibration loops, measurement flows, and converter front-end flows. | Yes | Higher-level composition score. |
| Auxiliary scored functions | Measurement and stimulus models when they have a real reusable circuit/testbench contract. | Yes, but report separately or with a smaller slice. | Shows benchmark can evaluate testbench and instrumentation tasks without letting them dominate. |
| L0 conformance | Syntax legality, source parsing, event scheduling, sampling, and checker semantics. | No | EVAS/Spectre health and regression evidence. |
| Historical evidence | main120, benchmark-v2, benchmark-balanced, smoke tasks, examples. | No, unless materialized into a certified task. | Discovery source and provenance. |

## Current Count Vocabulary

| Pool | Count | Meaning |
| --- | ---: | --- |
| Current promoted L1 seed functions | 28 | Countable functions inherited from current main120 after duplicate/removal policy. |
| Promoted top-level L1 additions | 32 | Additional L1 functions selected into the release coverage contract. |
| Selected L2 complete-circuit targets | 15 | System/flow tasks selected into the release coverage contract because they compose multiple L1 functions after duplicate kernels were removed. |
| Top-level L1/L2 coverage target | 75 | 28 current L1 seeds + 32 selected L1 additions + 15 selected L2 targets, before task-form multiplication. |
| Excluded historical bases | 2 | `background_calibration_accumulator` is merged; `offset_calibration_fsm` is removed pending redesign. |

The release score should only count materialized, certified tasks. The 32 L1
additions and 15 L2 targets are top-level coverage commitments, not current
scored tasks.

## Nine Top-Level Categories

| Category | Role in benchmark | Review decision |
| --- | --- | --- |
| Data Converters | DAC, ADC, decoder, SAR, and converter-loop behavior. | Core. This should be one of the largest categories. |
| Comparators and Decision Circuits | Threshold, offset, clocked, StrongARM-style, hysteresis, delay, and window-decision behavior. | Core. Keep detector tasks here when output is a binary decision. |
| PLL / Clock / Event Timing | VCO, PFD, divider, lock detector, phase accumulator, voltage-domain charge-pump abstraction, sampled loop-filter abstraction, and PLL flows. | Core. Important for event scheduling and mixed-signal timing behavior. |
| Calibration, DEM, and Control | Trim controllers, DEM/DWA, pointer selection, element shuffling, gain calibration, and calibration loops. | Core. Must aggressively deduplicate pointer variants. |
| Digital and Event-Driven Logic | Voltage-domain logic, counters, LFSR, serializer, pulse/event logic. | Useful but lower priority. Keep it from dominating the release. |
| Measurement and Testbench Instrumentation | Crossing metrics, settling time, gain estimation, peak detection, and artifact-generating measurement flows. | Auxiliary scored. Valid benchmark content, but separate from main circuit-function claims. |
| Stimulus and Sources | Ramp, burst clock, deterministic noise, dither, and source-driven flows. | Auxiliary scored. Count only reusable source models, not source syntax/conformance cases. |
| Analog Behavioral Signal Conditioning | Lowpass, integrator, rectifier, clamp, slew limiter, gain amplifier, soft limiter, and signal chains. | Core. Avoid duplicate limiter/clamp variants unless transfer behavior differs. |
| Sample, Hold, and Analog Memory | Track/hold, aperture, droop/leakage, resettable hold, and converter front-end sampling. | Core. Important converter-front-end primitive. |

## Duplicate and Naming Policy

| Risk | Policy |
| --- | --- |
| Binary DAC versus thermometer DAC | Use "simple 4-bit binary-coded DAC" for the current mathematical code-to-voltage model. Use "unit-element thermometer DAC" only when thermometer-coded unit cells are modeled. |
| Decoder versus DAC | A thermometer-code decoder is digital/code-format logic for converter control. It is distinct from a DAC only when no analog reconstruction is claimed. |
| StrongARM-style latch comparator | Keep the latch-style comparator as the clocked comparator coverage point; avoid a separate generic clocked comparator unless it adds independently checked behavior beyond reset/evaluate timing. |
| DEM pointer variants | Count separate tasks only when the selection rule differs: rotating pointer, windowed pointer, no-overlap DWA, or full thermo-DWA encoder. Pure wraparound edge cases are L0/checker cases. |
| Clamp versus limiter | `voltage_clamp` covers hard saturation. Add a new limiter only if it is soft, hysteretic, or otherwise behaviorally distinct. |
| Sample/hold droop versus leaky hold | Treat as one function unless reset, aperture, or noise behavior is central and separately checked. |
| Measurement helper versus checker schema | Metric writers and estimators can be tasks; checker schema validation is L0 conformance, not L1 circuit function. |
| Source model versus source syntax | Ramp/burst/noise/dither generators can be tasks; PWL continuation and breakpoint semantics are L0 conformance. |

## Recommended Paper Wording

Use this wording:

> vaBench organizes behavioral Verilog-A tasks by analog/mixed-signal IC circuit
> function. Scored tasks are L1 reusable circuit functions or L2 composed
> circuit flows. A separate L0 conformance suite isolates EVAS/Spectre syntax,
> source, event, sampling, and checker semantics. Historical task trees and
> examples provide source traces and provenance, but a task enters the
> release score only after prompt, metadata, checker, gold assets, and
> EVAS/Spectre certification are reviewed.

Avoid this wording:

> vaBench has 28 functions.

Reason: 28 is only the current promoted L1 seed count. The top-level expansion
pool is larger and should be reported separately.

Also avoid:

> vaBench is based on examples/main120/benchmark-v2.

Reason: those are construction and provenance sources, not the benchmark
definition.

## Next Experimental Direction

1. Promote current 28 L1 seeds into clean release tasks.
2. Materialize selected core L1 additions first: unit-element thermometer DAC,
   clocked ADC quantizer, threshold/delay/hysteresis/window comparators,
   PFD variants, DWA/DEM encoder, ramp/burst/noise/sine sources, gain
   estimator, edge interval timer, resettable sample/hold, and distinct
   signal-conditioning blocks.
3. Materialize selected L2 flows second: ADC/DAC chain, weighted SAR loop,
   flash ADC mini-array, PLL timing slices, calibration loop, event and
   serializer flows, measurement and gain-extraction flows, ADC/DAC source
   sweep flow, amplifier/filter chain, and converter front-end.
4. Keep L0 conformance growth parallel but separate from benchmark scoring.
