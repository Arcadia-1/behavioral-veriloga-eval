# Source RS Phase Detector Audit

- Source: `huangsy/PD_RS.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement an RS-latch phase detector. REF rising sets UP high/DOWN low; FB rising resets UP low/DOWN high.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
