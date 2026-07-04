# Two-Gate SOP Audit: Task 170 Clocked Four Input Mux

## Scope

Task 170 is a falling-edge sampled 4:1 analog mux. It is distinct from task 130 because selection is latched on a clock edge, and distinct from rewritten task 216 because it is the plain clocked mux baseline without reset/update qualification.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as sampled-data routing/control L1.
- Function boundary: two thresholded select bits choose one of four analog inputs on falling clock edges.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now exposes the clock edge, select-bit order, transition timing, and initialization.
- Checker alignment: checker now derives expected selected input from the select and data waveforms at clock edges.
- Hidden coverage: private deck now differs from visible stimulus and covers all four select codes with different data levels.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden repaired-batch checks passed; task-specific AHDL warnings were triaged.
