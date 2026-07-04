# Two-Gate SOP Audit: Task 155 Three Way Threshold Mux

## Scope

Task 155 is a three-input analog mux controlled by a differential threshold window. It is distinct from task 130 because it has three output regions and a differential control input.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as a three-region AMS selector L1 row.
- Function boundary: low, middle, and high selection regions over `V(cntrlp, cntrlm)`.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now exposes the differential control signal, inclusive middle region, and threshold parameters.
- Checker alignment: checker now derives expected selection from the control waveform and verifies all three regions.
- Hidden coverage: private deck now differs from the visible smoke deck and exercises the three regions in a different order.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden repaired-batch checks passed; task-specific AHDL warnings were triaged.
