# Controller Next Experiment Plan - 2026-05-09

## Thesis

The vaEVAS controller should evolve from a compile-only repair pipeline into a staged tool controller:

1. cheap deterministic compile repair first,
2. LLM fallback only for residual/unknown compile failures,
3. repair-trace memory for retrieval and future training,
4. compact diagnostics to reduce token cost,
5. behavior-repair controller after compile closure is mostly solved.

## Claim Map

| Claim | Why it matters | Minimum convincing evidence | Experiments |
| --- | --- | --- | --- |
| C1: deterministic compile skills are the right first pass | Most compile errors are pattern-like; using LLM everywhere wastes tokens | S2 keeps or improves PASS vs S1 while using no new LLM calls for selected residuals | S2 full, S2 heldout |
| C2: LLM fallback is useful only after S2 stalls | Unknown compile failures need open-ended reasoning | T1 reduces residual compile fail on S2 failures with acceptable cost | T1, T2 |
| C3: repair traces should become memory, not more hard-coded skills | Avoid overfitting and make fixes transferable | Retrieved traces reduce token cost or improve T1 success on residual/heldout | R0, R1 |
| C4: context compression is necessary | Current T1 uses about 11k tokens/task | CTX1 preserves most compile-closure gain with lower input tokens | CTX1 |
| C5: behavior repair is now the main bottleneck | S2/T1 convert compile fails into behavior fails | B1 improves behavior metrics on compile-OK failures without increasing compile failures | B1 |

## Systems

| System | Short name | Role |
| --- | --- | --- |
| A | prompt-only | Base model capability |
| D | rules-only | Public rule prompt baseline |
| C | compile-loop | LLM feedback loop baseline |
| S1 | compile-skill-prompt | Compile knowledge injected in prompt |
| S2 | compile-skill-accept | Deterministic local skill + EVAS accept/reject |
| T1 | LLM residual fallback | Online plan-execute fallback after S2 |
| R0/R1 | repair-trace memory | Trace extraction and retrieval-augmented repair |
| CTX1 | compact diagnostics | Token-reduced T1 variant |
| B1 | behavior controller | Behavior-gap repair after compile closure |

## Experiment Blocks

### Block S2: Deterministic Compile Skill First Pass

- Claim tested: deterministic compile skills should run before any expensive LLM fallback.
- Dataset: Main120 already done; repeat on heldout after heldout construction.
- Inputs: S2 uses S1/C residual compile failures, local skill transformations, EVAS accept/reject.
- Compared systems: C, S1, S2.
- Metrics: Spectre PASS, compile OK, compile fail, DUT/TB compile attribution, behavior fail, EVAS/Spectre mismatch, local runtime.
- Success criterion: S2 has equal or better Spectre PASS than S1 and lower compile fail with no extra LLM calls.
- Current evidence: Main120 S2 Spectre = PASS 29/120, compile OK 110/120, compile fail 10/120.
- Failure interpretation: If heldout loses S1 gains, local skills are overfitted and need feature-based guards.
- Priority: MUST-RUN on heldout after heldout exists.

### Block T1/T2: LLM Fallback for Residual or Unknown Compile Failures

- Claim tested: online LLM repair should be routed only when deterministic tools stall.
- Dataset: T1 = 10 S2 Spectre compile residuals; T2 = remaining 3 T1 Spectre compile residuals.
- Inputs: compact public contract, normalized failure notes, candidate snippet, previous repair history.
- Compared systems: S2 residual, T1 residual fallback, T2 focused fallback.
- Metrics: residual PASS, residual compile OK, residual compile fail, token/time per repaired compile failure, accepted/rejected rounds.
- Success criterion: T1/T2 reduce compile fail without causing compile regressions; any PASS gain is a bonus.
- Current evidence: T1 Spectre slice = PASS 1/10, compile OK 7/10, compile fail 3/10.
- Failure interpretation: If T2 stalls on 3 residuals, remaining errors may need domain-specific behavior/code synthesis rather than compile repair.
- Priority: MUST-RUN T2 before broader controller claims.

### Block R0/R1: Repair Trace Memory

- Claim tested: successful and failed repair trajectories should be stored and retrieved instead of repeatedly rediscovered.
- Dataset: traces from C/S1/S2/T1 on Main120; later heldout transfer.
- R0 output: repair-trace index with failure family, task form, file scope, before/after status, edit summary, EVAS delta, Spectre delta, token/time.
- R1 experiment: use top-k retrieved traces as compact examples for T1-style repair.
- Compared systems: T1 without memory, T1+trace-retrieval.
- Metrics: compile closure, PASS, token cost, no-code/extraction failures, repair rounds, trace-hit usefulness.
- Success criterion: T1+memory matches or improves compile closure with lower tokens or fewer rounds.
- Failure interpretation: If retrieval hurts, traces are too noisy or need stricter success labels and family normalization.
- Priority: MUST-RUN R0, SHOULD-RUN R1 after CTX1.

