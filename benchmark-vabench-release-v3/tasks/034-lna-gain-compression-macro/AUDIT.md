# Honest SOP Audit: Task 034 LNA Gain Compression Macro

## Scope

Task boundary is one Verilog-A DUT, `lna_gain_compression_macro.va`, plus
EVAS/Spectre-compatible `.scs` testbenches. Public solver materials are
`instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are
`solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`.

## Gate 1

- Admission label: `independent_l1_ready`.
- Function: low-noise-amplifier-style front-end macro with small-signal gain,
  large-signal gain compression, output bounding, and compression metric output.
- Counting decision: keep as the primary counted RF gain-compression L1 row.
  Task 037 remains a valid RF-role variant, but as currently written it is
  structurally close enough that both should not be counted without an explicit
  category policy or a PA-specific rewrite.

## Gate 2

- Modeling status: `cadence_modeling_ready` for the audited hidden gold slice.
- Prompt contract: public interface, parameters, small-signal gain, compression
  behavior, metric semantics, and voltage-only constraints are stated in the
  standard public contract format without hidden-checker or gold-history
  wording.
- Cadence semantics: the model uses voltage-domain behavioral contributions and
  transition-smoothed state/output updates.

## Verification

- EVAS hidden gold: PASS.
- Concrete negative recertification: 5/5 expected failures; all failed
  behavioral correctness with simulator return code 0.
- Visible smoke: PASS.
- Targeted Spectre hidden gold: PASS.
- AHDL lint/read-in triage: starter and solution preflight produced 0
  diagnostics; Spectre read-in showed no task-specific `AHDLLINT-*`,
  `VACOMP-1116`, or AHDL compile errors. The remaining Spectre warnings are
  global AHDL-CMI/environment or small-design setup notices.
