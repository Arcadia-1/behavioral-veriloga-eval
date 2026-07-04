# Two-Gate SOP Audit: Task 133 Time Diff Detector

## Scope

Task 133 is a clocked timing measurement utility that converts the previous cycle's input edge-time difference into a bounded voltage.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as an AMS measurement/utility L1 row.
- Function boundary: detect first rising input edges inside each clock window, scale their time difference, clip to rails, and rearm on the next clock event.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now exposes thresholds, scale, clipping, transition timing, and rearm behavior.
- Checker alignment: checker now extracts clock/input edges from the waveform and computes expected output dynamically.
- Hidden coverage: private deck now covers positive and negative timing differences over multiple clock windows.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden repaired-batch checks passed; task-specific AHDL warnings were triaged.
