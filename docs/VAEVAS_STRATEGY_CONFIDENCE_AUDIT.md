# vaEVAS Strategy Confidence Audit

**Date**: 2026-05-08

## Verdict

The original direction is sound but not sufficient as stated.  The revised
strategy reaches practical high confidence only after these changes:

1. `bpack48` is demoted to a development benchmark.
2. `vaBench-main` and `vaBench-heldout` are required before paper-facing
   generalization claims.
3. Gold generation is treated as `agentic-upper-bound`, not a fair baseline.
4. Conditions are reduced to A/D/C/S1/S2/B/T/R/O.
5. PASS rates must be reported with failure family, model settings, token/time,
   and Spectre audit scope.

## Red-Team Loop

| Iteration | Vulnerability | Failure mode | Repair | Residual risk |
| --- | --- | --- | --- | --- |
| 1 | Small benchmark | `21/48` vs `19/48` may be variance. | Use `bpack48` for dev only; build `vaBench-main` and heldout. | Main benchmark still needs construction work. |
| 2 | Prompt/checker mismatch | Model is punished for hidden requirements. | Require prompt-checker-gold audit before freeze. | Manual review still needed for semantic completeness. |
| 3 | Gold from Codex | Agentic construction is confused with one-shot model ability. | Label gold/Codex as upper bound unless rerun under A. | Need clean GPT-5.5 A row if claimed. |
| 4 | EVAS/Spectre mismatch | Fast validator could optimize wrong behavior. | Use Spectre audit on gold, high-impact deltas, representative slices. | Full Spectre for every row may be too expensive. |
| 5 | Skill overfitting | More skills memorize current residuals. | Promote only public-trigger, generalizable skills with heldout evidence. | Some manual skill design remains domain-specific. |
| 6 | Opaque condition names | Results become unreviewable. | Canonical A/D/C/S1/S2/B/T/R/O names. | Historical docs still need cleanup pointers. |
| 7 | PASS-only metrics | Compile closure can worsen behavior or cost. | Require failure taxonomy and cost/pass Pareto. | Tables get wider; need careful presentation. |
| 8 | Early RAG/SFT | Training fits noisy traces or benchmark specifics. | Delay until trace schema, main benchmark, and heldout are frozen. | May slow exciting model-improvement work, but protects validity. |

## Current Confidence

I would not claim literal 100% certainty.  I would claim the revised strategy is
factually robust enough to execute because every known major validity threat now
has a concrete gate:

```text
benchmark gate -> protocol gate -> provider gate -> validation gate ->
failure-taxonomy gate -> heldout/generalization gate
```

If a future result cannot pass these gates, it remains diagnostic rather than a
main claim.

## Immediate Must-Do List

1. Finish prompt-checker-gold audit for `bpack48` beyond file presence.
2. Build `vaBench-main` coverage table with candidate packs and heldout split.
3. Freeze model/provider protocol for MiMo/Kimi/future models.
4. Keep running dev experiments only when they answer a specific gate question.
5. Avoid adding more compile skills unless they are public-trigger and heldout-promotable.
