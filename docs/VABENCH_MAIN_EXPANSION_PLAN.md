# vaBench Main Expansion Plan

**Date**: 2026-05-08

This plan expands beyond `bpack48` without losing the clean four-form pack
structure.  The goal is a benchmark large enough for paper-facing claims while
remaining auditable by strict-EVAS and Spectre.

## Why Expand Beyond bpack48

`bpack48` is clean but small: 12 concrete circuit functions x 4 task forms.  It
is excellent for development, but too small to prove generalization or separate
small PASS deltas from variance.  The next benchmark must increase both circuit
mechanism diversity and heldout coverage.

## Target Structure

| Split | Recommended size | Unit | Purpose |
| --- | ---: | --- | --- |
| `vaBench-dev48` | 12 packs x 4 = 48 | existing bpack48 | Fast iteration and smoke tests. |
| `vaBench-main-120` | 30 packs x 4 = 120 | concrete function packs | Minimum main paper table. |
| `vaBench-main-192` | 48 packs x 4 = 192 | concrete function packs | Preferred main benchmark. |
| `vaBench-heldout-48` | 12 packs x 4 = 48 | unseen function packs | Generalization and anti-overfit. |
| `vaBench-stress` | variable | edge cases | Evaluator parity and Spectre compatibility. |

Decision for v1: freeze `main-120` first and grow to `main-192` as a versioned
expansion after the protocol is proven.  The concrete v1 coverage table is
`docs/VABENCH_MAIN_COVERAGE_TABLE.md`.

## Coverage Axes

### Task Forms

Every normal pack should contain exactly one task per form:

| Form | Required burden |
| --- | --- |
| `bugfix` | Repair a provided incorrect implementation using public failure intent only. |
| `spec-to-va` | Generate DUT from public behavioral spec. |
| `end-to-end` | Generate a complete DUT/TB or integrated behavioral setup as specified. |
| `tb-generation` | Generate a testbench for a public DUT/interface. |

### Circuit Mechanisms

The main benchmark should cover at least these mechanism families:

| Mechanism family | Example pack candidates | Why it matters |
| --- | --- | --- |
| Threshold/static nonlinear | threshold detector, window detector, analog limiter, clamp, rectifier | Basic analog transfer behavior. |
| Stateful analog memory | hysteresis comparator, sample-hold, peak detector, debounce latch | Requires state retention and initialization. |
| Event/timing | pulse stretcher, edge detector, one-shot, clock divider, PFD | Tests `cross`, `timer`, ordering, pulse width. |
| Data conversion | binary DAC, thermometer DAC, flash ADC, SAR helper, quantizer | Code/voltage mapping and bit-vector handling. |
| Calibration/control | offset calibration, gain trim, background calibration, lock detector | Tests state machines and convergence criteria. |
| Pointer/selection | DWA pointer, rotating selector, element shuffler | Tests index arithmetic and multi-module interfaces. |
| Continuous dynamics | integrator, first-order low-pass, slew limiter, VCO phase integrator | Tests analog differential behavior. |
| Source/measurement/TB | PWL stimulus, sine source, file-output measurement, settling measurement | Tests testbench generation and simulator compatibility. |
| Mixed-signal protocol | PRBS7, serializer/deserializer helper, sample clocking, digital threshold IO | Tests digital-like behavior in Verilog-A. |
| Robustness/stress | parameter bounds, unsupported ranges, source syntax, escaped names | Separates evaluator compatibility from functional modeling. |

## Split Rule

Use circuit-function-level splits.  A heldout pack must not share the same
`circuit_function_id` or near-duplicate observable behavior with train/dev packs.
For example, if `binary_dac_4b` is in dev/main, do not put a trivial renamed
`binary_dac_4bit` in heldout.  Prefer a different conversion mechanism such as
`thermometer_dac` or `sar_adc_logic`.

## Promotion Gates

A pack can enter `vaBench-main` only after:

| Gate | Requirement |
| --- | --- |
| Public spec | Checker-observed behavior appears in `prompt.md`. |
| Artifacts | `prompt.md`, `meta.json`, `checks.yaml`, `checker.py`, and `gold/` exist. |
| Gold strict-EVAS | PASS. |
| Gold Spectre | PASS, or documented exclusion from main. |
| No leakage | Prompt, skill retrieval, RAG, and controller can solve it without task-id/gold/checker internals. |
| Duplicate audit | No duplicate observable behavior in the same split. |

## Experiment Matrix On Main Benchmark

Must-run rows:

| Row | Purpose |
| --- | --- |
| A `prompt-only` | Bare model capability. |
| D `rules-only` | Rule prompt contribution. |
| C `compile-loop` | Feedback loop contribution. |
| S1 `compile-skill-prompt` | Prompt-side skill contribution. |
| S2 `compile-skill-accept` | Local skill and accept/reject contribution. |

Run after residual taxonomy:

| Row | Purpose | Gate |
| --- | --- | --- |
| B `behavior-skill` | Fix behavior residuals after compile closure. | Compile-passing behavior residual set is large enough. |
| T `tool-controller` | Cost/pass Pareto through tool routing. | Useful tools exist and can be selected. |
| R `repair-trace-rag` | Retrieve prior accepted/rejected repair traces. | Trace schema and at least one model/main run are complete. |

Optional/appendix:

| Row | Status |
| --- | --- |
| `evas-repair` | Negative control if budget permits. |
| `mechanism-public` | Only if redefined as behavior repair without identity routing. |
| `functional-ir` | Only on residual families where IR has a clear mechanism hypothesis. |
| pass@k | Useful to separate sampling capacity from repair-system capacity. |
| prompt compression | Cost optimization after main pass/failure story is stable. |

## First Build Milestones

| Milestone | Output | Stop/go gate |
| --- | --- | --- |
| M0 | Coverage table with candidate packs and split labels. | No mechanism family dominates. |
| M1 | 10 new pack prototypes. | Each has four public task forms. |
| M2 | strict-EVAS gold validation. | 100% pass or pack is withheld. |
| M3 | Spectre gold audit. | 100% pass for promoted main packs. |
| M4 | A/D smoke on new packs with one model. | Runner and prompt extraction stable. |
| M5 | Freeze `vaBench-main-v1`. | Versioned manifest and audit report exist. |
