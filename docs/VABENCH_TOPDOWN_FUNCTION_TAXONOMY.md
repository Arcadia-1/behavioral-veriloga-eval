# vaBench Top-Down Function Taxonomy

Date: 2026-05-15

This document is the target benchmark design surface. It defines what the final
vaBench release should contain before looking at existing experimental rows or
legacy task trees.

The immediate goal is to specify a complete vaBench coverage contract: large
circuit types, required behavioral functions, complete circuit forms, task
forms, and EVAS/Spectre certification rules. Historical rows, local examples,
and legacy task directories may help implementation, but they are not the
source of the benchmark definition.

For the current goal-mode input surface, use:

- `docs/VABENCH_RELEASE_TAXONOMY.md` for the clean release-facing taxonomy.
- `docs/VABENCH_BASE_FUNCTION_REGISTRY.md` and `.csv` for the current
  base-function counting decisions.

This file remains the construction rationale and audit trail.

## Design Principle

Use this construction order:

```text
large circuit type
  -> required behavioral functions
  -> complete circuit form
  -> task forms: dut / tb / bugfix / e2e
  -> EVAS/Spectre validation evidence
```

Avoid this construction order:

```text
existing rows
  -> categories after the fact
  -> paper claim
```

The second path makes duplicate kernels hard to see. The first path makes gaps
and duplicates visible before row counts become misleading.

## Taxonomy Contract

The nine categories below are the vaBench release taxonomy. They are not copied
from a single paper or standard benchmark, and they should not be justified as
being derived from historical construction artifacts.

The categories are chosen because they cover the major voltage-domain
behavioral Verilog-A circuit roles that the benchmark wants to evaluate:
conversion, decisions, clock/event timing, calibration/control, event-driven
logic, measurement/testbench behavior, stimulus/sources, signal conditioning,
and sample/hold memory. Existing experimental assets are only implementation
inputs that can be accepted, rewritten, or rejected against this contract.

External references can support individual circuit ingredients, but not this
exact eight-way split:

- Accellera Verilog-AMS LRM defines the language as a behavioral language for
  analog/mixed-signal systems, but does not prescribe a benchmark taxonomy.
- Verilog-AMS tutorial material commonly uses ADC/DAC and electrical digital
  bus models as mixed-signal behavioral examples.
- VerilogEval-style digital benchmarks motivate separating digital/event
  logic such as combinational logic, sequential logic, counters, and FSMs.
- PLL and ADC behavioral-modeling literature motivates treating full loops as
  complete systems assembled from components such as comparator, DAC, VCO,
  divider, PFD/charge pump, loop filter, and sample/hold.

Why these eight categories belong in the release:

| Category | Why it exists in vaBench | Design rationale |
| --- | --- | --- |
| Data Converters | ADC/DAC/SAR tasks are central mixed-signal behavioral models and have clear subfunctions. | Covers code/voltage conversion, quantization, decoder, and SAR loop behavior. |
| Comparators and Decision Circuits | Comparators are core mixed-signal decision elements and appear inside ADCs, detectors, and calibration loops. | Covers threshold, offset, delay, clocked reset, and event-decision behavior. |
| PLL / Clock / Event Timing | PLL-like blocks stress timers, edge ordering, phase accumulation, dividers, and lock logic. | Covers event scheduling and phase/frequency behavior within voltage-domain modeling. |
| Calibration, DEM, and Control | Calibration controllers and DEM pointers are common behavioral abstractions. | Covers feedback update, bounded control, pointer scheduling, and calibration loops. |
| Measurement and Testbench Instrumentation | Benchmark tasks need measurable outputs, metrics, and side effects such as file outputs. | Covers measurement helpers, metric generation, and testbench observability. |
| Stimulus and Sources | Testbench-generation tasks need reusable ramps, clocks, dither, and PWL-like sources. | Covers deterministic stimulus generation and source-driven verification flows. |
| Analog Behavioral Signal Conditioning | Filters, clamps, rectifiers, slew limiters, and integrators are simple but important voltage-domain blocks. | Covers continuous-valued transformations without expanding into KCL/KVL simulation. |
| Sample, Hold, and Analog Memory | S/H is a recurring converter front-end primitive and deserves separation from generic filters or converters. | Covers sampled analog memory, aperture behavior, leakage, and converter front ends. |

If this taxonomy is used in paper text, the safe wording is:

> We organize vaBench using a benchmark-construction taxonomy inspired by our
> voltage-domain AMS behavioral-modeling block boundaries.

