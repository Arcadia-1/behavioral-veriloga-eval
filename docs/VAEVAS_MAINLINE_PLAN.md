# vaEVAS Mainline Plan

## Core Direction

vaEVAS should be developed as two durable assets:

1. **vaBench**: a behavioral Verilog-A benchmark with public prompts, gold implementations, testbenches, checkers, metadata, and EVAS/Spectre validation evidence.
2. **EVAS**: a fast, debuggable evaluator aligned with Spectre on the benchmark-supported pure voltage-domain behavioral subset.

LLM repair workflows, compile skills, controller policies, RAG, token optimization, and local fine-tuning experiments are supporting harnesses only. They should not drive the paper contribution unless the project scope is explicitly reopened.

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

## Near-Term Plan

1. Consolidate `vaBench-main` documentation: coverage, task forms, gold evidence, known limitations.
2. Expand benchmark packs toward roughly 200 paper-facing tasks while preserving gold EVAS/Spectre validation.
3. Convert every historical EVAS/Spectre mismatch into an atomic conformance or syntax regression.
4. Use full `vaBench-main` as the periodic broad parity gate.
5. Add dedicated EVAS/Spectre stress cases when they cover new simulator semantics, not just more workflow failures.
6. Keep LLM baselines minimal and model-agnostic: prompt-only/rules-only/compile-feedback rows are enough to stress the benchmark.

## Success Criteria

- Benchmark gold tasks pass semantic/integrity checks and both EVAS/Spectre validation.
- Current audited benchmark slices maintain zero EVAS PASS / Spectre FAIL binary mismatches.
- Dedicated conformance regressions explain known parity risks with single-cause tests.
- Workflow experiments remain optional harness evidence rather than primary claims.
