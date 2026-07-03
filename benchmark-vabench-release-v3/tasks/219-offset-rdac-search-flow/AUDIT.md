# Source Offset RDAC Search Flow Audit

- Scenario: combined RDAC code search followed by comparator offset bisection and reference stepping.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `l2_core_ready`.
- Rationale: this is a composed calibration/search flow that combines RDAC refinement, bounded offset search, and reference stepping.
- Counting recommendation: retain as calibration L2/core flow, separate from single encoder or DFF support rows.

## Window B Calibration Closeout

- Gate 2 status: `cadence_modeling_ready`.
- Evidence: Window B targeted review on 2026-07-03 recorded EVAS hidden gold PASS, 5/5 concrete negatives rejected, AHDL-like lint PASS with 0 diagnostics, and targeted Spectre hidden gold PASS.
- Gold cleanup: differential stimulus/reference and RDAC bit outputs were smoothed with `transition(...)`, and RDAC array state was rewritten to scalar state so EVAS2 and Spectre exercise the same supported Verilog-A behavior.
- Counting recommendation: retain as a calibration L2/core flow. `TASKS.json` level is updated from L1 to L2 to match this boundary.
