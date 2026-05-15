# vaEVAS Mainline Plan

## Core Direction

vaEVAS should be developed as two durable assets:

1. **vaBench**: a behavioral Verilog-A benchmark with public prompts, gold implementations, testbenches, checkers, metadata, and EVAS/Spectre validation evidence.
2. **EVAS**: a fast, debuggable evaluator aligned with Spectre on the benchmark-supported pure voltage-domain behavioral subset.

LLM repair workflows, compile skills, controller policies, RAG, token optimization, and local fine-tuning experiments are supporting harnesses only. They should not drive the paper contribution unless the project scope is explicitly reopened.

## Current Assets

The current worktree has two benchmark-like assets that must be kept distinct:

| Asset | Status | Use |
| --- | --- | --- |
| `tasks/` | Source-controlled tree with 92 gold-backed tasks. | Current editable benchmark source. |
| `vabench-main-v1-main120` | Local result evidence under `results/`, with 120/120 gold EVAS and 120/120 gold Spectre pass summaries. | Broad mainline validation evidence until the matching source split is restored/materialized. |
| `benchmark-vabench-main-v1/` | Not present in this worktree. | Do not reference as an editable path unless it is restored. |

See `docs/VABENCH_MAIN_INVENTORY.md` for the frozen inventory and
`docs/VABENCH_MAIN120_MATERIALIZATION.md` for the main120 provenance and
materialization audit. See `docs/VAEVAS_VALIDATION_PIPELINE.md` for validation
gates. See `docs/VAEVAS_EXPERIMENT_RUNBOOK.md` for concrete run IDs,
experiment blocks, and stop/go gates. See
`docs/VABENCH_D001_D004_EXECUTION_PLAN.md` for the accepted D001-D008 checker,
bugfix-provenance, P2 tolerance, prompt-review, promotion-order, and
conformance-split execution plan.

## Benchmark Splits

Use these assets instead of treating heldout construction as the default next milestone:

| Asset | Role | Priority |
| --- | --- | --- |
| `vaBench-main` | Broad paper-facing benchmark and end-to-end EVAS/Spectre validation surface. | Highest |
| EVAS/Spectre conformance regressions | Single-cause tests for syntax, source parsing, event scheduling, timestep sampling, breakpoints, and checker semantics. | Highest |
| Benchmark extensions | New packs that improve circuit/function coverage and can later be promoted into `vaBench-main`. | High |
| Heldout split | Optional future blind/generalization set for leaderboard or method-comparison claims. | Later |

Heldout is a standard benchmark technique when optimizing methods against a dev set, but it is not the most valuable immediate asset for the current benchmark-plus-evaluator direction. The stronger near-term evidence is coverage quality, gold correctness, Spectre validation, and EVAS/Spectre parity.

## EVAS/Spectre Parity Strategy

`vaBench-main` should be used directly for broad parity audits. It answers whether EVAS and Spectre agree on realistic benchmark tasks end to end.

Dedicated EVAS/Spectre conformance tests are still needed because broad benchmark failures are often coupled. A single benchmark task may mix prompt ambiguity, Spectre syntax legality, source parsing, event scheduling, waveform sampling, and checker thresholds. Conformance regressions should isolate one cause per case so a future EVAS change can fail with a precise diagnosis.

"Small and focused" means **atomic and diagnostic**, not permanently tiny. The conformance suite can and should grow when new semantics matter, but each added case should have one clear purpose.

Recommended parity layers:

| Layer | Purpose | Example |
| --- | --- | --- |
| Broad benchmark parity | End-to-end confidence on realistic tasks. | Full `vaBench-main` EVAS/Spectre audit. |
| Atomic conformance regression | Pin one known EVAS/Spectre semantic. | `cross()` exact-threshold touch fires once at the crossing. |
| Syntax legality regression | Ensure strict EVAS rejects code Spectre rejects. | Empty control branch, uncontinued PWL/source line, module header backslash continuation. |
| Stress expansion | Add coverage for solver/event corner cases beyond current benchmark packs. | Coincident timer and PWL edge, transition placement, source breakpoint ordering. |

See `docs/EVAS_SPECTRE_CONFORMANCE_BACKLOG.md` for the first regression
targets.

## Ordered Roadmap

Work should proceed in this order unless new evidence shows a blocker in an earlier layer.

