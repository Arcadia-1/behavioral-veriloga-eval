# Two-Gate SOP Audit: Task 132 Max Detector Hold

## Scope

Task 132 is a continuous maximum detector with held output. It matches Cadence-style max-detector/sample-hold modeling practice and is distinct from resettable peak-detector rows because it has no reset or timer behavior.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as an analog memory/primitive L1 row.
- Function boundary: initialize from the input, update only on new maxima, and hold through input decreases.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now exposes the monotone held-maximum invariant without source-provenance text.
- Checker alignment: checker now derives the running maximum from the input waveform and verifies monotone hold behavior.
- Hidden coverage: private deck now uses a different peak sequence with explicit post-peak input drops.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden repaired-batch checks passed; task-specific AHDL warnings were triaged.
