# Honest SOP Audit: Task 039 Precision Rectifier Envelope Detector

## Scope

Task boundary is one Verilog-A DUT, `precision_rectifier_envelope_detector.va`,
plus EVAS/Spectre-compatible `.scs` testbenches. Public solver materials are
`instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are
`solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`.

## Gate 1

- Admission label: independent L1 DUT.
- Function: precision rectifier/envelope-detector macro with full-wave
  rectification around common mode, peak hold/decay memory, reset behavior, and
  a memory metric output.
- Duplicate risk: low within the reviewed RF/baseband batch.

## Gate 2

- Modeling status: `cadence_modeling_ready` for the audited hidden gold slice.
- Prompt contract: public interface, parameters, rectifier behavior,
  envelope-hold behavior, reset behavior, metric semantics, and voltage-only
  constraints are stated without hidden-checker or gold-history wording.
- Cadence semantics: the rectified output is a continuous direct voltage
  contribution; the envelope and metric are event-updated state outputs smoothed
  with `transition()`. The gold and negatives were adjusted to avoid applying
  `transition()` directly to a continuously varying input expression.

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
