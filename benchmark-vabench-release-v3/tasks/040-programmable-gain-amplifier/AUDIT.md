# Honest SOP Audit: Task 040 Programmable Gain Amplifier

## Scope

Task boundary is one Verilog-A DUT, `programmable_gain_amplifier.va`, plus
EVAS/Spectre-compatible `.scs` testbenches. Public solver materials are
`instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are
`solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`.

## Gate 1

- Admission label: independent L1 DUT.
- Function: clocked programmable-gain amplifier with sampled gain selection,
  common-mode preservation, rail clipping, reset behavior, and clip metric
  output.
- Duplicate risk: low within the reviewed RF/baseband batch.

## Gate 2

- Modeling status: `cadence_modeling_ready` for the audited hidden gold slice.
- Prompt contract: public interface, parameters, sampled gain-selection
  behavior, clipping/reset behavior, metric semantics, and voltage-only
  constraints are stated without hidden-checker or gold-history wording.
- Cadence semantics: the model uses event-driven sampled gain state and
  transition-smoothed voltage outputs.

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
