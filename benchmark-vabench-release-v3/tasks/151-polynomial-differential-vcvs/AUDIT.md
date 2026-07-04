# Two-Gate SOP Audit: Task 151 Polynomial Differential VCVS

## Scope

Task 151 is a parameterized polynomial differential voltage-controlled source with symmetric output common mode and saturation.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as a nonlinear differential source/amplifier L1 row.
- Function boundary: polynomial differential transfer, half-output scaling, output common-mode preservation, and symmetric saturation.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now exposes all polynomial coefficients, common-mode, saturation, and output symmetry requirements.
- Checker alignment: checker now derives expected outputs from the input waveform and public coefficient settings instead of fixed sample values.
- Hidden coverage: private deck now differs from visible stimulus and covers saturation with a different input/common-mode combination.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden PASS after checker coverage was aligned with visible and hidden stimulus coverage.
