# vaBench Base Function Registry

Date: 2026-05-15

This registry is the counting layer for current promoted seed functions between
historical task rows and the clean vaBench release taxonomy.

Source table: `docs/VABENCH_BASE_FUNCTION_REGISTRY.csv`.

Selected top-level additions are tracked in
`docs/VABENCH_LEVEL_COVERAGE_TABLE.md`. The current clean release package has
materialized 75 L1/L2 package entries after removing duplicate L2 kernels, but
EVAS/Spectre release certification is still partial. The detailed
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
release package has materialized the selected 75-entry target, but release
certification is still partial. Score, speed, and model-baseline claims remain
disabled until their own claim gates are explicitly enabled.

The package asset target is larger than this current-seed registry:

| Pool | Count | Where tracked |
| --- | ---: | --- |
| Current promoted L1 seed functions | 28 | This registry. |
| Promoted top-level L1 additions | 32 | `docs/VABENCH_LEVEL_COVERAGE_TABLE.md` and `docs/VABENCH_RELEASE_TAXONOMY.md`. |
| Selected L2 package targets | 15 | `docs/VABENCH_LEVEL_COVERAGE_TABLE.md` and `docs/VABENCH_RELEASE_TAXONOMY.md`. |
| Top-level L1/L2 package target | 75 | 28 current L1 seeds + 32 promoted L1 additions + 15 L2 package targets. |

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
| Release entries | 75 | Materialized. |
| L1 entries | 60 | Materialized. |
| L2 entries | 15 | Materialized after duplicate L2 deletion. |
| Release task forms | 259 | Materialized. |
| EVAS/Spectre-certified entries | 23 | Partial; current package manifest is the source of truth. |
| EVAS/Spectre-certified forms | 101 | Partial; full release rerun/import remains pending. |
| Pending release entries | 52 | Await fresh certification or import. |
| Pending release forms | 158 | Await fresh certification or import. |
| Failed release entries/forms | 0 / 0 | No current release failure is countable as certified evidence. |
| EVAS PASS / Spectre FAIL mismatches | 0 | Clear. |
| Scored entries/forms | 0 / 0 | Disabled by policy. |

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
| `retriggerable_one_shot_pulse_stretcher` | Count as a promoted L1 addition, not as part of the original 28-seed registry. | One-shot-family pulse stretcher; unlike `one_shot_timer`, trigger edges during an active pulse refresh the falling deadline. |

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
| Retriggerable one-shot pulse stretcher | Active pulse remains high until the most recent trigger plus the specified width; reset cancels the active pulse. | `trig`, `rst`, `pulse`, burst trigger timing. | Ignoring retriggers while active, falling after the first trigger deadline, missing reset cancellation, or checking only one isolated trigger. |
| Signal conditioning | Analog transform has expected gain, filtering, clamping, rectification, or slew behavior. | Input/output waveforms and optional control/reset. | Pass-through behavior, wrong gain sign/magnitude, missing lag, clamp/slew violations, or unbounded output. |
| Sample/hold memory | Sample instant, hold behavior, and droop/aperture semantics. | Input waveform, sampling clock, held output. | Transparent-through behavior during hold, missing droop/leakage when required, or wrong aperture delay. |
| L2 chains | Interaction between named L1 blocks, not only individual module compilation. | Cross-block signals, final output, chain metric if present. | Generic L1-only checks, missing inter-block dependency, or metrics inconsistent with the composed flow. |

## Category Mapping Corrections

| Historical hint | Registry mapping |
| --- | --- |
| `analog-events` | `Digital and Event-Driven Logic` unless extracted as L0 conformance. |
| `phase-detector` | `PLL / Clock / Event Timing`. |
| `signal-source` for clamp/slew behavior | `Analog Behavioral Signal Conditioning`. |
| `measurement` helper rows | `Measurement and Testbench Instrumentation`, not generic `tb-generation`. |
| misleading historical `thermometer_dac` provenance | `Data Converters / Simple 4-bit binary-coded DAC`; release-facing base id is `simple_binary_voltage_dac_4b`. |

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
