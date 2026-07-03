# Source Offset RDAC Search Flow Audit

- Scenario: combined RDAC code search followed by comparator offset bisection and reference stepping.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `l2_core_ready`.
- Rationale: this is a composed calibration/search flow that combines RDAC refinement, bounded offset search, and reference stepping.
- Counting recommendation: retain as calibration L2/core flow, separate from single encoder or DFF support rows.
