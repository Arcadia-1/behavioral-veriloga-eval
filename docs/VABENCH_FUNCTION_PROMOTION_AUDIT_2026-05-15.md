# vaBench Function Promotion Audit

Date: 2026-05-15

## Purpose

This audit records why the former expansion list is no longer just a loose
candidate pool. The selected functions have been promoted into the top-level
release coverage contract, while scoring remains gated by task materialization
and EVAS/Spectre certification.

## Current Decision

| Pool | Count | Decision |
| --- | ---: | --- |
| Current promoted L1 seeds | 28 | Keep as current seed functions after duplicate/removal policy. |
| Promoted top-level L1 additions | 32 | Add directly to the main release taxonomy as selected coverage targets. |
| Selected L2 complete-circuit targets | 20 | Add directly to the main release taxonomy as selected composition targets. |
| Top-level L1/L2 coverage target | 80 | Use as the planning denominator before task-form multiplication. |
| Scored release tasks | TBD | Count only after prompt, metadata, checks, gold, and EVAS/Spectre evidence are complete. |

This resolves the earlier ambiguity: these functions are not "maybe useful
candidates" anymore. They are selected target functions. They are just not
certified scored tasks yet.

## Promotion Filters

A function can be selected into the main table only if all filters pass:

| Filter | Requirement | Failure action |
| --- | --- | --- |
| Circuit relevance | It names a recognizable analog/mixed-signal IC behavioral block or reusable testbench/instrumentation block. | Defer or delete. |
| Scope fit | It fits the pure voltage-domain, event-driven behavioral Verilog-A subset. | Move to future scope or L0 conformance. |
| Non-duplication | It is not only a renamed version of an existing kernel. | Merge into the canonical function. |
| Observable contract | It has an obvious public behavior that a checker can measure without leaking the gold implementation. | Keep as research note, not release target. |
| L1/L2 separation | L1 is one reusable function; L2 composes multiple interacting functions or a complete flow. | Reclassify before promotion. |
| Helper boundary | Pure parser, file-schema, source-continuation, or final-row semantics are not counted as L1/L2 functions. | Move to L0 conformance. |
| IC terminology | Names match common mixed-signal terminology such as DAC, ADC quantizer, comparator, PFD, DWA/DEM, VCO, sample/hold, filter, limiter, and calibration loop. | Rename before promotion. |
| Certification gate | Scoring requires reviewed prompt/meta/checks/gold plus EVAS and Spectre validation. | Keep as selected target only. |

## Confidence Loop

| Iteration | Strategy | Main loophole found | Fix applied |
| --- | --- | --- | --- |
| 0 | Keep all extracted functions as candidates. | Too weak: agents can keep asking whether candidates count, and row count can drift. | Split selected coverage targets from deferred variants. |
| 1 | Promote every extracted function. | Too risky: helper syntax, duplicate kernels, and over-digital toy blocks would inflate coverage. | Add promotion filters for scope, observability, non-duplication, and helper boundary. |
| 2 | Promote only filtered functions into the main table, but do not score them yet. | Good planning contract, but scoring could still be over-claimed. | Explicitly state materialization/certification gate in taxonomy, registry, and positioning docs. |
| 3 | Align all count vocabulary across docs. | Old "56 candidates" wording remained and contradicted the new policy. | Replace with 28 current seeds + 32 selected L1 additions + 20 selected L2 targets = 80 top-level target. |

## Remaining Risks And Guards

| Risk | Why it matters | Guard |
| --- | --- | --- |
| Duplicate behavioral kernels under new names. | Inflates function coverage without adding capability coverage. | Keep `VABENCH_BASE_FUNCTION_REGISTRY` as the current-seed dedup layer and require a review note for every new function. |
| L2 name but L1 behavior. | Makes an e2e wrapper look like a system benchmark. | L2 must name interacting components, not only a longer testbench. |
| Measurement/stimulus helper leakage. | Could turn checker/source mechanics into benchmark tasks. | Count only reusable measurement or source models; move parser/schema/source syntax to L0. |
| EVAS unsupported semantics. | Would make the benchmark depend on behavior outside the stated evaluator scope. | Keep additions voltage-domain/event-driven; current-domain/KCL/KVL/device-level behavior stays out of scope. |
| Paper wording overclaim. | "80 functions" could be misread as "80 certified tasks already exist." | Use "top-level coverage target" until tasks are materialized and validated. |
| Weak checkers. | A function can be nominally present but behaviorally under-tested. | Every promoted task needs a checker tied to its prompt observables. |

## Practical Confidence Verdict

The strategy is not mathematically 100% certain, because benchmark quality still
depends on future prompt/checker/gold review. It is, however, practically
safe enough for the next build loop:

- The selected functions now live in the main release taxonomy.
- The old loose-candidate count is removed from current planning vocabulary.
- The score boundary remains protected by certification gates.
- Known loopholes have explicit guards and failure actions.

Therefore, use the 80-entry top-level L1/L2 coverage target for planning, and
use certified materialized tasks only for benchmark scores.
