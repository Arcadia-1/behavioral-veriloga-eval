# Source PFD Up Down State Audit

- Source: `huangsy/PFD.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a bounded phase-frequency detector state machine. REF rising increments state up to +1, FB rising decrements state down to -1, and U/D expose the sign of the state.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
