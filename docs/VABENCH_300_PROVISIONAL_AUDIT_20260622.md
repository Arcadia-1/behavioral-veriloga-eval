# vaBench 300 Provisional Audit

Date: 2026-06-22

This audit records the claim-boundary decision for the vaBench 300 management
surface after inspecting the 29 v1.1 expansion rows.

## Decision

The 300-row surface remains useful as an asset-management and future-expansion
surface, but only the 271 inherited release-v1 rows are currently paper-score
ready. The 29 v1.1 rows are kept as provisional management assets and must not
enter paper score denominators.

## Evidence

- The release-v1 score source of truth remains the 79-entry / 271-form package
  with the 66-entry / 236-form core score denominator.
- The 29 v1.1 rows currently use generated public prompts rather than
  task-specific release-style contracts.
- The v1.1 gold Verilog-A assets are generated from the same generic
  voltage-domain event-driven state scaffold with ports `in`, `clk`, `rst`,
  `out`, and `metric`.
- The current `runners/simulate_evas.py` behavior-checker registry covers the
  271 inherited v1 rows, but not the 29 v1.1 normalized task IDs.
- The 1500 negative candidates are static-shallow-shape audited; none are yet
  verified as full-checker failures.

## Required Before v1.1 Score Admission

Each provisional v1.1 row needs all of the following before it can become a
paper-scored benchmark task:

1. A task-specific public prompt with interface, artifact, stimulus, observable,
   and forbidden-overclaim boundaries.
2. A task-specific gold Verilog-A implementation and Spectre testbench whose
   behavior matches the claimed circuit function.
3. A registered behavior checker in `runners/simulate_evas.py`.
4. At least three meaningful negative or mutation fixtures that fail the full
   checker; high-risk L2 rows should retain five near-miss negatives.
5. Fresh EVAS/Spectre evidence with zero EVAS PASS / Spectre FAIL mismatches.

## Current Safe Wording

- The public release benchmark score is based on the release-v1 score
  denominator, not the provisional 300-row surface.
- The vaBench 300 directory is an expansion-management surface with 271
  inherited release-v1 rows plus 29 provisional v1.1 rows.
- Negative candidates are useful for future checker hardening but are not yet
  publication evidence for checker discriminative power.
