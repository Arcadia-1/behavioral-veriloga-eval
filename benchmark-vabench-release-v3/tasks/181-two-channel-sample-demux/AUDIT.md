# Two-Gate SOP Audit: Task 181 Two Channel Sample Demux

## Scope

Task 181 is a two-source clocked analog sample router. It is distinct from task 170 because it uses separate source clocks instead of a latched binary select word.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as sampled-data routing/control L1.
- Function boundary: rising edges on two separate clocks select and hold samples from two analog inputs onto one output.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now exposes initialization, clock thresholds, both source clocks, and fixed output transition timing.
- Checker alignment: checker now derives expected output from source-specific clock events and sampled inputs.
- Hidden coverage: private deck now differs from visible stimulus and covers both source clocks with different input values.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden repaired-batch checks passed; task-specific AHDL warnings were triaged.
