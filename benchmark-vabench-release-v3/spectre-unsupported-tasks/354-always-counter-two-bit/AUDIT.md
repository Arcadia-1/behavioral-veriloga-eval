# Honest SOP Audit: Always Counter Two Bit

## Scope

This task belongs to the AMS mixed-signal extension set. It is not part of the original full-300 Verilog-A-only claim.

## Four Standards

- Useful scenario: exercises `Use always block with small digital counter state.`
- Reasonable task: the prompt fixes the target artifact and keeps the task behavioral.
- Complete tests: visible/hidden harness placeholders and five concrete negative variants are materialized for evaluator integration.
- Fair evaluation: negatives are intended to compile under an AMS-capable simulator while changing small behavior details that should fail full checks.

Certification status: ams-mixed-signal-candidate. EVAS support is currently incomplete for some digital AMS constructs, especially `always` blocks and ANSI typed digital ports.
