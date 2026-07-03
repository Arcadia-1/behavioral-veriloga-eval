# Source DFF Set Reset Hold Audit

- Scenario: D flip-flop with asynchronous active-low set/reset priority and held clocked data.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `l2_support_component`.
- Rationale: richer than a bare DFF, but still a generic voltage-coded state primitive rather than an AMS subsystem behavior.
- Counting recommendation: support/control primitive only unless policy counts state primitive variants.
