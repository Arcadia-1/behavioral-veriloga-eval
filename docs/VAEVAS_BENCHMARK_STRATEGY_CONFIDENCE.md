# vaEVAS Benchmark Strategy Confidence Audit

**Date**: 2026-05-08

## Strategy Under Review

Use Main120 as the first clean benchmark anchor, run the core model/system
matrix, analyze residuals, then build heldout/stress/v2 based on evidence rather
than expanding blindly.

## Loophole Loop

| Iteration | Potential loophole | Consequence | Mitigation | Confidence after mitigation |
| --- | --- | --- | --- | --- |
| L1 | Main120 is too small for final claims | Results may not generalize | Treat Main120 as v1 anchor, not final universe; require heldout48 before final claims | High for first matrix, not final paper alone |
| L2 | Main120 is too clean/simple | Systems may look better than on realistic tasks | Use residual taxonomy to decide stress/v2 additions; include harder composites later | Medium-high |
| L3 | Benchmark construction may fit current methods | Skill/controller improvements could overfit | Lock heldout before final method selection; do not tune on heldout | High if enforced |
| L4 | Old 143 benchmark content may be discarded too aggressively | Lose valuable edge cases | Keep 143-style pool as source/regression/stress mining pool, not main split | High |
| L5 | Running methods before heldout could bias design | Method choices may adapt to Main120 | Allow Main120 for development, but final claims require heldout transfer | High if tracked |
| L6 | Provider settings may be incomparable | Model comparisons unfair | Run provider smoke; standardize max output, reasoning mode, temperature, worker policy | High after smoke |
| L7 | EVAS may hide Spectre mismatch | False confidence in repair loops | Final metric is Spectre; EVAS used as fast prior only | High |
| L8 | More benchmark expansion might reveal current tasks are flawed | Current matrix may need rerun | Use stop/go gates; if residuals reveal benchmark flaw, patch and rerun affected rows | Medium-high |
| L9 | SFT/RAG decisions may be premature | Adds complexity without evidence | Only consider RAG/SFT after repair traces and residual families justify them | High |
| L10 | Checker contracts are finite | Passing checker is not full analog correctness | State claims as public contract correctness; add stress/heldout for breadth | High for benchmark claims, not theorem claims |

## Machine Strategy Gate

A machine-checkable strategy gate has been added and run:

- Script: `runners/audit_vabench_strategy_gate.py`
- JSON: `analysis/vabench-main-v1_strategy_gate_audit_20260508.json`
- Markdown: `analysis/vabench-main-v1_strategy_gate_audit_20260508.md`
- Result: `PASS`, decision `GO`, failure count `0`

This gate checks Main120 shape, four-form coverage, semantic/integrity audits,
static leakage audit, result coverage audit, full Main120 EVAS, full Main120
Spectre, and tracker state.

## Decision

The strategy is strong enough to proceed to Main120 experiments now.

It is not strong enough to claim final generalization until heldout48 exists and
selected methods transfer to it.

## Required Next Actions

1. Run provider smoke for the model/provider to be used next.
2. Run Main120 A/D/C/S1/S2 under one standardized protocol.
3. Produce residual taxonomy.
4. Decide whether behavior-skill, controller, RAG, prompt compression, or SFT is
   justified by observed residuals.
5. Build and lock heldout48 before final generalization claims.

## Rerun Triggers

Rerun benchmark gates or affected experiment rows if any of these change:

- benchmark prompt/gold/checker files
- strict-EVAS validator or EVAS kernel
- Spectre bridge/profile/environment
- provider reasoning/output/token policy
- code extraction/staging logic
- compile/repair loop protocol
