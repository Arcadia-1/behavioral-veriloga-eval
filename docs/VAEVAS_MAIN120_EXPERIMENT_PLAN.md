# vaEVAS Main120 Experiment Plan

**Date**: 2026-05-08

## Core Position

We should not keep expanding the benchmark before running any model/system
experiments.  The current strategy is:

1. Build one clean, balanced, executable main benchmark (`vaBench-main-v1`,
   Main120).
2. Use it to validate task design, runner stability, model behavior, and method
   deltas.
3. Build heldout and stress/v2 only after the first matrix tells us which
   failure families and benchmark gaps actually matter.

Main120 is therefore not the final universe of Verilog-A evaluation.  It is the
first paper-facing, gold-validated anchor benchmark.

## Claim Map

| Claim | Why It Matters | Minimum Convincing Evidence | Linked Blocks |
| --- | --- | --- | --- |
| C1: A clean executable Verilog-A benchmark can expose model/system bottlenecks better than an accumulated historical pool | The old 143-style pool is useful but uneven; paper claims need clean splits and aligned contracts | Main120 passes semantic/integrity/EVAS/Spectre gates and reveals meaningful model failure differences | B0, B1 |
| C2: System mechanisms should be evaluated incrementally before adding more benchmark scale | Prevents overfitting benchmark construction or wasting compute on flawed tasks | A/D/C/S1/S2 on Main120 produce interpretable compile/behavior/cost deltas | B1, B2, B3 |
| C3: Generalization claims require heldout, not just Main120 | Skills/RAG/controller can overfit Main120 | Heldout48 is built after Main120 diagnostics and never used for tuning | B4 |

## Experiment Blocks

### B0: Benchmark Gate Already Completed

- Claim tested: Main120 is clean enough to be used as a main experimental anchor.
- Dataset / split: `vaBench-main-v1`, 30 packs / 120 tasks.
- Evidence:
  - semantic audit: `120/120 PASS`, `0 WARN`, `0 FAIL`
  - integrity audit: `PASS`
  - full strict-EVAS: `120/120 PASS`
  - full Spectre: `120/120 PASS`
- Success criterion: all gates pass.
- Status: DONE.
- Artifacts:
  - `docs/VABENCH_MAIN120_VALIDATION_REPORT.md`
  - `docs/VABENCH_MAIN120_CONFIDENCE_AUDIT.md`
  - Strategy gate audit: `PASS / GO`, `analysis/vabench-main-v1_strategy_gate_audit_20260508.json`

### B1: Main120 Model/Strategy Matrix

- Claim tested: model/system strategy differences are measurable on a clean benchmark.
- Dataset / split: Main120.
- Compared systems:
  - A: prompt-only
  - D: rules-only / spectre-strict public rules
  - C: compile-loop
  - S1: compile-skill-prompt
  - S2: compile-skill-accept
- Models:
  - first: the currently available target model/provider after smoke validation
  - later: Kimi, MiMo, and additional providers under the same output-token/reasoning policy
- Metrics:
  - primary: Spectre PASS@1, compile-pass, behavior-pass
  - secondary: strict-EVAS PASS, token usage, wall-clock time, truncation rate, repair iterations
- Success criterion:
  - at least one strategy improves compile-pass or final Spectre PASS without exploding cost
  - failure taxonomy separates compile residuals from behavior residuals
- Failure interpretation:
  - if all strategies tie, Main120 may be too easy or current mechanisms are ineffective
  - if compile improves but behavior does not, behavior-skill/controller work becomes the next focus
- Priority: MUST-RUN.

### B2: Residual Taxonomy

- Claim tested: remaining failures are structured enough to motivate targeted methods.
- Dataset / split: Main120 outputs from B1.
- Inputs:
  - generated candidates
  - strict-EVAS summaries
  - Spectre summaries
  - compile logs and checker notes
- Taxonomy axes:
  - compile/interface failure
  - simulator incompatibility
  - wrong module/port/function
  - event/timer behavior error
  - state initialization/reset error
  - analog threshold/range error
  - testbench/stimulus mismatch
  - token truncation/no code block
- Success criterion: top residual families explain most failures and map to actionable methods.
- Priority: MUST-RUN.

### B3: Method Triage After Residuals

- Claim tested: next method complexity is justified by observed failures.
- Candidate followups:
  - behavior-skill for behavior residuals
  - controller/tool routing for multi-step compile/behavior repair
  - repair-trace RAG if repeated repair patterns appear
  - prompt compression if token cost/truncation dominates
  - SFT/DPO only if enough clean traces are accumulated and heldout is locked
