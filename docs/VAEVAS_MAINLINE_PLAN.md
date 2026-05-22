# vaEVAS Mainline Plan

## Core Direction

vaEVAS should be developed as two durable assets:

1. **vaBench**: a behavioral Verilog-A benchmark with public prompts, gold implementations, testbenches, checkers, metadata, and EVAS/Spectre validation evidence.
2. **EVAS**: a fast, debuggable evaluator aligned with Spectre on the benchmark-supported pure voltage-domain behavioral subset.

LLM repair workflows, compile skills, controller policies, RAG, token optimization, and local fine-tuning experiments are supporting harnesses only. They should not drive the paper contribution unless the project scope is explicitly reopened.

Paper-safe current wording:

> We release vaBench as a complete behavioral Verilog-A benchmark organized by
> circuit function and task form. Each released task contains a public prompt,
> metadata, checker, gold Verilog-A/testbench assets, and EVAS/Spectre
> certification evidence. L1/L2 circuit-function tasks form the scored
> benchmark surface; L0 primitive cases form a separate EVAS/Spectre
> conformance suite. EVAS is the fast routine/debug evaluator, while Spectre
> remains the reference for row certification, gold promotion, and
> paper-facing claims.

## Release Target And Internal Assets

The paper-facing object is the clean vaBench release package, not any historical
experimental directory. Existing rows, examples, and legacy task trees are
internal construction material only: use them for gap analysis, provenance, and
regression evidence, but do not cite them as the benchmark definition.

| Asset | Status | Use |
| --- | --- | --- |
| Clean `vaBench` release package | Target artifact. | Final benchmark definition: task dirs, schemas, evaluator contract, and certification evidence. |
| `docs/VABENCH_TOPLEVEL_POSITIONING.md` | Top-level release wording. | Defines the paper-facing scoring surfaces, category roles, and duplicate/naming policy. |
| `docs/VABENCH_RELEASE_TAXONOMY.md` | Clean release taxonomy. | Paper-facing category/function/level contract without historical source-trace wording. |
| `docs/VABENCH_BASE_FUNCTION_REGISTRY.md` and `.csv` | Base-function counting registry. | Prevents duplicate kernels, weak e2e forms, evidence-only rows, and historical category hints from inflating release claims. |
| `docs/VABENCH_LEVEL_COVERAGE_TABLE.md` | Human-review L0/L1/L2 map. | Shows concrete circuits under the nine categories and separates current L1 seeds from L2 expansion targets. |
| `docs/VABENCH_FUNCTION_PROMOTION_AUDIT_2026-05-15.md` | Promotion confidence audit. | Records why selected additions are now top-level coverage targets while scoring remains certification-gated. |
| `docs/VABENCH_TAXONOMY_TABLE_AUDIT_2026-05-15.md` | Taxonomy naming/duplication audit. | Records duplicate-risk, naming, necessity, and literature-supported terminology decisions. |
| `docs/VABENCH_TOPDOWN_FUNCTION_TAXONOMY.md` | Design spec for the target release. | Defines circuit-function coverage, L0/L1/L2 levels, and task-form rules. |
| EVAS/Spectre certification evidence | Required per released task. | Proves gold/checker behavior and evaluator parity. |
| Historical validated inventories | Internal construction material. | Reuse validated assets where they fit the release spec; do not let them define coverage. |

See `docs/VABENCH_TOPLEVEL_POSITIONING.md` for the top-level paper-facing
口径, `docs/VABENCH_RELEASE_TAXONOMY.md` for the clean release contract,
`docs/VABENCH_BASE_FUNCTION_REGISTRY.md` for base-function counting decisions,
`docs/VABENCH_LEVEL_COVERAGE_TABLE.md` for the current L0/L1/L2 review table,
`docs/VABENCH_FUNCTION_PROMOTION_AUDIT_2026-05-15.md` for the selected-function
promotion audit,
`docs/VABENCH_TAXONOMY_TABLE_AUDIT_2026-05-15.md` for naming and
duplication-risk audit decisions, `docs/VABENCH_TOPDOWN_FUNCTION_TAXONOMY.md`
for construction rationale,
`docs/VABENCH_MAIN120_MATERIALIZATION.md` for retained historical evidence
provenance, `docs/VAEVAS_VALIDATION_PIPELINE.md` for validation gates,
`docs/EVAS_SPECTRE_CONFORMANCE_BACKLOG.md` for atomic parity regressions, and
`docs/VABENCH_D004_BUGFIX_TRIAGE.md` plus
`docs/VABENCH_P2_TOLERANCE_POLICY.md` for retained bugfix/conformance policy.

