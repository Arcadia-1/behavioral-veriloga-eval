# vaEVAS Clean Mainline Plan

**Date**: 2026-05-07

This document trims the current vaEVAS work into a clean paper-facing mainline.
It does not delete historical artifacts.  Instead, it defines which results are
maintained, which are diagnostic, and which future runs should use the new naming
contract.

Repository artifact cleanup policy lives in
`docs/REPOSITORY_CLEANUP_POLICY.md`.  Cleanup should be staged as ignore,
summarize, archive, then delete only in a dedicated cleanup PR if needed.

## One-Sentence Project Goal

vaEVAS builds a Spectre-aligned evaluation and skill-guided closure framework for
LLM-generated Verilog-A, so that generation failures can be measured, audited,
and improved from public circuit specifications.

## Clean Thesis

The paper should defend two claims:

| Claim | Meaning | Minimum evidence |
| --- | --- | --- |
| C1: Spectre-aligned evaluation | EVAS can serve as a fast evaluator only when the maintained `strict-evas` validator follows Spectre frontend legality and execution semantics closely enough. | `strict-evas` main results plus real Spectre audits with zero pass/fail mismatch on full or targeted slices. |
| C2: Skill-guided compile closure | The dominant near-term bottleneck is compile/interface legality, and compile skills improve it more reliably than generic repair loops. | `rules-only -> compile-loop -> compile-skill-*` ablation under one benchmark, one validator, one model/accounting protocol. |

The current project should not yet claim that mechanism guidance or functional IR
is solved.  Those are next-stage behavior-repair hypotheses.

## Canonical Benchmark

Use only one maintained benchmark for current claims:

| Canonical name | Role |
| --- | --- |
| `b143` / `benchmark-balanced` | Main benchmark: 143 non-oracle Verilog-A generation tasks. |

The benchmark should be described by task forms and circuit-function coverage,
not by historical construction provenance:

| Task form | Count |
| --- | ---: |
| `bugfix` | 25 |
| `dut-only/spec-to-va` | 33 |
| `end-to-end` | 62 |
| `tb-generation` | 23 |

It covers 22 core-function families.  Every core-function family has at least
one task in each of the four task forms, but the benchmark is not count-equal
across task forms because the inherited task mix is end-to-end heavy.
The detailed benchmark audit is in `docs/B143_BENCHMARK_AUDIT.md`.
The planned exact function-pack benchmark is described in
`docs/BPACK_BENCHMARK_PLAN.md`.

Policy:

- Do not run new standalone `full92` main experiments.
- Report task-form and core-function breakdowns for `b143`; use older source
  labels only for debugging or appendix migration notes.
- Retire fixed-stage/lite/non-strict EVAS from all current claims.
- Add future tasks as circuit-function packs: introduce one function family, then
  cover the relevant task forms without duplicating the same observable
  behavior.
- Do not present `b143` as an exact four-form pack benchmark; use the planned
  `bpack-v1` / `bpack48` benchmark for that claim.

## Canonical Validators

| Canonical name | Meaning | Use |
| --- | --- | --- |
| `strict-evas` | The unified main validator: Spectre-compatible preflight, EVAS simulation, then checker. | Main validator for full 143 runs. |
| `spectre-audit` | Real Spectre execution through bridge plus the same checker. | Audit full or targeted slices; not required for every full run. |
| `legacy-score` | Old single-task/score.py-style validation. | Historical debugging only; not a maintained claim surface. |

`strict-evas` is one validator, not three separate evaluation methods.  Its two
internal alignment mechanisms have different responsibilities:

| Internal mechanism | Handles | Example |
| --- | --- | --- |
| Spectre-compatible preflight | Frontend legality: candidates that Spectre would reject before meaningful simulation. | Unsupported parameter ranges, source syntax, illegal module-header continuation, incompatible instance/source forms. |
| EVAS parser/kernel parity fixes | Execution semantics: candidates Spectre accepts but EVAS used to parse or simulate differently. | String parameter propagation into `$fopen`, source waveform parameter semantics, timer/cross/source behavior parity. |

