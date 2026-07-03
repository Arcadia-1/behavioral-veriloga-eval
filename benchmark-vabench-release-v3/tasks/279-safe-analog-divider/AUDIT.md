# Two-Gate SOP Audit: Task 279 Safe Analog Divider

## Scope

Task 279 implements the same guarded analog divider function as task 150, with a different module name and default denominator floor.

## Gate 1: Admission And Counting

- Admission label: `hard_duplicate_rewrite_or_remove`.
- Counting decision: do not count task 279 as a real independent benchmark while task 150 carries the canonical safe-divider coverage.
- Duplicate evidence: both tasks expose `signumer`, `sigdenom`, and `sigout`; both compute gain-scaled numerator divided by a sign-preserving guarded denominator. The different default guard value and module name are not enough to create a new circuit function.
- Rewrite path: to become independent, this row would need a materially different divider function such as saturation, rail-aware clipping, differential inputs, denominator-valid flagging, or a composed measurement flow.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_boundary_only` for independent benchmark coverage.
- Prompt hygiene: public instruction now describes the module contract without old provenance wording or private evidence paths.
- Checker alignment: checker verifies the guarded divider behavior, but this remains duplicate coverage relative to task 150.
- Hidden coverage: visible and private decks remain identical because this row is retained only as a non-counted duplicate/regression artifact.

## Evidence

- Human confirmation: task 279 should not count as an independent benchmark; task 150 is the canonical safe-divider row.