Avoid wording such as:

> Prior work defines these nine standard categories.

## Function Levels

| Level | Meaning | Example | Use in benchmark |
| --- | --- | --- | --- |
| L0 primitive | One behavioral operator or event semantic. | threshold crossing, timer update, clamp, transition, file write. | EVAS/Spectre dual-simulator conformance set; not in headline score. |
| L1 component | A recognizable circuit block with a stable interface. | binary DAC, strongarm comparator behavior, clock divider, sample-and-hold. | Main benchmark base functions; counted in headline score. |
| L2 complete mini-system | Multiple L1 blocks connected into a realistic flow. | SAR ADC loop, gain calibration loop, ADPLL slice. | E2E tasks and paper-facing showcase circuits; counted in headline score. |

The benchmark scoring surface should be L1 and L2 functions only, because L1
and L2 are the circuit-function evaluation surface. L0 is not discarded: it
forms the EVAS/Spectre dual-simulator conformance set that explains and guards
the fast evaluator. See `## Evaluation Protocol` for the dual-simulator
agreement gate and the per-task-form grading rules.

## Evaluation Protocol

Every released L1/L2 benchmark row should have EVAS/Spectre certification
evidence. EVAS is the fast routine grader used for development-time model
evaluation; Spectre is the behavioral reference used for row certification,
gold promotion, and paper-facing final claims. L0 rows live in the companion
conformance suite rather than in the scored benchmark surface.

### Simulator roles

| Simulator | Role | Used at | Property |
| --- | --- | --- | --- |
| EVAS | Fast routine grader and debug evaluator. | L0, L1, L2. | Sub-second to single-second turnaround on benchmark rows. |
| Spectre | Behavioral reference for certification and paper-facing claims. | L0, L1, L2. | Slower, trusted as the final judge. |

Spectre is not on the ordinary development hot path. After a row is certified,
EVAS can be used as the default fast grader for iteration. Paper-facing model
scores should still be backed by Spectre audit evidence, especially for new
models, new task families, or suspected EVAS/Spectre semantic gaps.

### Dual-simulator agreement gate

A released L1/L2 row is admitted into the scored benchmark only after passing
this gate:

1. The same DUT, testbench, and checker triple is driven into EVAS and Spectre
   with identical stimulus.
2. Each simulator emits a verdict bundle: continuous-probe waveform samples,
   declared digital probe edges and timestamps, the `done` signal, and any
   declared file side effects.
3. The two verdict bundles are compared under the tolerances defined below.
4. Agreement -> the row is certified, and its certified verdict bundle becomes
   the fast-grading reference for that row.
5. Disagreement -> the row is quarantined; the divergence is treated as an EVAS
   or Spectre modeling issue, not a model error, and the row does not enter the
   scored benchmark until resolved.

This gate is what allows EVAS to be used as the routine fast grader: every
certified row carries Spectre-backed evidence that the reference/gold behavior
is aligned. It does not mean arbitrary future submissions can never expose a
new EVAS/Spectre divergence; those cases should trigger Spectre audit or
conformance expansion.

### Role of L0 in the protocol

L0 primitive rows are not counted in the headline benchmark score. The headline
score is computed over L1 and L2 only, because L1 and L2 are the circuit-
function evaluation surface.

L0 rows are nonetheless mandatory inputs to the dual-simulator agreement gate.
They form the conformance backbone of the benchmark:

- Each L0 row stresses one behavioral primitive in isolation (`cross`, `timer`,
  `transition`, clamp, contribution, file write, etc.).
- L0 is the smallest scope at which EVAS/Spectre divergence can be localized.
  An L1 or L2 disagreement is far harder to root-cause.
- Maintaining the L0 conformance set surfaces simulator divergences at
  primitive scope before they contaminate composite L1 or L2 rows.

This reframes L0 rather than discarding it. L0 is not a scored benchmark
surface; it is the conformance set that licenses EVAS as the L1/L2 grader. The
construction taxonomy therefore covers all three levels, but the published
benchmark score reports L0 conformance and L1/L2 task performance as separate
quantities.

### Per-task-form judging

Every approved L1 or L2 base may expand into one or more task forms below. The
four-form expansion is a design pattern, not an obligation: `bugfix` requires a
realistic badcase, and `e2e` is only L2 when the task actually composes multiple
components. Each form has its own input, expected output, and grading rule.
Routine grading is anchored to the row's certified verdict bundle; final
paper-facing claims can be audited with Spectre.

