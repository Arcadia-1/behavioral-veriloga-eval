# Audit: Macro Ifdef Gain Select

- Task id: `v3_410_macro_ifdef_gain_select`
- Category: `veriloga_preprocessor_control_semantics`
- Gate 1 label: L0/support language-semantics row, not an independent AMS
  circuit-function benchmark and not part of the original full-300 claim.
- Gate 2 status: `cadence_boundary_only`; the public prompt, gold, checker,
  negatives, EVAS2, and Spectre behavior are aligned for this support boundary.

## Public Contract

The row checks an object-like preprocessor define and `ifdef`/`else` selection
inside a clocked voltage-domain model. With `V3_HIGH_GAIN` defined, sampled
`vin` is scaled by the high-gain branch and `metric` reports the selected gain.

## Validation

- Default EVAS2/Rust: gold passed and all five concrete negatives were rejected.
- Python EVAS fallback: gold passed and all five concrete negatives were
  rejected.
- Targeted Spectre validation: passed.
- AHDL-like lint/preflight: passed with zero diagnostics.
- Spectre warning triage: only the shared `VACOMP-2435` environment warning was
  observed; no task-specific AHDL warning or compile error was found.
