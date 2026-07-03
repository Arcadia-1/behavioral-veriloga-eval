# Honest SOP Audit: Task 037 PA Compression Macro

## Scope

Task boundary is one Verilog-A DUT, `pa_compression_macro.va`, plus
EVAS/Spectre-compatible `.scs` testbenches. Public solver materials are
`instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are
`solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`.

## Gate 1

- Admission label: RF gain-compression L1 candidate.
- Function: power-amplifier-style macro with above-unity gain, large-signal
  compression/limiting, bounded output, and compression metric output.
- Counting risk: medium. This row and task 034 both model gain-compression
  amplifier behavior in different RF roles. Keep both as role-distinct
  candidates for now, but final counted status should be confirmed against the
  category-level duplicate policy.

## Gate 2

- Modeling status: `cadence_modeling_ready` for the audited hidden gold slice.
- Prompt contract: public interface, parameters, gain/compression behavior,
  output limiting, metric semantics, and voltage-only constraints are stated
  without hidden-checker or gold-history wording.
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
