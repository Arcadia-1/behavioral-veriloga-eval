# vaBench Base Function Registry

Date: 2026-05-15

This registry is the counting layer for current promoted seed functions between
historical task rows and the clean vaBench release taxonomy.

Source table: `docs/VABENCH_BASE_FUNCTION_REGISTRY.csv`.

Selected top-level additions are tracked in
`docs/VABENCH_LEVEL_COVERAGE_TABLE.md`. The current clean release package has
materialized 79 L1/L2 package entries after removing duplicate kernels and weak
readout/control/PLL/DEM rows and adding bias/reference/power plus RF/AFE
coverage. The 79-entry target contains both core circuit entries and
measurement/stimulus support entries, with current EVAS/Spectre release
certification complete. The detailed
completed-content inventory is `docs/VABENCH_RELEASE_COMPLETED_CONTENTS.md`.

## Why This Exists

The current 120-row evidence inventory was built as 30 base circuits times four
task forms. That construction is useful, but it is not by itself a paper-safe
claim of 30 distinct circuit functions.

This registry adds one explicit decision per base:

| Decision | Meaning |
| --- | --- |
| `counts_as_distinct_function=yes` | The base can count as a distinct L1/L2 circuit function once its prompt/checker/gold are release-quality. |
| `counts_as_distinct_function=no` | The base is retained only as trace evidence or merged into another release function. |

## Current Counting Decisions

| Status | Bases | Action |
| --- | --- | --- |
| Clearly countable | 28 | Keep as current release seeds after wording/checker review. |
| Merged into canonical function | 1 | `background_calibration_accumulator` is completely merged into `cdac_calibration` trim-controller evidence. |
| Removed pending redesign | 1 | `offset_calibration_fsm` is removed from the release count for now. It can return only as a true multi-state offset-search controller. |

These numbers are registry decisions, not final benchmark scores. The current
release package has materialized and certified the selected 79-entry target.
The core score denominator is enabled for certified `track=core` entries;
speed and model-baseline claims remain blocked until their own claim gates are
explicitly enabled.

The package asset target is larger than this current-seed registry:

| Pool | Count | Where tracked |
| --- | ---: | --- |
| Current promoted L1 seed functions | 22 | `docs/VABENCH_RELEASE_SEED_MANIFEST.csv`. |
| Promoted top-level L1 additions | 40 | `docs/VABENCH_LEVEL_COVERAGE_TABLE.md` and `docs/VABENCH_RELEASE_TAXONOMY.md`. |
| Selected L2 package targets | 17 | `docs/VABENCH_LEVEL_COVERAGE_TABLE.md` and `docs/VABENCH_RELEASE_TAXONOMY.md`. |
| Top-level L1/L2 package target | 79 | 66 core circuit entries + 13 measurement/stimulus support entries. |

## Identifier Policy

Release IDs such as `vbr1_l1_charge_pump_abstraction` are stable internal
foreign keys, not the public circuit-function names. They decompose as
`vb` = vaBench, `r1` = release v1, `l1`/`l2` = benchmark level, and the suffix
= a stable slug. Paper-facing tables, prompts, and claims should lead with the
circuit function name, such as "Voltage-domain charge-pump control
abstraction" or "Trim-voltage generator"; the `vbr1_*` ID is only for manifest,
evidence, and script joins.

## Current Release Completion Snapshot

| Item | Count | Status |
| --- | ---: | --- |
| Release entries | 79 | Materialized. |
| L1 entries | 62 | Materialized. |
| L2 entries | 17 | Materialized after duplicate/weak entry deletion and later category expansion. |
| Release task forms | 271 | Materialized. |
| EVAS/Spectre-certified entries | 79 | Full release dual certification imported. |
| EVAS/Spectre-certified forms | 271 | Full release dual certification imported. |
| Pending release entries | 0 | No current release entries await dual certification. |
| Pending release forms | 0 | No current release forms await dual certification. |
| Failed release entries/forms | 0 / 0 | No current release failure is countable as certified evidence. |
| EVAS PASS / Spectre FAIL mismatches | 0 | Clear. |
| Scored entries/forms | 66 / 236 | Enabled for certified `track=core`; support remains excluded. |

See `docs/VABENCH_RELEASE_COMPLETED_CONTENTS.md` for the completed functions
by category and form.

## High-Risk Wording Decisions

| Base | Registry decision | Release wording |
| --- | --- | --- |
| `cdac_calibration` | Count as calibration/control. | "Trim-voltage generator"; do not call it a full CDAC model. |
| `background_calibration_accumulator` | Fully merged. | Treat as `cdac_calibration` trace evidence only; do not release or count separately. |
| `offset_calibration_fsm` | Removed for now. | Reintroduce later only if redesigned as a real multi-state offset-search controller. |
| `simple_binary_voltage_dac_4b` | Count. | Simple 4-bit binary-coded DAC using a mathematical code/15 transfer model; reserve "thermometer DAC" for unit-element thermometer-coded DAC tasks. |
| `unit_element_thermometer_dac` | Count after true 15-segment source review. | 4-bit-equivalent, 15-segment unary DAC; checker must exercise all fifteen segments including full-scale `seg14`. |
| `file_metric_writer` | Count with stronger checker. | Require a one-line `metric.out` value and compare it to waveform crossing time. |
| `settling_time_measurement_tb` | Count with explicit metric semantics. | Define tolerance band, settle window, and metric artifact behavior. |
| `vco_phase_integrator` | Count with tolerance policy. | Public prompt should describe final phase/frequency behavior; startup-sample parity belongs in evaluator policy. |
| `adc_code_capture_register` | Removed from the core release. | Weak readout-boundary logic duplicated converter support behavior without adding a strong analog/mixed-signal circuit function. |
| `serial_readout_deserializer` | Removed from the core release. | Readout reconstruction overlapped with serializer/frame-alignment support tasks and was not kept as a distinct core circuit function. |

