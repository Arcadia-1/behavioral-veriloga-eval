# Audit: Parameter Range Real Control

- Task id: `v3_414_parameter_range_real_control`
- Category: `veriloga_preprocessor_control_semantics`
- Gate 1 label: L0/support language-semantics row, not an independent AMS
  circuit-function benchmark and not part of the original full-300 claim.
- Gate 2 status: `cadence_boundary_only`; the public prompt, gold, checker,
  negatives, EVAS2, and Spectre behavior are aligned for this support boundary.

## Public Contract

The row checks ranged real and integer parameters in a clocked voltage-domain
model. The observable behavior is sampled-input gain scaling on `out` and the
updated modulo counter value on `metric`.

## Validation

- Default EVAS2/Rust: gold passed and all five concrete negatives were rejected.
- Python EVAS fallback: gold passed and all five concrete negatives were
  rejected.
- Targeted Spectre validation: passed.
- AHDL-like lint/preflight: passed with zero diagnostics.
- Spectre warning triage: only the shared `VACOMP-2435` environment warning was
  observed; no task-specific AHDL warning or compile error was found.