| Task form | Model input | Model output | Grading rule |
| --- | --- | --- | --- |
| `dut` | Natural-language circuit spec + port list. | A `.va` module implementing the spec. | EVAS runs the model DUT against the reference TB and checker. Pass if the EVAS verdict bundle matches the certified verdict bundle within tolerance. |
| `tb` | Natural-language testbench spec + reference DUT interface. | A testbench that drives the DUT and reports a metric or `done`. | EVAS runs the reference DUT under the model TB. Pass if the model TB elicits the reference event/timing coverage and reports the expected metric. |
| `bugfix` | A perturbed reference `.va` plus the failing checker report. | A patched `.va`. | EVAS runs the patched module under the reference TB and checker. Pass if the certified verdict is restored. |
| `e2e` | Natural-language scenario or system spec. | One or more modules implementing the scenario or mini-system. | EVAS runs the model system under the reference scenario. Pass if the end-to-end metric (e.g., final SAR code, PLL lock time, calibration residual) is within tolerance. Only multi-component e2e rows count as L2. |

A task form is only released for a base after that base is approved and after
its certified verdict bundle exists. Bases that have not yet passed the
dual-simulator gate cannot expand into task forms.

### Tolerances

Default tolerances apply unless a row overrides them in its sidecar.

| Quantity | Default tolerance |
| --- | --- |
| Continuous voltage probe | 1% of declared full-scale range, sampled on the declared probe grid. |
| Event/edge timestamp on declared digital probe | 1% of nominal period, or 1 ns absolute, whichever is larger. |
| Event ordering on declared digital probes | Exact match. |
| `done` signal | Exact match. |
| Declared file side effects | Exact match on declared fields; non-declared bytes are ignored. |

Per-row tolerance overrides are version-pinned in the row sidecar so that
grading is deterministic and reproducible across runs.

### Scoring aggregation

- Per row: pass or fail under the per-task-form grading rule.
- Per category: pass rate over the L1 and L2 rows in that category, reported
  separately for each task form.
- Taxonomy-balanced headline score, once the taxonomy is sufficiently filled:
  macro-average of per-category L1+L2 pass rates over the approved categories.
  A separate L2-only score should expose mini-system performance, which is the
  harder evaluation surface.
- Interim internal inventories should remain more conservative: row-level pass
  rate, base-function coverage, EVAS/Spectre dual-validation status, and known
  duplicate/gap decisions.
- L0 conformance is reported separately as an EVAS/Spectre health metric and
  is not folded into the headline score.

## Release Circuit Types

This section is the normative vaBench release coverage contract. The
"implementation source trace" column is only for internal traceability while we
build the package; a source row can be reused, rewritten, or dropped. The
paper-facing benchmark should describe the required functions, complete circuit
forms, task forms, and certification evidence, not the experimental source from
which a function was first noticed.

### 1. Data Converters

Internal implementation notes, not release rationale:
`adc_dac_ideal_4b`, `d2b_4b`, `dac_binary_clk_4b`,
`vbm1_thermometer_dac_15seg_*`, `sar_adc_dac_weighted_8b`.

| Required function | Complete circuit form | Implementation source trace | Release action |
| --- | --- | --- | --- |
| Simple binary-coded DAC mapping | code bits plus reference rails drive analog output through a mathematical code/15 transfer model. | Historical `thermometer_dac` evidence actually covers `simple_binary_voltage_dac_4b`. | Keep public wording as simple 4-bit binary-coded DAC; do not describe it as thermometer or segmented DAC. |
| Clocked DAC update | sampled code updates output on clock edge. | Prototype coverage is incomplete. | Add L1 clocked binary DAC. |
| Unit-element thermometer DAC | Fifteen unary segment inputs implement a 4-bit-equivalent unit DAC with endpoint-scaled voltage output. | Covered by `unit_element_thermometer_dac`; distinct from the simple binary-coded DAC. | Keep as a separate unit-element DAC base; checker must count all 15 segments including full scale. |
| Segmented DAC | binary LSBs plus thermometer MSBs combine into output. | `segmented_dac`. | Strengthen checker for segment weights and code transitions. |
| Binary-to-thermometer decoder | binary code generates cumulative thermometer controls. | `thermometer_decoder_guarded`. | Keep as digital converter helper, not analog DAC. |
| Analog-to-binary quantizer | analog input maps to code bits. | Prototype coverage exists but is not release-ready. | Add ADC quantizer base. |
| SAR sequencer | comparator result controls bit trial sequence. | `sar_logic_4b`. | Keep L1 logic; add L2 SAR ADC loop later. |
| Complete SAR ADC loop | sample/hold + comparator + DAC + SAR logic. | Existing source material is partial. | High-priority L2 expansion. |