## Function-Level Review Contract

Before promoting a task into the benchmark-strength surface, the prompt,
checker, and gold must agree on the circuit property being tested. This table is
the top-level review lens for future manual audits.

| Function area | Verification angle | Key observables | Checker must reject |
| --- | --- | --- | --- |
| Binary-weighted DAC | Binary code-to-voltage transfer with reference rails. | Code bits, `vref`, `vss`, analog output. | Missing MSB weight, non-monotonic code levels, wrong endpoint scaling, or thermometer wording leakage. |
| Unit-element thermometer DAC | Unary segment count-to-voltage transfer. | `seg0..seg14`, `vref`, `vss`, `aout`. | Missing `seg14`, 14/15 full-scale output, non-monotonic levels, or reuse of binary-coded DAC semantics. |
| ADC quantizer / decoder | Threshold or code mapping correctness. | Input voltage, output code bits or thermometer bits. | Wrong saturation, skipped code regions, inverted bit order, or insufficient threshold coverage. |
| Comparator family | Decision polarity, threshold, hysteresis, clock/evaluate timing, or delay. | Inputs, clock/reset where present, output decision waveform. | Stuck outputs, inverted polarity, missing hysteresis memory, or delay outside the specified window. |
| PFD/phase detector family | Phase-error direction produces bounded pulse response. | REF/DIV or data/clock edges, UP/DN or detector output. | Sustained overlap, missing UP/DN response, wrong direction, or a checker that only tests exact simulator threshold timing. |
| VCO / phase accumulator | Control-dependent phase or edge-rate behavior. | Control voltage, phase state, output clock edges. | No control dependence, no wrap/edge progression, or public reliance on startup-row simulator artifacts. |
| Calibration / control | Signed state update toward correction with bounded output. | Error input, trim/control state, actuator output. | Near-zero movement outside deadband, wrong sign, clamp violations, or duplicate kernels counted twice. |
| DEM / selector / shuffler | Legal pointer, rotation, or element-selection sequence. | Clock/reset, pointer bits, cell enables, selected element outputs. | Non-rotating selection, illegal one-hot/window width, missing wrap, or unchanged element stress pattern. |
| Measurement/testbench tasks | Metric artifact agrees with waveform semantics. | Waveform columns, `metric.out` or measurement output, crossing/settling windows. | Missing artifact, multiple/ambiguous records, metric-waveform mismatch, or final-row artifact passing. |
| Source/stimulus tasks | Requested waveform schedule or deterministic sequence is produced. | Source waveform, burst edges, seed/state outputs. | Wrong amplitude, wrong burst count, non-reproducible sequence, or underspecified timing. |
| Signal conditioning | Analog transform has expected gain, filtering, clamping, rectification, or slew behavior. | Input/output waveforms and optional control/reset. | Pass-through behavior, wrong gain sign/magnitude, missing lag, clamp/slew violations, or unbounded output. |
| Sample/hold memory | Sample instant, hold behavior, and droop/aperture semantics. | Input waveform, sampling clock, held output. | Transparent-through behavior during hold, missing droop/leakage when required, or wrong aperture delay. |
| L2 chains | Interaction between named L1 blocks, not only individual module compilation. | Cross-block signals, final output, chain metric if present. | Generic L1-only checks, missing inter-block dependency, or metrics inconsistent with the composed flow. |

## Category Mapping Corrections

| Historical hint | Registry mapping |
| --- | --- |
| `analog-events` | Map to the concrete analog-facing circuit family, such as Data Converter Models, Comparators, PLL Timing, Stimulus, or L0 conformance. |
| `phase-detector` | `PLL Clock and Timing Systems`. |
| `signal-source` for clamp/slew behavior | `Baseband Signal Conditioning`. |
| `measurement` helper rows | `Measurement Instrumentation Flows`, not generic `tb-generation`. |
| misleading historical `thermometer_dac` provenance | `Data Converter Models / Simple 4-bit binary-coded DAC`; release-facing base id is `simple_binary_voltage_dac_4b`. |

## Next Registry Gate

The top-level function-selection gate is complete. The next registry-adjacent
work is:

1. Keep `background_calibration_accumulator` and `offset_calibration_fsm` out
   of release-count denominators.
2. Keep L0 EVAS/Spectre conformance cases separate from L1/L2 benchmark
   coverage.
3. Finish or re-import full EVAS/Spectre release certification before any
   benchmark-ready claim.
4. Enable scoring only after the score-denominator policy is reviewed.
5. Add future benchmark functions only through the same path: top-level
   taxonomy decision, prompt/meta/checks/gold materialization, static checks,
   and EVAS/Spectre certification.
