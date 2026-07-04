# Two-Gate SOP Audit: Task 150 Safe Voltage Divider

## Scope

Task 150 is the canonical safe analog divider row for this category. It implements numerator divided by a sign-preserving guarded denominator with a public gain parameter.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as the counted divider L1 row.
- Duplicate relationship: task 279 implements the same guarded-divider function with a different module name/default denominator floor and should remain non-counted unless rewritten.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now exposes the gain parameter, positive denominator range, and sign-preserving guard behavior.
- Checker alignment: checker now computes the expected divider output from the saved numerator and denominator waveforms, including positive and negative guarded regions.
- Hidden coverage: private deck now differs from the visible smoke deck and covers both guard polarities.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden repaired-batch checks passed; task-specific AHDL warnings were triaged.