Audit note: data converters should not be one bucket called "DAC". Binary,
thermometer, segmented, quantizer, SAR logic, and full SAR loop are different
benchmark functions.

### 2. Comparators and Decision Circuits

Internal implementation notes, not release rationale: `cmp_ideal`, `cmp_delay`, `cmp_offset_search`,
`cmp_strongarm`, `edge_interval_timer`.

| Required function | Complete circuit form | Implementation source trace | Release action |
| --- | --- | --- | --- |
| Ideal threshold comparator | analog differential input drives digital decision. | Not yet cleanly isolated as a release task. | Add simple ideal comparator base if needed. |
| Offset comparator | decision threshold shifted by modeled offset. | `offset_comparator`. | Keep; ensure prompt states offset sign. |
| Delayed comparator | decision occurs after bounded delay. | Prototype coverage exists but is not release-ready. | Add if delay semantics are useful. |
| StrongArm-style clocked comparator | rising clock decides, falling clock resets outputs. | `strongarm_comparator_behavior`. | Keep behavioral scope explicit. |
| Edge/time interval measurement | compare event timing between two signals. | `lock_detector` partly covers this. | Add standalone edge interval timer or keep as conformance. |
| Complete comparator test flow | stimulus + comparator + decision checker. | e2e form can cover this. | Use for benchmark showcase, not duplicate L1 rows. |

Audit note: comparator tasks should separate threshold, offset, delay, reset
phase, and timing measurement. These are distinct behaviors and should not be
collapsed into one "comparator" label.

### 3. PLL / Clock / Event Timing

Internal implementation notes, not release rationale: no complete local PLL
prototype exists; nearest reusable source traces are comparator timing, clock
divider, and stimulus clock generation.

| Required function | Complete circuit form | Implementation source trace | Release action |
| --- | --- | --- | --- |
| VCO phase integrator | control voltage changes phase increment and output edge rate. | `vco_phase_integrator`. | Keep; startup semantics belong in conformance. |
| Clock divider | programmable ratio maps input clock to output clock. | `resettable_counter_divider`. | Keep; add dynamic ratio hop later. |
| PFD UP/DN logic | REF/DIV edges generate UP/DN and reset overlap. | `pfd_reset_race`. | Keep; dense timing must remain robust. |
| PFD small phase-error response | small REF/DIV phase offsets generate short bounded UP or DN pulses with no sustained overlap. | `pfd_small_phase_response_smoke`. | Keep as a phase-error response task, not as an exact simulator-threshold conformance task. |
| Lock detector | aligned feedback/reference edges assert lock. | `lock_detector`. | Keep; consider unlock behavior expansion. |
| Charge pump / loop filter behavior | UP/DN pulses adjust control voltage. | Not covered. | Add L1 charge-pump/loop-filter behavioral block. |
| Complete PLL slice | PFD + CP/filter + VCO + divider + lock detector. | Partial through individual bases only. | High-priority L2 expansion. |

Audit note: PLL coverage is important because it exercises event scheduling and
timer-driven analog state without leaving voltage-domain behavior.

### 4. Calibration, DEM, and Control

Internal implementation notes, not release rationale: reusable source traces exist
for pointer generation and gain-calibration flow.

| Required function | Complete circuit form | Implementation source trace | Release action |
| --- | --- | --- | --- |
| Generic signed calibration accumulator | error bit updates bounded control variable. | `background_calibration_accumulator`, `cdac_calibration`, `offset_calibration_fsm`. | Duplicate-risk group; keep at most one generic version unless roles diverge. |
| Deadband trim controller | measured value compared to target with hold band. | `gain_trim_controller`. | Keep; distinct from binary error accumulator. |
| Offset search controller | comparator sign drives trim convergence. | `offset_calibration_fsm`. | Redesign into real FSM/search if counted separately. |
| DEM pointer | rotating pointer selects unit elements. | `rotating_element_selector`. | Keep if presented as DEM pointer. |
| Windowed DEM pointer | adjacent two-hot or no-overlap window selection. | `barrel_pointer_window`. | Keep if two-hot/window behavior is central. |
| Shuffler / scrambling sequence | nontrivial permutation of selected elements. | `element_shuffler`. | Keep only if permutation differs from rotation. |
| Complete calibration loop | estimator + controller + actuator + plant. | Existing source material is partial. | High-priority L2 expansion. |

