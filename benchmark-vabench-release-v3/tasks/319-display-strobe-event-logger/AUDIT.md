# Honest SOP Audit: Display Strobe Event Logger

## Scope

This task is part of the Verilog-A language-semantics extension set. It is a pure voltage-domain behavioral DUT task.

## Four Standards

- Useful scenario: exercises `Use final_step and file/display system tasks for a deterministic metric.` from the Cadence Verilog-A Language Reference in a behavioral modeling context.
- Reasonable task: the public prompt fixes the port contract and voltage-coded behavior family.
- Complete tests: visible/hidden harness placeholders and five concrete negative variants are materialized for evaluator integration.
- Fair evaluation: negatives are intended to compile while changing only small behavioral details that should pass shallow smoke but fail full behavior checks.

Certification status: syntax-extension-candidate. These tasks extend language coverage beyond the original full-300 claim and must be certified separately before being included in paper-facing full-suite pass counts.
