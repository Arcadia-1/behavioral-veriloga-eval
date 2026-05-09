# vaEVAS Handoff: Compile Closure to Behavior Repair - 2026-05-09

This file is intended as a clean new-window handoff. It summarizes what is now reliable, what should be removed from the active mainline, and what the next research direction should be.

## One-Sentence Project Direction

vaEVAS is now best framed as a Spectre-aligned fast validation and repair environment for Verilog-A generation: use EVAS for cheap iterative diagnosis and candidate filtering, use Spectre for final audit, and move from compile-closure repair toward behavior-level repair.

## Current Mainline

The current mainline should be:

```text
Main120 benchmark gate
  -> Spectre-aligned EVAS validation
  -> A/D/C/S1/S2 compile strategy matrix
  -> T1 residual compile fallback only when S2 stalls
  -> R0 repair trace memory
  -> behavior-repair controller B1
  -> heldout/generalization
```

The next main research bottleneck is not generic compile repair. It is behavior repair after compile success.

## Reliable Results So Far

### Main120 Compile Strategy Matrix

Model setting: `mimo-v2.5-pro`, reasoning disabled, `max_tokens=4096`. Final metric is Spectre.

| row | PASS | compile OK | compile fail | behavior fail | DUT compile fail | TB compile fail |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A Spectre | 20/120 | 48/120 | 72/120 | 28/120 | 46 | 26 |
| D Spectre | 21/120 | 76/120 | 44/120 | 55/120 | 32 | 12 |
| C Spectre | 24/120 | 92/120 | 28/120 | 68/120 | 19 | 9 |
| S1 Spectre | 28/120 | 108/120 | 12/120 | 80/120 | 6 | 6 |
| S2 Spectre | 29/120 | 110/120 | 10/120 | 81/120 | 6 | 4 |

Interpretation:

- `D` rules-only improves compile closure strongly over `A`, but barely improves PASS.
- `C` compile-loop adds modest PASS and compile closure.
- `S1` compile-skill prompt improves compile closure further.
- `S2` deterministic skill accept/reject is the best compile-first pass so far: slightly better than S1 and cheaper because it makes no LLM calls for selected skill fixes.

### T1 Residual Compile Fallback

T1 starts from the 10 S2 Spectre compile-fail residuals and uses online LLM plan-execute repair with EVAS accept/reject and targeted Spectre audit.

| row | PASS | compile OK | compile fail | behavior fail | DUT compile fail | TB compile fail |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| S2 residual slice | 0/10 | 0/10 | 10/10 | 0/10 | 6 | 4 |
| T1 Spectre slice | 1/10 | 7/10 | 3/10 | 6/10 | 2 | 1 |

Main120 targeted-splice estimate:

| row | PASS | compile OK | compile fail | behavior fail |
| --- | ---: | ---: | ---: | ---: |
| S2 full Spectre | 29/120 | 110/120 | 10/120 | 81/120 |
| S2 + T1 targeted splice | 30/120 | 117/120 | 3/120 | 87/120 |

Interpretation:

- T1 is useful as a fallback for S2's closed-world limitation.
- T1 should not replace S2 because it costs more: 28 API calls, 112405 total tokens, 214.088 API seconds on only 10 tasks.

### T2 Residual Compile Retry

T2 retries T1-style LLM fallback only on the three T1 residual compile failures.

| row | PASS | compile OK | compile fail | behavior fail | DUT compile fail | TB compile fail |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 residual slice | 0/3 | 0/3 | 3/3 | 0/3 | 2 | 1 |
| T2 Spectre slice | 0/3 | 0/3 | 3/3 | 0/3 | 2 | 1 |

Interpretation:

- Generic extra LLM compile looping has hit diminishing returns.
- `offset_comparator_e2e` is not a clean AHDL syntax compile failure: Spectre log completes with 0 errors, but validator reports missing data/tran output.
- The two integrator residuals contain invalid `$abstime_step`; this is a targeted language/operator issue, not something generic looping solved.

### R0 Repair Trace Index

R0 extracted repair traces from C/S1/S2/T1 artifacts.

| metric | value |
| --- | ---: |
| trace entries | 278 |
| unique tasks | 120 |
| C entries | 120 |
| S1 entries | 120 |
| S2 entries | 28 |
| T1 entries | 10 |
| warnings | 0 |

Interpretation:

