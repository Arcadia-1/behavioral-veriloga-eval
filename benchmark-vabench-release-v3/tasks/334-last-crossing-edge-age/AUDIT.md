# Honest SOP Audit: Last Crossing Edge Age

## Scope

This task is part of the Verilog-A language-semantics extension set. It is a pure voltage-domain behavioral DUT task.

## Four Standards

- Useful scenario: exercises `above()`, `last_crossing()`, and `timer()` for threshold/edge timing behavior in a behavioral modeling context.
- Reasonable task: the public prompt fixes the port contract and voltage-coded behavior family.
- Complete tests: visible/hidden harness placeholders and five concrete negative variants are materialized for evaluator integration.
- Fair evaluation: negatives are intended to compile while changing only small behavioral details that should pass shallow smoke but fail full behavior checks.

Issue #69 repair: the public prompt, gold solution, and concrete negatives now
use the Spectre-supported two-argument `last_crossing(expr, dir)` form instead
of the non-portable four-argument form. The prompt also avoids hidden timing
breakpoints and states the observable age/marker/reset contract.

Fresh validation: EVAS Python hidden gold passes and five concrete negatives
are rejected behaviorally; targeted Spectre hidden gold passes; targeted
Spectre hidden negatives are rejected behaviorally; EVAS AHDL-like lint has no
diagnostics; Spectre AHDL read-in has no task-specific warning beyond the
global `VACOMP-2435` environment-variable notice.

Certification status: language-extension-spectre-ready. This task extends
language coverage beyond the original full-300 claim and must be certified
separately before being included in paper-facing full-suite pass counts.