| Order | Workstream | Goal | Main Outputs | Gate to Move On |
| --- | --- | --- | --- | --- |
| 0 | Repository contract and cleanup | Keep the repo aligned with the benchmark + evaluator mainline. | `AGENTS.md`, cleanup manifest, ignore rules for generated runs. | Status is readable; generated artifacts are not polluting source diffs. |
| 1 | `vaBench-main` inventory | Establish the current benchmark as the paper-facing source of truth. | Coverage table, task taxonomy, main120 provenance/materialization map, gold-validation index, known-limitations list. | Every included task has clear metadata, checks, gold status, and EVAS/Spectre evidence. |
| 2 | Validation pipeline lock | Make benchmark promotion reproducible. | One-command or documented flows for semantic checks, strict EVAS, Spectre validation, and result summarization. | A new or changed gold task cannot be promoted without fresh validation evidence. |
| 3 | Broad EVAS/Spectre parity gate | Use `vaBench-main` directly to measure end-to-end evaluator agreement. | Full benchmark parity table with binary PASS/FAIL agreement, failure labels, and representative logs. | Current audited slices maintain zero EVAS PASS / Spectre FAIL mismatches. |
| 4 | Atomic conformance regressions | Turn known and future mismatches into diagnostic tests. | Dedicated syntax, source, event, sampling, breakpoint, and checker regression cases. | Each historical mismatch has a single-cause regression or a documented reason it is out of scope. |
| 5 | EVAS parity fixes | Fix evaluator behavior where conformance or broad parity exposes real EVAS/Spectre disagreement. | EVAS patches, targeted tests, updated parity report. | Fixes pass atomic conformance tests and do not regress `vaBench-main` broad parity. |
| 6 | Benchmark expansion | Grow toward roughly 200 paper-facing tasks while preserving validation quality. | New packs, prompts, gold Verilog-A, testbenches, checkers, and coverage deltas. | Each expansion batch passes semantic checks, strict EVAS, and Spectre validation before promotion. |
| 7 | Simulator stress expansion | Add dedicated tests proving EVAS is useful beyond simply replaying current tasks. | Stress cases for event ordering, PWL/source breakpoints, `cross()`, `timer()`, `transition()`, and checker semantics. | Each stress case maps to a real simulator semantic and has both expected behavior and debug value. |
| 8 | Minimal model baselines | Use LLMs to stress the benchmark without making workflow engineering the contribution. | Prompt-only, EVAS-feedback, and optional Spectre-feedback baseline rows. | Baselines support the benchmark/evaluator claims without requiring bespoke controller claims. |
| 9 | Paper package | Convert validated assets into claims, figures, and tables. | Benchmark description, coverage figures, EVAS/Spectre parity table, speed/debug evidence, limitation section. | Every paper claim traces to a validation artifact or a documented limitation. |
| 10 | Optional heldout/leaderboard | Add blind evaluation only after main coverage and parity are strong. | Heldout split or public leaderboard protocol. | Needed only if making generalization or method-comparison claims that require a blind split. |

## Immediate Work Order

1. Materialize `vabench-main-v1-main120` from result evidence into a source-backed split. Treat this as provenance/source recovery, not as "92 existing plus 28 missing": the current `tasks/` IDs and main120 `vbm1_*` IDs are different assets.
2. Build a compact `vaBench-main` parity report that separates binary EVAS/Spectre agreement from failure taxonomy.
3. Create the first conformance-regression pack from historical mismatches:
   - empty control branch syntax legality,
   - uncontinued multiline source/PWL syntax legality,
   - `$abstime`/continuous-decay solver-time behavior,
   - any current residual event/sampling mismatch found by the broad gate.
4. Define promotion rules for new benchmark tasks: metadata completeness, checker determinism, strict EVAS result, Spectre result, and manual review note.
5. Expand benchmark coverage in batches instead of one large dump. A practical cadence is 20-40 tasks per batch, each batch ending with validation and a coverage delta.
6. Add simulator stress cases only when they teach a distinct EVAS/Spectre semantic; do not add near-duplicate workflow failures.
7. Keep baseline experiments intentionally simple until the benchmark and EVAS parity story is stable.

## Success Criteria

- Benchmark gold tasks pass semantic/integrity checks and both EVAS/Spectre validation.
- Current audited benchmark slices maintain zero EVAS PASS / Spectre FAIL binary mismatches.
- Dedicated conformance regressions explain known parity risks with single-cause tests.
- Workflow experiments remain optional harness evidence rather than primary claims.