- R0 is now the right base for memory/RAG/SFT/RL-style future work.
- The next controller should retrieve compact repair trace cards instead of endlessly adding new hand-written skills.

### CTX1 Compact Diagnostics

CTX1 repeated the T1 10-task slice with `--compile-compact-diagnostics`, which removes verbose validator notes from compile prompts.

| row | PASS | compile OK | compile fail | behavior fail |
| --- | ---: | ---: | ---: | ---: |
| T1 Spectre | 1/10 | 7/10 | 3/10 | 6/10 |
| CTX1 Spectre | 1/10 | 7/10 | 3/10 | 6/10 |

Cost:

| row | API calls | input tokens | output tokens | total tokens |
| --- | ---: | ---: | ---: | ---: |
| T1 | 28 | 102426 | 9979 | 112405 |
| CTX1 | 34 | 120719 | 13495 | 134214 |

Interpretation:

- CTX1 preserved final outcome but increased total token cost because several tasks needed extra rounds.
- Simple raw-note deletion is not a good compression method.
- Better context engineering should use structured diagnostic compression plus R0 repair trace cards.

### B1 Behavior Smoke Selection

B1 selected 10 S2 Spectre behavior failures for behavior-repair controller smoke.

| property | value |
| --- | ---: |
| selected tasks | 10 |
| compile failures selected | 0 |
| core functions covered | 9 |
| task forms | bugfix 2, spec-to-va 6, tb-generation 2 |

The B1 tasklist is `tasklists/B1_behavior_repair_smoke_20260509.txt`.

## What to Remove from Active Mainline

These should not be deleted as files, because they are useful evidence, but they should be removed from the active forward path.

| Item | Mainline status | Reason |
| --- | --- | --- |
| More generic T1/T2 compile-loop retries | remove from active path | T2 did not improve final Spectre status; final residuals need targeted handling, not more generic rounds. |
| Naive CTX1 raw-note deletion | remove from active path | It preserved outcome but increased total tokens; compression must be structured, not blind deletion. |
| Unbounded compile-skill accumulation | remove from active path | This risks overfitting benchmark-specific patterns; use R0 trace memory and public-feature routing instead. |
| Old bpack48 controller smoke rows | appendix only | Useful history, but Main120 is the current main evidence base. |
| Legacy 92-only framing | appendix/calibration only | Main120 is the cleaner current benchmark; 92 can explain ancestry but should not drive the main paper. |
| Full-run-by-default after small changes | remove from workflow | Prefer targeted regression + splice, with full checkpoint only at milestone boundaries. |
| Prompt-only rule inflation | remove from optimization path | D used far more input tokens than A while adding only one Spectre PASS; future prompt work must be selective/compressed. |

## Current Strategic Decision

The compile side is now close to diminishing returns:

- S2 reduces compile fail to 10/120.
- T1 targeted-splice estimate reduces compile fail to 3/120.
- T2 does not close the remaining 3 under final Spectre validator status.

Therefore the next work should prioritize behavior repair:

```text
B1 behavior controller smoke
  -> behavior metric gap diagnosis
  -> targeted EVAS subchecks
  -> compile-preserving behavior patch
  -> EVAS behavior gate
  -> targeted Spectre audit
```

## Immediate Next Experiments

### B1: Behavior-Repair Controller Smoke

Goal: prove that behavior repair can improve compile-OK failures without reintroducing compile errors.

Input: `tasklists/B1_behavior_repair_smoke_20260509.txt`.

Protocol:

1. Start from S2 generated candidates for the 10 selected behavior failures.
2. Keep only compile-OK tasks.
3. Build a compact behavior gap summary from checker metrics and waveform summaries.
4. Ask LLM for a behavior diagnosis and minimal patch plan.
5. Execute one patch.
6. Run EVAS compile-preserving gate first.
7. Only if compile remains OK, evaluate behavior metrics.
8. Run targeted Spectre audit for accepted candidates.

Required table:

| row | PASS | compile OK | compile fail | behavior fail | compile regression | token/time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |

Success criterion:

- No compile regressions on accepted candidates.
- At least some checker metrics improve.
- Any Spectre PASS gain is strong evidence but not required for first smoke.

### R1/CTX2: Trace-Card Context Compression

Goal: replace naive CTX1 with useful compact context.

Protocol:

1. Retrieve top-k R0 traces by normalized failure family and task form.
2. Convert them into short trace cards:
   - failure atom
   - accepted fix idea
   - rejected fix warning
   - EVAS/Spectre delta
