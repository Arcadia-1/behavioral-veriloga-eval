# vaEVAS Experiment Tracker

**Date**: 2026-05-08

Canonical protocol: `docs/VAEVAS_MAINLINE_PROTOCOL.md`.
Benchmark expansion plan: `docs/VABENCH_MAIN_EXPANSION_PLAN.md`.

| Run ID | Milestone | Purpose | Benchmark | System / Variant | Metrics | Priority | Status | Gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R000 | M0 | bpack48 readiness audit | `benchmark-bpack-v1` | file/manifest audit | artifact completeness, form coverage | MUST | DONE | 48/48 complete; audit JSON written |
| R001 | M0 | prompt-checker-gold contract audit | `benchmark-bpack-v1` | semantic prompt/checker/gold audit | hidden checker leakage, public contract coverage | MUST | DONE_WITH_WARN | hard FAIL cleared; P1 prompt cleanup remains |
| R002 | M0 | vaBench-main coverage table | candidate packs | manual + manifest audit | mechanism/task-form coverage | MUST | DONE | `main-v1=30 packs`, `heldout-v1=12 packs` |
| R003 | M1 | provider smoke for any new model | `vaBench-dev48` subset | A/D smoke | no-code, truncation, token/time, strict-EVAS | MUST | TODO | artifact gate passes |
| R004 | M2 | A prompt-only dev row | `vaBench-dev48` | A | PASS, compile fail, behavior fail, cost | MUST | DONE for MiMo | exact model settings recorded |
| R005 | M2 | D rules-only dev row | `vaBench-dev48` | D | PASS, compile fail, behavior fail, cost | MUST | DONE for MiMo | exact model settings recorded |
| R006 | M2 | C compile-loop dev row | `vaBench-dev48` | C | compile closure, PASS, repair cost | MUST | DONE for MiMo | repair trace available |
| R007 | M2 | S1 compile-skill-prompt dev row | `vaBench-dev48` | S1 | skill prompt delta and cost | MUST | DONE for MiMo | current best full dev row |
| R008 | M2 | S2 compile-skill-accept dev row | `vaBench-dev48` | S2 | local accept/reject delta and cost | MUST | PARTIAL | full replay valid, needs promotion policy |
| R009 | M3 | vaBench-main gold validation | `vaBench-main` | gold | strict-EVAS + Spectre | MUST | MAIN120_GOLD_DONE | main120 full semantic/integrity PASS; full strict-EVAS 120/120; full Spectre 120/120 via bridge profile `jin`; incremental/hash evidence retained |
| R010 | M4 | A/D/C/S1/S2 main rows | `vaBench-main` | core matrix | main pass/failure/cost table | MUST | TODO | same protocol across models |
| R011 | M5 | failure taxonomy | `vaBench-main` residuals | analyzer | failure family by task form/pack | MUST | TODO | identifies behavior residual families |
| R012 | M6 | behavior-skill targeted smoke | compile-passing residuals | B | behavior delta without compile regression | SHOULD | TODO | improves behavior residuals |
| R013 | M7 | controller cost/pass smoke | residual subset | T | PASS, compile closure, token/time Pareto | SHOULD | TODO | beats fixed strategy in cost or pass |
| R014 | M8 | repair-trace RAG smoke | trace dataset | R | top-k retrieval, repair delta, cost | LATER | TODO | trace schema stable |
| R015 | M9 | SFT/DPO feasibility | heldout split | trained small model | heldout pass/cost delta | LATER | TODO | enough clean traces and heldout evidence |
