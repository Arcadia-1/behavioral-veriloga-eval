# Audit: Macro Functionlike Clamp

- Task id: `v3_409_macro_functionlike_clamp`
- Category: `veriloga_preprocessor_control_semantics`
- Gate 1 label: L0/support language-semantics row, not an independent AMS
  circuit-function benchmark and not part of the original full-300 claim.
- Gate 2 status: `cadence_boundary_only`; the public prompt, gold, checker,
  negatives, EVAS2, and Spectre behavior are aligned for this support boundary.

## Public Contract

The row checks a function-like preprocessor macro used in a clocked
voltage-domain model. The observable behavior is a sampled clamp to the public
`0.0` to `0.9` interval, with `metric` reporting the normalized clamped value.

## Validation

- Default EVAS2/Rust: gold passed and all five concrete negatives were rejected.
- Python EVAS fallback: gold passed and all five concrete negatives were
  rejected.
- Targeted Spectre validation: passed.
- AHDL-like lint/preflight: passed with zero diagnostics.
- Spectre warning triage: only the shared `VACOMP-2435` environment warning was
  observed; no task-specific AHDL warning or compile error was found.