3. Keep structured validator atoms instead of raw long notes.
4. Compare against T1 on the same 10 residual tasks.

Success criterion:

- Lower input tokens than T1.
- No worse compile closure than T1.
- Fewer extra rounds than CTX1.

### Targeted Cleanup: Three Residual Compile Cases

Do not run another generic LLM loop. Instead:

- `offset_comparator_e2e`: inspect validator/output extraction because Spectre completes with 0 simulator errors but validator reports data/tran missing.
- `resettable_integrator_bugfix`: forbid `$abstime_step` and require Spectre-compatible integration style.
- `vco_phase_integrator_bugfix`: same `$abstime_step` issue plus conditional `transition()`; needs targeted operator/semantic repair.

## Risk Loop

### Initial Confidence

Not 100%. The strategy is strongly supported by current evidence, but there are still important risks.

### Risk 1: Behavior Repair May Overfit the 10-Task B1 Slice

Why it matters: B1 may learn task-specific behavior fixes that do not transfer.

Mitigation:

- Use only public prompt/ports/checker/waveform metrics, never task-id routing.
- Keep B1 as smoke only, then require heldout behavior transfer.
- Track behavior families and report per-family outcomes.

Residual risk after mitigation: medium.

### Risk 2: EVAS Behavior Metrics May Not Match Spectre Enough

Why it matters: a behavior patch accepted by EVAS may not improve Spectre.

Mitigation:

- For B1, every accepted candidate gets targeted Spectre audit.
- Report EVAS/Spectre mismatch explicitly.
- Keep EVAS as fast screening, not final metric.

Residual risk after mitigation: medium-low.

### Risk 3: Behavior Patches May Break Compile

Why it matters: behavior repair could undo compile closure.

Mitigation:

- Enforce compile-preserving gate before behavior scoring.
- Reject any candidate that regresses DUT/TB compile.
- Keep compile and behavior rewards separate.

Residual risk after mitigation: low.

### Risk 4: R0 Trace Memory May Become Noisy

Why it matters: bad traces can mislead future RAG/controller behavior.

Mitigation:

- Store accepted/rejected and EVAS/Spectre deltas.
- Prefer Spectre-confirmed traces over EVAS-only traces.
- Add confidence labels to trace cards.

Residual risk after mitigation: medium.

### Risk 5: Main120 May Still Be Too Dev-Like

Why it matters: methods tuned on Main120 may not generalize.

Mitigation:

- Treat Main120 as dev/main, not final proof.
- Build heldout and freeze it before tuning B1/R1 further.
- Final claims require heldout Spectre audit.

Residual risk after mitigation: medium.

## Confidence After Risk Loop

I do not have literal 100% certainty, and it would be misleading to claim that. But after the loop above, I have high practical confidence in the strategy:

1. Stop treating generic compile-looping as the main source of future gains.
2. Preserve S2 as the cheap compile-first pass.
3. Use T1 only as residual fallback.
4. Use R0 as repair memory infrastructure.
5. Move the active research front to B1 behavior repair.
6. Require heldout/Spectre validation before making final paper claims.

This is the cleanest direction supported by the current evidence.

## New Window Starter Prompt

Use this if opening a new Codex window:

```text
We are working in /Users/bucketsran/Documents/TsingProject/vaEvas.
The current vaEVAS mainline has finished Main120 compile strategy experiments A/D/C/S1/S2, T1 residual compile fallback, T2 residual retry, R0 repair trace indexing, CTX1 compact diagnostics, and B1 behavior task selection.

Key conclusion: compile repair is near diminishing returns. S2 is the cheap deterministic compile-first pass. T1 is useful only as residual fallback. T2 generic retry did not help. Naive CTX1 raw-note deletion did not reduce tokens. R0 trace memory exists. The next active direction is B1 behavior-repair controller using compile-preserving EVAS gate and targeted Spectre audit.

Read first:
- behavioral-veriloga-eval/analysis/vaevas_behavior_repair_handoff_20260509.md
- behavioral-veriloga-eval/analysis/B1_behavior_residual_analysis_20260509.md
- behavioral-veriloga-eval/tasklists/B1_behavior_repair_smoke_20260509.txt
- behavioral-veriloga-eval/analysis/main120_repair_trace_index_20260509.json

Start by designing/running B1 behavior-repair smoke on the selected 10 compile-OK behavior failures.
```