Real `spectre-audit` validates the combined `strict-evas` behavior.  The audit
backend is not the main full-run evaluator because it is slower and heavier; it
is the trust anchor for targeted/full parity checks.

## Canonical Condition Names

Future tables and run ids should use descriptive names instead of opaque A/D/F/G/I
labels.  Legacy labels may appear in parentheses only for continuity.

| Canonical condition | Legacy label | Keep? | Current result | Paper role |
| --- | --- | --- | ---: | --- |
| `prompt-only` | `A` | Yes | `31/143` | Lower baseline. |
| `rules-only` | `D` | Yes | `68/143` | Strong public-rule baseline. |
| `evas-repair` | `F` | Appendix/negative control | `70/143` | Shows generic repair loop is weak. |
| `compile-loop` | `C` | Yes | `75/143` | LLM compile-first closure baseline. |
| `compile-skill-prompt` | `C-SKILL` | Yes | `78/143` | Prompt-side skill guidance contribution. |
| `compile-skill-local` | `C-SKILLPLUS` | Appendix ablation | `80/143` | Deterministic local skill layer. |
| `compile-skill-accept` | `C-ULTRA(full)` | Yes | `81/143` | Conservative audited skill accept/reject layer. |
| `compile-skill-advanced` | `C-ULTRA-ADVANCED` | Yes, current best | `83/143` | Current best clean compile-skill row. |
| `mechanism-public` | `G public-only` | Rerun before claim | `76/143` diagnostic | Behavior-mechanism hypothesis, not accepted. |
| `functional-ir` | `I` | Rerun only if justified | `67/143` diagnostic | Future behavior-repair branch. |

Main table should be compact:

1. `prompt-only`
2. `rules-only`
3. `compile-loop`
4. `compile-skill-prompt`
5. `compile-skill-accept`
6. `compile-skill-advanced`

Appendix/diagnostic table should include `evas-repair`, `compile-skill-local`,
`mechanism-public`, `functional-ir`, MiMo/cross-model, and prompt compression.

## Run ID Naming Contract

Future generated/result directories should use this shape:

```text
<artifact-kind>-<bench>__<model>__<validator>__<condition>__<yyyymmdd>[-rN]
```

Where:

| Field | Example | Notes |
| --- | --- | --- |
| `artifact-kind` | `generated`, `results` | Keep generated candidates and evaluation results separate. |
| `bench` | `b143`, `targeted7` | Full benchmark or explicit targeted slice. |
| `model` | `kimi-k25`, `mimo-v25-pro` | Sanitized exact model label; exact provider id remains in metadata. |
| `validator` | `strict-evas`, `spectre-audit`, `both-audit` | Use `both-audit` only for EVAS+Spectre paired audits. |
| `condition` | `rules-only`, `compile-skill-advanced` | Canonical condition names only. |
| `yyyymmdd` | `20260507` | Add `-r2`, `-r3` for reruns. |

Examples:

```text
generated-b143__kimi-k25__strict-evas__rules-only__20260507
results-b143__kimi-k25__strict-evas__compile-skill-advanced__20260507
results-targeted7__kimi-k25__both-audit__compile-skill-advanced-r6__20260505
```

Do not bulk-rename existing historical directories.  Existing artifacts remain
traceable through result summaries and the legacy-to-canonical mapping above.

## Maintained Evidence