Audit note: this is the highest duplicate-risk area. Several current rows share
the same "clocked signed update and clamp" kernel. They may be useful tasks, but
the paper should not count them as unrelated circuit functions without redesign
or explicit role separation.

### Former Control/Readout Bucket Split

The previous standalone control/readout bucket has been removed from the release taxonomy. Its useful analog-facing tasks now live in concrete circuit families:

| Function | Current category | Rationale |
| --- | --- | --- |
| Comparator debounce latch | Comparators and Decision Circuits | It qualifies comparator decisions and reset behavior. |
| ADC code capture register | Data Converters | It captures conversion-result code and overrange state at the ADC readout boundary. |
| ADC/readout serializer frame aligner | Data Converters | It serializes converter/readout words with frame alignment. |
| Serial readout deserializer | Data Converters | It reconstructs framed converter/readout words. |
| Conversion event controller | Data Converters | It sequences sample, compare, readout, and done phases. |
| Readout frame-monitor flow | Data Converters | It checks serializer/readout reconstruction as a converter flow. |
| PRBS stimulus/dither generator | Stimulus and Sources | It is reusable deterministic stimulus support. |

Pure edge detector, pulse stretcher, one-shot, and parity-only readout helpers are not release functions in this package.

### 5. Measurement and Testbench Instrumentation

Internal implementation notes, not release rationale: reusable source traces exist
for gain extraction, file I/O, and timing-boundary checks.

| Required function | Complete circuit form | Implementation source trace | Release action |
| --- | --- | --- | --- |
| Crossing metric writer | crossing time is written to file and exposed by `done`. | `file_metric_writer`. | Keep normal task; file semantics also in conformance. |
| Settling response measurement helper | response plus threshold/time condition asserts `done`. | `settling_time_measurement_tb`. | Keep as measurement helper, not lowpass duplicate. |
| Peak detector | max tracker with reset. | `peak_detector`. | Keep. |
| Gain estimator | estimate gain from injected stimulus or ADC samples. | No release-ready source task. | Add high-value measurement expansion. |
| Complete measurement flow | stimulus + DUT + estimator + reported metric. | No release-ready source task. | High-priority L2 expansion. |

Audit note: measurement tasks should specify both waveform observables and
metric side effects. Pure file or exact final-step semantics should be
conformance unless tied to a measurement circuit role.

### 6. Stimulus and Sources

Internal implementation notes, not release rationale: reusable source traces exist
for burst clocks, deterministic noise-like stimulus, and ramps.

| Required function | Complete circuit form | Implementation source trace | Release action |
| --- | --- | --- | --- |
| Ramp source | timer/PWL-like source generates monotone ramp. | No release-ready source task. | Add as source-helper task if public benchmark includes TB generation. |
| Burst clock source | gated or finite burst clock generation. | No release-ready source task. | Add for clock/testbench tasks. |
| Noise source / dither | deterministic pseudo-noise or bounded random-like source. | No release-ready source task. | Add carefully; avoid nondeterministic scoring. |
| PWL/step source | configured step or breakpoint sequence. | Partly through testbenches, not as model task. | Add if EVAS source semantics matter. |
| Complete source-driven testbench | reusable source drives DUT and checker. | Existing source material is partial. | Strong fit for `tb-generation` tasks. |

Audit note: source/stimulus functions are important for testbench generation
and EVAS debug value, but the final release should include them only when the
public task contract is deterministic.

### 7. Analog Behavioral Signal Conditioning

Internal implementation notes, not release rationale: reusable source traces exist
for simple signal-conditioning L1 blocks.

| Required function | Complete circuit form | Implementation source trace | Release action |
| --- | --- | --- | --- |
| Lowpass filter | timer-discretized first-order response. | `first_order_lowpass`. | Keep; add second-order later. |
| Integrator | timer accumulation with reset/clamp. | `resettable_integrator`. | Keep; distinct from signed calibration accumulator due to analog input. |
| Rectifier | sign-dependent output. | `precision_rectifier`. | Keep as simple analog nonlinear baseline. |
| Clamp / limiter | bound signal to rails or range. | `voltage_clamp`. | Keep; avoid over-counting with rectifier. |
| Slew-rate limiter | per-step bounded movement. | `slew_rate_limiter`. | Keep. |
| Complete signal chain | source -> filter/limiter/nonlinearity -> measurement. | Not cleanly represented. | Add L2 analog chain expansion. |

