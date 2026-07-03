# Two-Gate SOP Audit: Task 154 Analog Multiplier

## Scope

Task 154 is a two-input analog multiplier with a public gain parameter, matching common Verilog-A primitive multiplier examples.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as an analog arithmetic primitive L1 row.
- Function boundary: continuous multiplication of two input voltages with public gain scaling.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now exposes only the interface, gain parameter, and multiplier behavior.
- Checker alignment: checker now derives expected output from the two input waveforms and gain, including negative products.
- Hidden coverage: private deck now differs from visible stimulus and exercises sign changes in the product.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden repaired-batch checks passed; task-specific AHDL warnings were triaged.