### Block CTX1: Compact Diagnostics

- Claim tested: T1 prompt is overfed; compact context can keep the useful signal at lower cost.
- Dataset: same 10 T1 residual tasks for controlled comparison.
- Variant A: current T1 full-ish prompt.
- Variant B: compact diagnostics only: public contract, normalized failure family, minimal code slice, checker target, previous repair summary.
- Variant C: compact diagnostics + retrieved trace card after R0.
- Metrics: input tokens/task, output tokens/task, API seconds/task, compile OK, compile fail, PASS, invalid/no-code rate.
- Success criterion: at least 30-50% input token reduction while preserving most T1 compile-closure gain.
- Failure interpretation: If performance drops sharply, missing context must be identified by ablation: code slice, rules, contract, or prior notes.
- Priority: MUST-RUN before scaling T1 to heldout or larger benchmarks.

### Block B1: Behavior-Repair Controller

- Claim tested: after compile closure, behavior mismatch is the dominant bottleneck and needs separate tools.
- Dataset: 8-12 compile-OK behavior failures from S2/T1, stratified by family.
- Inputs: checker metrics, waveform-derived summaries, public contract, minimal code snippets.
- Tools: behavior-gap diagnoser, targeted EVAS subcheck, LLM behavior patch, EVAS accept/reject, targeted Spectre audit.
- Compared systems: S2/T1 candidate, B1 behavior repair candidate.
- Metrics: behavior PASS, checker-axis improvement, compile regression count, token/time, EVAS/Spectre agreement.
- Success criterion: behavior metrics improve without increasing compile failures; at least a small PASS gain on selected slice.
- Failure interpretation: If behavior repair causes compile regressions, require compile-preserving patch constraints and two-stage validation.
- Priority: MUST-RUN after T2/R0, because behavior fail is now larger than compile fail.

## Run Order

| Step | Run ID | Goal | Dataset | Gate | Cost |
| --- | --- | --- | --- | --- | --- |
| 1 | T2 | Close/analyze three remaining T1 compile residuals | 3 tasks | compile fail goes 3 -> <=2 or clear failure taxonomy | low |
| 2 | R0 | Build trace memory table from C/S1/S2/T1 | Main120 artifacts | trace rows cover accepted/rejected repairs with EVAS/Spectre deltas | low |
| 3 | CTX1 | Token compression ablation on T1 slice | 10 tasks | >=30% token reduction with similar compile closure | medium |
| 4 | B1-smoke | Behavior repair on small stratified slice | 8-12 tasks | no compile regressions; behavior metric improves | medium |
| 5 | S2/T1/CTX1 heldout | Transfer check | heldout48 or next heldout | gains transfer without task-id routing | high |
| 6 | B1-heldout | Behavior transfer check | heldout behavior residuals | behavior gains transfer | high |

## Metrics to Report Everywhere

Primary:

- Spectre PASS
- Spectre compile OK / compile fail
- Spectre behavior fail
- DUT compile fail / TB compile fail attribution

Secondary:

- EVAS PASS and compile closure
- EVAS/Spectre PASS mismatch
- token input/output/reasoning
- API elapsed time
- repair rounds
- accepted/rejected tool actions
- compile regressions introduced by behavior repair

## Immediate Task List

1. Create `R0` trace extractor over existing C/S1/S2/T1 artifacts.
2. Run `T2` on the three T1 residual compile failures.
3. Implement CTX1 compact prompt mode for T1 residual repair.
4. Select B1 behavior smoke tasks by failure family and checker metrics.
5. Run B1 with compile-preserving gate: candidate must keep EVAS compile OK before behavior improvement is considered.

## Design Risks and Mitigations

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| S2 overfits known benchmark failures | deterministic skills may look strong but not transfer | public-feature routing only; heldout transfer |
| T1 consumes too many tokens | 11k tokens/task is expensive for scaling | CTX1 compact diagnostics and ReWOO-style plan/execute separation |
| Repair memory becomes noisy | bad traces can poison future repairs | store accept/reject, Spectre delta, failure family, and confidence score |
| Behavior repair causes compile regression | behavior patches may break syntax | compile-preserving gate before behavior scoring |
| EVAS/Spectre mismatch misleads controller | EVAS is fast but not final | targeted Spectre audit for accepted controller milestones |
