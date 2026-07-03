# Source RS Latch Voltage Audit

- Scenario: set/reset state latch for voltage-domain digital control.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, and EVAS/Spectre parity pass.
- Evaluation: stable truth-table/state samples from `tran.csv`; raw simulator timestep equality is not used.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `l2_support_component`.
- Rationale: latch state is useful for AMS control sequencing, but this row is a generic latch primitive as written.
- Counting recommendation: support/control primitive only unless an explicit policy counts digital state primitives.
