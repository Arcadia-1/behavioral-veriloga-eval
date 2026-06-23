# vaBench Benchmark Validity Audit Plan

Date: 2026-06-22

This document records the current benchmark-quality gaps after pausing the
SFT/GRPO training line. It does not change release claims. It is a work plan for
strengthening vaBench itself before additional model-training experiments.

## Current Strengths

The release package already has strong engineering evidence:

- 79 materialized L1/L2 entries and 271 release forms.
- Static certification passes for all 271 forms.
- EVAS/Spectre dual certification passes for all 271 forms.
- EVAS PASS / Spectre FAIL count is 0.
- A score denominator is enabled for 66 core entries and 236 core forms.

These facts support a credible benchmark package, but they do not by themselves
prove that every task is semantically useful, every checker is strong, or every
reported aggregate is fair.

## Validity Risks

| Benchmark property | Current risk | Why it matters | Primary evidence |
| --- | --- | --- | --- |
| Useful scenarios | Scope can be overclaimed beyond voltage-domain/event-driven behavioral Verilog-A. | Reviewers may expect current-domain, KCL/KVL, AC/DC/noise, transistor-level, RF S-parameter, or silicon-implementation coverage that the benchmark does not test. | `AGENTS.md`, `docs/VABENCH_L2_CLAIM_MAPPING_AUDIT.md` |
| Useful scenarios | Support/instrumentation tasks remain in the package but are excluded from the core denominator. | The package is useful, but core circuit coverage must not be inflated by measurement/stimulus infrastructure. | `benchmark-vabench-release-v1/reports/content_contract_audit.md` |
| Reasonable tasks | Some L2 rows require constrained wording because they are compact behavioral macros, not full systems. | A compact SAR transfer loop, I/Q schedule macro, or AGC leveling macro is valid only if the paper wording stays narrow. | `docs/VABENCH_L2_CLAIM_MAPPING_AUDIT.md`, `benchmark-vabench-release-v1/reports/overabstracted_benchmark_audit_20260531.md` |
| Reasonable tasks | Difficulty labels are not empirically calibrated. | D1/D2/D3 should not be used as calibrated difficulty tiers while baseline results show anomalies such as D3 not always harder than D2. | `benchmark-vabench-release-v1/reports/vabench_model_baseline_quality_audit_20260529.md` |
| Complete tests | EVAS/Spectre agreement does not prove checker sufficiency. | A weak checker can pass in both simulators. Parity validates evaluator agreement, not semantic discriminative power. | `benchmark-vabench-release-v1/reports/content_contract_audit.md` |
| Complete tests | Negative/mutation checker evidence is not yet systematic. | We still need evidence that shallow, hardcoded, final-value-only, or protocol-gaming implementations fail. | `benchmark-vabench-release-v1/reports/checker_evidence_workplan.md` |
| Complete tests | The 29 v1.1 rows in the 300-row surface are provisional because their current prompt/gold/checker surface is generic, not task-specific. | Counting them as final benchmark rows would inflate coverage and checker strength claims. | `docs/VABENCH_300_PROVISIONAL_AUDIT_20260622.md`, `benchmark-vabench-release-v1/vabench-300-expansion/VABENCH_300_MANIFEST.json` |
| Fair evaluation | Entry-level and form-level denominators are correlated. | The headline metric should avoid treating `tb`, `dut`, `e2e`, and `bugfix` forms as fully independent tasks. | `benchmark-vabench-release-v1/reports/score_denominator_manifest.json` |
| Fair evaluation | Aggregate pass rates mix very different forms and failure modes. | `e2e` is much harder than `bugfix`; syntax/protocol failures should be separated from circuit-behavior failures. | `benchmark-vabench-release-v1/reports/baseline_artifact.json`, `benchmark-vabench-release-v1/reports/vabench_model_baseline_quality_audit_20260529.md` |

## Audit Workstreams

### W1: Core-Task Usefulness Audit

Goal: prove that the 66 scored core entries are useful analog/mixed-signal
behavioral modeling tasks, not support utilities or overabstracted artifacts.

Checklist for each scored entry:

1. Identify the real circuit-function scenario.
2. State why a behavioral Verilog-A model is a natural artifact for that scenario.
3. Confirm the public prompt asks for that function, not a hidden checker trick.
4. Confirm the task stays inside the supported voltage-domain/event-driven scope.
5. Mark the row as `core_keep`, `core_keep_constrained`, `support_only`, or
   `revise_before_core_claim`.

