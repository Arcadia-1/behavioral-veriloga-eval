# Source Linearity RDAC Offset Sweep Audit

- Scenario: comparator offset stimulus generator that alternates bisection search and RDAC code stepping.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `l2_measurement_ready`.
- Rationale: this row sweeps RDAC code while rerunning comparator-directed offset bisection, so the measured behavior is a calibration/linearity characterization flow rather than a scalar helper.
- Counting recommendation: retain as calibration measurement L2.

## Window B Calibration Closeout

- Gate 2 status: `cadence_modeling_ready`.
- Evidence: Window B targeted review on 2026-07-03 recorded EVAS hidden gold PASS, 5/5 concrete negatives rejected, AHDL-like lint PASS with 0 diagnostics, and targeted Spectre hidden gold PASS.
- Gold cleanup: differential stimulus/reference outputs were smoothed with `transition(...)`.
- Counting recommendation: retain as a calibration measurement L2. `TASKS.json` level is updated from L1 to L2 to match this boundary.
