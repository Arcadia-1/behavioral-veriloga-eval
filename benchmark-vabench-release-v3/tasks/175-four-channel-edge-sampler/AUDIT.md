# Two-Gate SOP Audit: Task 175 Four Channel Edge Sampler

## Scope

Task 175 is a simultaneous four-channel analog sampler with a configurable clock-edge direction and transition output shaping.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as a multi-channel sampled analog memory L1 row.
- Function boundary: sample four analog inputs on the same clock event and preserve channel order at the outputs.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now exposes channel order, `direction`, `vdd/2` threshold, initialization, and `transition` timing.
- Checker alignment: checker now derives expected outputs from the four input waveforms at detected sampler edges.
- Hidden coverage: private deck now differs from visible stimulus and exercises a different per-channel sample sequence.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden repaired-batch checks passed; task-specific AHDL warnings were triaged.