Audit note: these are simple but valuable because they test continuous-valued
behavior using only voltage-domain assignments and event/timer updates.

### 8. Sample, Hold, and Analog Memory

Internal implementation notes, not release rationale: reusable source traces exist
for ideal sample/hold behavior in converter flows.

| Required function | Complete circuit form | Implementation source trace | Release action |
| --- | --- | --- | --- |
| Ideal track/sample hold | sample actual `vin` on clock and hold value. | `track_hold_aperture` samples `vin` with aperture delay. | Keep. |
| Aperture-delay sample hold | clock schedules delayed capture. | `track_hold_aperture`. | Keep; avoid exact solver artifact scoring. |
| Leaky hold | sampled or fixed held value decays over time. | `leaky_hold`, but current version captures fixed level. | Consider upgrading or adding input-tracking leaky hold. |
| Complete front-end | source + S/H + ADC/comparator. | Not yet release-ready as a single L2 task. | Add as data-converter L2 expansion. |

Audit note: `leaky_hold` is useful but currently weaker as a circuit model
because it captures a fixed level rather than `vin`. It should be reviewed
before being treated as a mature sample-and-hold function.

## Audit Workflow

Use the following audit loop before adding more rows:

1. Freeze this top-down taxonomy.
2. For each required function, mark one of:
   - release-ready with EVAS/Spectre evidence,
   - implemented only as internal source-trace material,
   - missing and high priority,
   - out of current voltage-domain scope.
3. For every covered function, decide whether it is L0, L1, or L2.
4. Remove or down-count functions that are only duplicate kernels with renamed
   ports.
5. Add new base functions only when they fill a taxonomy gap.
6. Derive `dut`, `tb`, `bugfix`, and `e2e` forms after the base function is
   approved.
7. Promote only after EVAS/Spectre validation evidence exists.

## Immediate Audit Decisions

| Decision ID | Topic | Recommended decision | Why |
| --- | --- | --- | --- |
| A001 | Should benchmark construction be top-down? | Yes. Freeze circuit-type taxonomy before expanding rows. | This avoids padding by duplicated kernels. |
| A002 | Is a small historical base-function list enough? | No. Build the complete release coverage table first. | A small validated set is useful implementation material, but too small to define the full benchmark space. |
| A003 | Should historical validated rows be ignored? | No. Reuse them only when they satisfy the release contract. | They contain valuable EVAS/Spectre evidence, but should not drive the ontology. |
| A004 | Should every base expand to four forms? | Only after the base is approved. | Otherwise duplicated or weak functions multiply into four weak rows. |
| A005 | What should expansion optimize? | Add missing L1/L2 functions, not row count. | Coverage quality matters more than `N` in the paper. |

## Selected Top-Level Additions

High-priority additions selected from release taxonomy gaps. They are part of
the top-level coverage target, but they do not enter the scored benchmark until
prompt, metadata, checks, gold assets, and EVAS/Spectre evidence are complete.

| Selected base | Type | Level | Why it matters |
| --- | --- | --- | --- |
| unit-element thermometer DAC | data-converter | L1 | Separate from the simple binary-weighted DAC baseline. |
| analog-to-binary quantizer | data-converter | L1 | Adds ADC-side conversion coverage. |
| clocked binary DAC | data-converter | L1 | Separates static mapping from sampled update behavior. |
| SAR ADC mini-loop | data-converter | L2 | Turns SAR logic, comparator, DAC, and S/H into a complete circuit form. |
| charge pump / loop filter | PLL | L1 | Completes the missing middle of a PLL slice. |
| ADPLL/CPPLL mini-loop | PLL | L2 | Provides a realistic complete clocking benchmark. |
| gain estimator | measurement | L1 | Strengthens measurement/extraction coverage. |
| gain calibration loop | calibration/measurement | L2 | Gives a complete calibration flow with estimator, controller, actuator, and plant. |
| ramp source | stimulus | L1 | Supports testbench-generation tasks. |
| burst clock source | stimulus | L1 | Supports event-driven testbench tasks. |
| LFSR/PRBS generator | digital-logic | L1 | Adds deterministic sequence generation. |
| input-tracking leaky sample hold | sample/hold | L1 | Fixes the current fixed-level leaky-hold weakness. |