| Evidence | Status | Keep in clean story? |
| --- | --- | --- |
| `prompt-only=31/143` | Completed under `strict-evas`. | Yes, baseline. |
| `rules-only=68/143` | Completed under `strict-evas`; full Spectre parity audited. | Yes, baseline plus evaluator evidence. |
| `evas-repair=70/143` | Completed; weak delta. | Appendix/negative control. |
| `compile-loop=75/143` | Completed. | Yes. |
| `compile-skill-prompt=78/143` | Completed; targeted audit parity. | Yes. |
| `compile-skill-local=80/143` | Completed. | Appendix ablation unless table space allows. |
| `compile-skill-accept=81/143` | Completed; conservative targeted Spectre audit. | Yes. |
| `compile-skill-advanced=83/143` | Completed; R6 targeted audit parity. | Yes, current best. |
| Wrong-function replay | EVAS `1/1`, Spectre `1/1`, mismatch `0/1`; replay only. | Side evidence; not a live result. |

## Retired Or Demoted Work

| Work | Clean status | Reason |
| --- | --- | --- |
| Standalone legacy-92 experiments | Historical only | Current claims use `b143` task-form/core-function breakdowns instead. |
| Fixed-stage/lite/non-strict EVAS | Retired | Not Spectre-faithful enough for main claims. |
| Identity-routed G runs | Retired as claims | Used task identity in retrieval, so not public-only. |
| Current `mechanism-public=76/143` | Diagnostic | Does not meet G compile KPI and does not beat compile-skill path. |
| Current `functional-ir=67/143` | Diagnostic | Does not beat `rules-only`; needs redefinition before rerun. |
| MiMo partial/truncated runs | Diagnostic | Provider reasoning/output controls and token budget need stabilization. |
| Prompt compression | Future optimization | Important for cost, but not part of current method claim. |

## Problems That Need Rerun Or New Evidence

| Problem | Why it matters | Clean experiment plan | Promotion gate |
| --- | --- | --- | --- |
| Live wrong-function regeneration | Current replay proves route, not live model ability. | Run `completion92_calibration_bugfix` with a valid provider using `run_wrong_function_regeneration.py`; validate with `strict-evas` and `spectre-audit`. | Live result passes EVAS and Spectre without task-id templates or hidden gold code. |
| Behavior residual taxonomy | Compile is nearly closed; remaining failures drive next method choice. | Classify residual failures from `compile-skill-advanced` by circuit family, task form, failure axis, and likely mechanism gap. | A ranked behavior-error table that tells whether mechanism cards or IR are worth rerunning. |
| Clean `mechanism-public` | Old accepted G was identity-routed; current public G is weak. | Freeze public-only retrieval from prompt/ports/observables only, run a 10-task smoke, then full `b143` if compile does not regress; compare against `compile-skill-advanced`. | Improvement in behavior correctness after matching compile closure, not just compile fixes. |
| Clean `functional-ir` | Current I underperforms and lacks a clear target. | Rerun only on behavior residual families where IR is expected to help; do targeted audit before any full run. | Targeted residual improvement without compile regression. |
| Cross-model MiMo | Useful robustness evidence, not core method. | Smoke-test no/low reasoning mode, code extraction, token/time accounting; then run `rules-only` and best compile-skill path if stable. | Comparable thinking mode and no systematic output truncation. |
| Prompt compression | Reduces cost but can break public contract. | Segment-aware compression ablation on a small audit slice. | Same pass/failure profile with lower input tokens and no Spectre mismatch. |

## Execution Order

| Step | Run | Purpose | Required now? |
| --- | --- | --- | --- |
| R1 | Live wrong-function regeneration single task | Convert replay evidence into live provider evidence. | Yes, once key is available. |
| R2 | Behavior residual taxonomy on `compile-skill-advanced` | Decide whether G or I is the next real mainline. | Yes; can start without API. |
| R3 | Clean table materialization | Produce final main/appendix tables with canonical names and token/time columns. | Yes. |
| R4 | Clean `mechanism-public` smoke | Test whether mechanism guidance helps behavior after removing identity leakage. | After R2. |
| R5 | Clean `mechanism-public` full `b143` | Only if smoke passes. | Conditional. |
| R6 | Clean `functional-ir` targeted rerun | Only if R2 identifies IR-suitable residual families. | Conditional. |
| R7 | MiMo/cross-model robustness | Generalization evidence. | Later. |
| R8 | Prompt compression | Cost optimization. | Later. |

