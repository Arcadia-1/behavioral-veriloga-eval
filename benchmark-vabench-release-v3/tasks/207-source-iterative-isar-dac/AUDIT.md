# Source Iterative ISAR DAC Audit

- Source: `dmanager/_tool_iSAR.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: iterative SAR DAC estimate update with halving search step.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch16-evas/207-source-iterative-isar-dac`
  - `WORK/source-import-batch16-spectre/207-source-iterative-isar-dac`
