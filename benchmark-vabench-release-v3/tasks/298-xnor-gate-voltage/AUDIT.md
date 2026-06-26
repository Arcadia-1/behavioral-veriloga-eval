# Source XNOR Gate Voltage Audit

- Source: `wangx/xnor_gate.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a two-input XNOR gate with voltage-coded logic. OUT is high when the two logical inputs match.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/298-xnor-gate-voltage`
  - `WORK/source-import-batch32-spectre/298-xnor-gate-voltage`
