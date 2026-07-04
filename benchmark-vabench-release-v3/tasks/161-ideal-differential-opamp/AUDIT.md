# Two-Gate SOP Audit: Task 161 Ideal Differential Opamp

## Scope

Task 161 is a fixed-gain ideal differential output stage with a fixed output common mode. Cadence reference material includes differential amplifier/opamp behavioral patterns with symmetric output driving.

## Gate 1: Admission And Counting

- Admission label: `independent_l1_ready`.
- Counting decision: retain as a compact differential amplifier L1 row.
- Function boundary: fixed output common mode plus signed differential gain from `vinp-vinn` to `voutp-voutn`.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` after targeted EVAS, Spectre visible/hidden gold validation, and AHDL warning triage.
- Prompt hygiene: public instruction now states that the fixed common mode and gain are module contract values, not hidden testbench artifacts.
- Checker alignment: checker now computes expected outputs from the differential input and verifies common-mode preservation.
- Hidden coverage: private deck now differs from visible stimulus and covers both differential polarities.

## Evidence

- Fresh EVAS gold after checker/hidden repair: PASS.
- Fresh EVAS negatives after checker repair: all concrete negatives rejected behaviorally.
- Spectre gold validation: visible and hidden repaired-batch checks passed; task-specific AHDL warnings were triaged.