## Rerun Command Templates

Use the new run-id contract for all reruns.  These commands are templates; keep
provider keys in the environment and do not write them into shell history or
committed files.

### R1: Live Wrong-Function Regeneration

```bash
python3 runners/run_wrong_function_regeneration.py \
  --bench-dir benchmark-balanced \
  --source-generated-dir generated-balanced-CULTRA-WRONGFUNC-GATE-kimi-k2.5-2026-05-03 \
  --source-result-root results/balanced-CULTRA-WRONGFUNC-GATE-kimi-k2.5-quick-2026-05-03 \
  --output-generated-dir generated-targeted1__kimi-k25__both-audit__wrongfunc-live__20260507 \
  --output-root results-targeted1__kimi-k25__both-audit__wrongfunc-live__20260507 \
  --task completion92_calibration_bugfix \
  --model kimi-k2.5 \
  --validation-backend both
```

Promotion gate: the live replacement passes both EVAS and Spectre, and the
manifest records a real provider call rather than replay mode.

### R2: Behavior Residual Taxonomy

Start from the maintained advanced summary:

```text
results/balanced-CULTRA-ADVANCED-skill-acceptreject-kimi-k2.5-spectre-strict-evas-2026-05-03/summary.json
```

Classify each residual failure by:

1. task form: bugfix, dut-only/spec-to-va, end-to-end, tb-generation
2. core function / circuit family: converter, PLL/timer, DWA/DEM, digital
   sequence, source/TB, etc.
3. failure axis: compile, testbench compile, runtime, behavior
4. likely next mechanism: mechanism card, functional IR, checker/task cleanup,
   or cut/no action

This analysis should produce a small table before any new full G/I run.

### R3: Clean Table Materialization

Materialize tables from existing maintained summaries under canonical names.
Do not rerun models for this step.  The output should contain:

```text
results-b143__kimi-k25__strict-evas__clean-main-table__20260507.md
results-b143__kimi-k25__strict-evas__clean-audit-table__20260507.md
```

### R4/R5: Clean `mechanism-public`

Only run after R2 shows behavior residuals that mechanism guidance should
plausibly fix.  The smoke run must verify public-only retrieval: no task id,
task name, directory name, source task id, gold implementation, or checker
internals.

Suggested smoke output naming:

```text
generated-targeted10__kimi-k25__strict-evas__mechanism-public-smoke__20260507
results-targeted10__kimi-k25__strict-evas__mechanism-public-smoke__20260507
```

Full `b143` promotion is conditional on the smoke improving behavior without
compile regression.

## Paper Table Boundary

Use two clean tables:

### Table 1: Main Result

Rows: `prompt-only`, `rules-only`, `compile-loop`, `compile-skill-prompt`,
`compile-skill-accept`, `compile-skill-advanced`.

Columns: `PASS/143`, pass rate, generated count, compile pass rate, sim-correct
rate, avg tokens/task, avg API time/task, notes.

### Table 2: Audits And Diagnostics

Rows: `rules-only spectre-audit`, targeted compile-skill audits,
wrong-function replay, `evas-repair`, `mechanism-public`, `functional-ir`, MiMo
if stabilized.

Columns: scope, EVAS pass, Spectre pass, pass mismatch, failure-domain mismatch,
status, promotion decision.

## Current Mainline Decision

The clean maintained method path is:

```text
prompt-only -> rules-only -> compile-loop -> compile-skill-prompt
           -> compile-skill-accept -> compile-skill-advanced
```

Everything else is either evaluator support, audit evidence, or future behavior
repair.  This keeps the paper from claiming more than the current evidence can
support, while still preserving a clear next-step plan.
