# Two-Gate SOP Audit: Task 130 Analog Mux Threshold

## Scope

Task 130 is a threshold-controlled 2:1 analog mux. It is backed by common Verilog-A mux modeling patterns in the Cadence material and is distinct from clocked/sample-held mux rows because its selection follows the analog control threshold directly.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as a small AMS selector L1 row.
- Function boundary: direct analog input selection controlled by a public threshold on `vsel`.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now uses the mandatory v3 heading shape and exposes only interface, threshold parameter, and observable mux behavior.
- Checker alignment: checker derives the expected output from `vin1`, `vin2`, and `vsel` instead of using a fixed waveform table.
- Hidden coverage: private deck now differs from the visible smoke deck and exercises both initial-high and low-to-high select behavior.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden repaired-batch checks passed; task-specific AHDL warnings were triaged.
