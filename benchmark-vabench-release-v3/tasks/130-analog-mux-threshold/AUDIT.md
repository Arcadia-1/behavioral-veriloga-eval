# Source Analog Mux Threshold Audit

- Scenario: threshold-controlled two-input analog multiplexer.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `independent_l1_ready`.
- Rationale: this is an analog signal selector controlled by voltage threshold, not merely a Boolean gate. It is distinct from clocked mux samplers because selection follows both rising and falling threshold crossings.
- Counting recommendation: retain as a small AMS selector L1 row.
