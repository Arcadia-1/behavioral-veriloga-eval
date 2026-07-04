# Audit: Last Crossing Period Meter

## Gate 1 Classification

- Classification: L0/support boundary.
- Circuit role: `last_crossing()` period measurement.
- Counting note: this row primarily exercises Cadence/Verilog-A operator or syntax semantics. As written, it should not be counted as a new independent core circuit-function benchmark without a separate rescue decision.

## Gate 2 Modeling Notes

- Useful scenario: exercises `last_crossing()` and `cross()` for threshold/edge timing behavior in a behavioral modeling context.
- Reasonable task: the public prompt fixes the port contract and voltage-coded behavior family.
- Complete tests: visible/hidden harness placeholders and five concrete negative variants are materialized for evaluator integration.
- Fair evaluation: negatives are intended to compile while changing only small behavioral details that should pass shallow smoke but fail full behavior checks.
- The public prompt is normalized to the v3 instruction headings.
- The DUT contract is voltage-domain behavioral Verilog-A and avoids transistor-level devices and current-domain branch contributions.
- Public parameter values, event thresholds, output scaling, reset behavior, and smoothing requirements are stated in the prompt where they are part of the observable contract.
- Testbench values are not presented as implementation constants to copy into the DUT.

Issue #69 repair: the public prompt, gold solution, and concrete negatives now
use the Spectre-supported two-argument `last_crossing(expr, dir)` form instead
of the non-portable four-argument form. The prompt also avoids hidden timing
breakpoints and states the observable period/reset contract.

Fresh validation: EVAS Python hidden gold passes and five concrete negatives
are rejected behaviorally; targeted Spectre hidden gold passes; targeted
Spectre hidden negatives are rejected behaviorally; EVAS AHDL-like lint has no
diagnostics; Spectre AHDL read-in has no task-specific warning beyond the
global `VACOMP-2435` environment-variable notice.

Certification status: language-extension-spectre-ready. This task extends
language coverage beyond the original full-300 claim and must be certified
separately before being included in paper-facing full-suite pass counts.

## Validation Notes

- EVAS2 reference run: PASS for this row in the 326-340 batch after the EVAS idtmod/random/last_crossing semantic fixes.
- EVAS2 negative run: the 326-340 batch produced 90/90 expectation matches, including rejection of this row's concrete negatives.
- Spectre reference run: PASS for this row in the targeted 326-340 private validation batch.
- Spectre negative run: this row's concrete negatives were rejected in the targeted 326-340 private validation batch.
- AHDL-like lint: PASS with zero diagnostics.
