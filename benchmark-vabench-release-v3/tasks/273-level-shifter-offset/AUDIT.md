# Two-Gate SOP Audit: Task 273 Level Shifter Offset

## Scope

Task 273 is a continuous analog level shifter with a public offset parameter.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as a small analog primitive L1 row.
- Function boundary: output equals input plus a configurable DC offset.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now exposes the `sigshift` parameter and offset behavior in the mandatory v3 format.
- Checker alignment: checker now derives expected output from the saved input waveform rather than a fixed sample table.
- Hidden coverage: private deck now differs from visible stimulus and exercises negative and positive input levels.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden repaired-batch checks passed; task-specific AHDL warnings were triaged.
