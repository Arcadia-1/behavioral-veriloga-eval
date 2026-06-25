# Source QTZ Differential 2level Audit

- Source: `zhangsh/QTZ.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked two-threshold differential quantizer with signed analog output code.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch22-evas/237-source-qtz-differential-2level`
  - `WORK/source-import-batch22-spectre/237-source-qtz-differential-2level`
