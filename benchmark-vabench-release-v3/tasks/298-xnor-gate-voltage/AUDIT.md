# Source XNOR Gate Voltage Audit

- Gate 1 status: `l2_support_component` / support-regression candidate, not a strong core scored benchmark as written.
- Review note: this is a thresholded Boolean equality primitive with a rail-coded voltage output. It is meaningful as a helper inside AMS control, converter, sampler, or calibration flows, but the standalone prompt is mainly a truth-table task.
- Counting recommendation: keep as a support utility or L0-style regression row; do not count as an independent core circuit benchmark without a distinct AMS decision/control role.

- Scenario: Implement a two-input XNOR gate with voltage-coded logic. OUT is high when the two logical inputs match.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