## Benchmark Splits

Use these assets instead of treating heldout construction as the default next milestone:

| Asset | Role | Priority |
| --- | --- | --- |
| Clean vaBench release package | Paper-facing benchmark: task dirs, public prompts, gold/checkers, schemas, and certification evidence. | Highest |
| Top-down function taxonomy | Coverage contract: large circuit types, required L1/L2 functions, and complete circuit forms. | Highest |
| EVAS/Spectre L0 conformance regressions | Single-cause tests for syntax, source parsing, event scheduling, timestep sampling, breakpoints, and checker semantics. Report separately from benchmark score. | Highest |
| Benchmark extensions | New L1/L2 functions and task forms that improve circuit/function coverage and can later be promoted into `vaBench-main`. | High |
| Historical evidence inventories | Internal source of reusable gold/checker/evidence material. | Supporting |
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
| 1 | Complete vaBench specification | Establish the paper-facing benchmark ontology and release package contract. | Top-down function table, L0/L1/L2 rules, task-form schema, evaluator/result schema, duplicate/gap list. | Every released task has clear metadata, checks, gold status, EVAS/Spectre evidence, and a taxonomy placement. |
| 2 | Validation pipeline lock | Make benchmark promotion reproducible. | One-command or documented flows for semantic checks, strict EVAS, Spectre validation, and result summarization. | A new or changed gold task cannot be promoted without fresh validation evidence. |
| 3 | Broad EVAS/Spectre parity gate | Use `vaBench-main` directly to measure end-to-end evaluator agreement. | Full benchmark parity table with binary PASS/FAIL agreement, failure labels, and representative logs. | Current audited slices maintain zero EVAS PASS / Spectre FAIL mismatches. |
| 4 | Atomic conformance regressions | Turn known and future mismatches into diagnostic tests. | Dedicated syntax, source, event, sampling, breakpoint, and checker regression cases. | Each historical mismatch has a single-cause regression or a documented reason it is out of scope. |
| 5 | EVAS parity fixes | Fix evaluator behavior where conformance or broad parity exposes real EVAS/Spectre disagreement. | EVAS patches, targeted tests, updated parity report. | Fixes pass atomic conformance tests and do not regress `vaBench-main` broad parity. |
| 6 | Benchmark expansion | Grow missing L1/L2 circuit functions first, then add task forms, while preserving validation quality. | New packs, prompts, gold Verilog-A, testbenches, checkers, and coverage deltas. | Each expansion batch passes semantic checks, strict EVAS, and Spectre validation before promotion. |
| 7 | Simulator stress expansion | Add dedicated tests proving EVAS is useful beyond simply replaying current tasks. | Stress cases for event ordering, PWL/source breakpoints, `cross()`, `timer()`, `transition()`, and checker semantics. | Each stress case maps to a real simulator semantic and has both expected behavior and debug value. |
| 8 | Minimal model baselines | Use LLMs to stress the benchmark without making workflow engineering the contribution. | Prompt-only, EVAS-feedback, and optional Spectre-feedback baseline rows. | Baselines support the benchmark/evaluator claims without requiring bespoke controller claims. |
| 9 | Paper package | Convert validated assets into claims, figures, and tables. | Benchmark description, coverage figures, EVAS/Spectre parity table, speed/debug evidence, limitation section. | Every paper claim traces to a validation artifact or a documented limitation. |
| 10 | Optional heldout/leaderboard | Add blind evaluation only after main coverage and parity are strong. | Heldout split or public leaderboard protocol. | Needed only if making generalization or method-comparison claims that require a blind split. |

## Immediate Work Order

1. Freeze the top-down function taxonomy as the benchmark construction surface: large circuit types, required L1/L2 functions, complete circuit forms, and optional task forms.
2. Build the clean `vaBench` release package with one evaluator/result schema and explicit links from each released task to gold, checker, metadata, and EVAS/Spectre certification evidence.
3. Reuse historical validated rows only when they satisfy the release spec. Close duplicate/gap decisions before expanding row count so old experiment kernels cannot inflate coverage claims.
4. Keep historical inventories as internal traceability material; avoid paper-facing wording that cites construction artifacts as the benchmark basis.
5. Maintain the L0 EVAS/Spectre conformance pack separately from the scored L1/L2 benchmark. Start from historical mismatches:
   - empty control branch syntax legality,
   - uncontinued multiline source/PWL syntax legality,
   - `$abstime`/continuous-decay solver-time behavior,
   - any current residual event/sampling mismatch found by the broad gate.
