# Honest SOP Audit: Task 083 Crossing Metric Writer

## Scope

Task boundary is one Verilog-A DUT migrated from `vbr1_l1_crossing_metric_writer:dut`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: accepted. The module is a reusable behavioral Verilog-A block or flow component with a concrete transient use case.
- Reasonable task: accepted for this migration slice. The public prompt names the target artifact, interface, and behavior context.
- Complete tests: accepted for current v3 smoke. Hidden gold passes and `neg_001_zero` is non-full-credit; further hand-authored negatives can still strengthen release evidence.
- Fair evaluation: accepted for current v3 smoke. The checker is bound through the v3 alias and the hidden behavior is covered by the public prompt context.

## Checker And Evidence

- Source checker id: `vbm1_file_metric_writer_dut`
- EVAS 0.4.5 hidden gold smoke: PASS
- Concrete negative `neg_001_zero`: non-full-credit

## Remaining Risk

This is an initial migration artifact. Do not count this task in a release denominator until gold and negative evidence are attached.
