# Source Linearity RDAC Offset Sweep Audit

- Scenario: comparator offset stimulus generator that alternates bisection search and RDAC code stepping.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `l2_measurement_ready`.
- Rationale: this row sweeps RDAC code while rerunning comparator-directed offset bisection, so the measured behavior is a calibration/linearity characterization flow rather than a scalar helper.
- Counting recommendation: retain as calibration measurement L2.