Stop condition:

- Every scored entry has a one-line scenario justification and a claim boundary.
- Any support-like row is excluded from the core score denominator or explicitly
  redesigned.

### W2: L2 Claim Strength Audit

Goal: make the L2 claim reviewer-proof.

Checklist for each L2 entry:

1. Identify the claimed composition, loop, chain, or measurement-flow relation.
2. Identify public observables for intermediate state or coupled behavior.
3. Identify checker assertions that couple intermediate observables to output.
4. Confirm the checker cannot be passed by a direct final-value lookup.
5. Write permitted paper wording and forbidden overclaim wording.

Stop condition:

- Each L2 row has an explicit public-observable-to-checker-relation mapping.
- Rows with only compact behavior keep constrained wording.
- Support L2 rows remain outside the core circuit-function score.

### W3: Checker Negative/Mutation Audit

Goal: prove that checkers reject plausible wrong implementations.

Minimum negative classes:

| Negative class | Example wrong behavior |
| --- | --- |
| Constant output | Always drives a fixed value or fixed code. |
| Final-value-only | Produces the expected final metric without the intermediate behavior. |
| Polarity/sign inversion | Comparator, control, or feedback direction is reversed. |
| Timing-insensitive | Ignores clock, reset, sample, aperture, or event ordering. |
| Saturation-only | Rails output and accidentally matches loose bounds. |
| Hardcoded stimulus | Keys behavior to testbench timing instead of public inputs. |
| Missing intermediate coupling | Output changes, but exposed intermediate monitor is unrelated. |

Stop condition:

- Each L2 row has at least three meaningful negative variants that fail.
- High-risk L1 rows have at least one negative variant for their dominant
  failure mode.
- Negative fixtures are small and named as checker-regression tests, not scored
  benchmark rows.

### W4: Difficulty Calibration Audit

Goal: keep D1/D2/D3 useful without overclaiming them.

Actions:

1. Treat current D1/D2/D3 as design-intent labels.
2. Recompute empirical difficulty from multiple baselines using the frozen score
   denominator.
3. Flag rows where D1 is consistently hard or D3 is consistently easy.
4. Decide whether to relabel, keep as design-intent, or report difficulty only
   as a diagnostic axis.

Stop condition:

- Paper wording does not claim calibrated difficulty unless monotonicity and
  row-level anomalies have been resolved.

### W5: Evaluation Fairness Audit

Goal: make reported scores defensible.

Recommended reporting policy:

1. Use entry-level pass rate as the headline benchmark score.
2. Use form-level pass rate as diagnostic detail.
3. Report `tb`, `dut`, `e2e`, and `bugfix` separately.
4. Use `full_strict` as the fixed-budget model metric.
5. Report `valid_candidate` and `behavior_ready` only as diagnostic slices.
6. Separate syntax/protocol failures from circuit-behavior failures.
7. Keep support rows and L0 conformance rows out of core benchmark scores.

Stop condition:

- A reader can reproduce exactly which rows are counted, which are diagnostic,
  and which failure modes are attributed to protocol versus behavior.

## Priority Order

1. Freeze the claim boundary table for scope, support rows, L2 constrained rows,
   and score denominator wording.
2. Build a mutation/negative checklist for the 17 L2 rows.
3. Implement or materialize the smallest negative fixtures for the riskiest L2
   rows first: AGC, I/Q downconversion, SAR loop, ADPLL, CPPLL, calibration,
   LDO, and measurement-flow rows.
4. Re-run static, EVAS, and Spectre only for rows whose gold/checker/testbench
   behavior changes.
5. Regenerate paper-facing tables only after claim boundaries and checker
   negative evidence are stable.

## Non-Goals

- Do not expand the paper-scored benchmark count before validity gaps are closed.
- Do not count provisional v1.1 rows from the 300-row management surface until
  task-specific prompt/gold/checker/negative evidence is complete.
- Do not restart SFT/GRPO training from this workstream.
- Do not claim broader analog-design coverage than the voltage-domain,
  event-driven behavioral subset.
- Do not use EVAS-only success as final benchmark certification; Spectre remains
  the final paper-facing judge.