- Success criterion: choose at most two next mechanisms with clear residual support.
- Priority: MUST-RUN after B2, not before.

### B4: Heldout48 Construction

- Claim tested: results generalize beyond the benchmark used to tune skills/controllers.
- Dataset / split: `vaBench-heldout-v1`, planned 12 packs / 48 tasks.
- Timing: build after B1/B2 identify real gaps, but before final generalization claims.
- Hard rule: heldout cannot be used to tune skill cards, RAG examples, controller policies, or prompts.
- Success criterion:
  - heldout has four-form structure
  - semantic/integrity/EVAS/Spectre gold gates pass
  - final selected methods transfer from Main120 to heldout
- Priority: MUST-RUN before paper/generalization claims.

### B5: Stress / v2 Expansion

- Claim tested: evaluator and method robustness under harder edge cases.
- Dataset / split: stress or `vaBench-main-v2`.
- Include only after Main120 residuals justify it:
  - more realistic PLL/ADC/DAC composites
  - multi-module hierarchy
  - noisier measurement/TB tasks
  - Spectre syntax/semantic edge cases
  - EVAS/Spectre parity stress cases
- Priority: NICE-TO-HAVE for v1, MUST for later v2.

## Run Order

| Milestone | Goal | Runs | Decision Gate | Risk | Mitigation |
| --- | --- | --- | --- | --- | --- |
| M0 | Benchmark gate | Main120 audits + full EVAS/Spectre | DONE: all pass | Benchmark itself flawed | Already completed; rerun on benchmark/tool changes |
| M1 | Provider smoke | 3-5 tasks per model/provider | API, code extraction, token/time, truncation pass | Provider settings not comparable | Fix max output, reasoning mode, temperature, worker policy before full matrix |
| M2 | First Main120 row | Run A on Main120 | No systemic truncation/runner failure | Prompt-only too weak/noisy | Still useful as baseline; inspect residuals |
| M3 | Core strategy rows | Run D/C/S1/S2 on Main120 | Compile/pass/cost deltas are interpretable | Repair loops too expensive | Record cost and stop on cost explosion |
| M4 | Residual taxonomy | Analyze all Main120 rows | Identify top residual families | Failures diffuse | Then expand benchmark or simplify claims |
| M5 | Method triage | Decide behavior-skill/controller/RAG/compression | Pick at most two justified mechanisms | Adding methods becomes curve fitting | Require residual-family support and heldout validation |
| M6 | Heldout48 | Build and gold-validate heldout | Heldout gold gates pass | Hidden overfitting to Main120 | Lock heldout before final method tuning |
| M7 | Final validation | Run selected methods on heldout | Transfer holds | Main gains do not transfer | Report honestly; revise method or benchmark claims |

## Must-Run Matrix On Main120

| Row | Description | Why It Exists | Primary Metrics |
| --- | --- | --- | --- |
| A | prompt-only, one generation, no checker/skill/repair | base model capability | Spectre PASS, compile-pass, behavior-pass, cost |
| D | public strict rules prompt, one generation, no repair | rules contribution | delta over A |
| C | compile-loop | feedback/compile closure contribution | compile-pass delta, repair cost |
| S1 | compile-skill-prompt | prompt-side skill knowledge contribution | compile-pass/PASS delta, token cost |
| S2 | compile-skill-accept | deterministic accept/reject contribution | compile-pass/PASS delta, runtime cost |

## Stop / Go Gates

| Gate | Stop If | Go If |
| --- | --- | --- |
| Provider smoke | truncation or extraction failure rate is high | code extraction/token/time stable |
| A row | outputs are mostly empty/truncated | enough valid attempts to analyze |
| D/C/S1/S2 | strategy logs are incomplete or incomparable | same validator/settings across rows |
| Residual taxonomy | failures cannot be grouped | residual families are actionable |
| Heldout | heldout gold fails EVAS/Spectre | heldout gates pass and remains untuned |

## Confidence Assessment

I do not have mathematical 100% confidence, because no benchmark strategy can
prove checker completeness or future toolchain stability.  I do have practical
confidence in this strategy for the current stage because it explicitly avoids
both failure modes:

- It avoids blind benchmark expansion by forcing Main120 model/system feedback
  before heldout/stress/v2.
- It avoids premature method claims by requiring heldout before final
  generalization claims.

Remaining loopholes and mitigations are tracked in
`docs/VAEVAS_BENCHMARK_STRATEGY_CONFIDENCE.md`.