6. Define promotion rules for new L1/L2 benchmark tasks: metadata completeness, checker determinism, strict EVAS result, Spectre result, taxonomy placement, and manual review note.
7. Expand benchmark coverage in batches by missing circuit functions first, not by row count first. A practical cadence is 20-40 tasks per batch, each batch ending with validation and a coverage delta.
8. Add simulator stress cases only when they teach a distinct EVAS/Spectre semantic; do not add near-duplicate workflow failures.
9. Keep baseline experiments intentionally simple until the benchmark and EVAS parity story is stable.

## Current Experiment Plan

The next experiments should close paper-facing claim gates in dependency order.
Do not run model baselines or claim EVAS speed until their denominator and
same-slice evidence gates are ready.

| Phase | Experiment | Goal | Inputs | Outputs | Pass Gate |
| --- | --- | --- | --- | --- | --- |
| P0 | Report source-of-truth audit | Remove status conflicts across release reports. | `manifest.json`, `dual_certification.json`, `score_denominator_manifest.json`, `claim_gate.json`, `paper_artifacts.json`, Markdown exports. | One consistent authoritative status table; stale/import-only reports clearly labeled. | No report implies a stronger claim than the claim gate allows. |
| P1 | Score denominator enablement | Decide what enters benchmark scores. | Certified release entries/forms and content audit exclusions. | Enabled nonzero counted rows, preferably entry-level main denominator with form-level diagnostic appendix. | `score_denominator_manifest.json` has nonzero counted entries/forms and excludes known duplicate/shallow rows. |
| P2 | L2 checker-strength audit | Ensure L2 rows test composed behavior rather than thin wrappers. | All 15 L2 rows, public prompts, checks, gold modules, content audit table. | Strengthened checks or auxiliary labels for shallow rows. | Each scored L2 row has at least two behavior-level observables tied to interacting functions or complete flow behavior. |
| P3 | Same-slice EVAS/Spectre speed measurement | Prove whether EVAS is faster than Spectre on the certified release slice. | Same staged DUT/TB/checker rows for EVAS and Spectre, machine/bridge/Cadence config. | `speed_debug_artifact.json`, `paper_tables/speed_baseline.csv`, timing summary. | Nonzero timed rows, zero EVAS PASS / Spectre FAIL mismatches, and reported total/median/p25/p75 speedup. |
| P4 | Minimal model baseline | Show vaBench differentiates model capability. | Enabled score denominator and certified release rows. | Prompt-only baseline, EVAS-feedback repair baseline, failure taxonomy. | Baseline artifact reports pass rates on counted rows only, with Spectre as final judge. |
| P5 | Optional agent feedback protocol | Support modern verifier-in-the-loop comparisons without making workflow engineering the contribution. | Static/EVAS checker feedback schema and baseline outputs. | Standardized feedback JSON and limited retry protocol. | Results are clearly labeled as engineering baselines, not core method claims. |
| P6 | Paper artifact freeze | Convert gates into paper claims. | Coverage, parity, speed, baseline, and limitation artifacts. | Paper tables, figure specs, claim-gated wording. | Every table cell traces to a current artifact and no blocked claim appears in text. |

Speed measurement should use these formulas:

```text
speedup_i = T_spectre_i / T_evas_i
total_speedup = sum_i T_spectre_i / sum_i T_evas_i
median_speedup = median_i(speedup_i)
geo_mean_speedup = exp(mean_i(log(speedup_i)))
```

Minimum speed table columns:

```text
row_count
evas_total_wall_time_s
spectre_total_wall_time_s
total_speedup
median_speedup
p25_speedup
p75_speedup
evas_pass_spectre_fail_count
machine_or_bridge_config
```

Safe speed wording before P3 passes:

> EVAS is designed as the routine/debug evaluator, while Spectre remains the
> reference simulator. EVAS speedup is a pending same-slice measurement claim.

Safe speed wording after P3 passes:

> On the certified same-slice vaBench release subset, EVAS achieves Xx
> wall-clock speedup over Spectre while preserving zero EVAS PASS / Spectre FAIL
> mismatches.

## Success Criteria

- Benchmark gold tasks pass semantic/integrity checks and both EVAS/Spectre validation.
- Current audited benchmark slices maintain zero EVAS PASS / Spectre FAIL binary mismatches.
- Dedicated conformance regressions explain known parity risks with single-cause tests.
- Paper-facing benchmark scores use L1/L2 circuit-function tasks; L0 conformance is reported separately as evaluator health evidence.
- EVAS speed/debug claims use same-slice timing evidence rather than historical summaries.
- Workflow experiments remain optional harness evidence rather than primary claims.
