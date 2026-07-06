# Source Single Shot Timer Pulse Audit

- Source: `wangx/single_shot.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a single-shot pulse generator. A rising VIN crossing asserts VOUT high after delay and a timer deasserts it after the configured pulse width.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
