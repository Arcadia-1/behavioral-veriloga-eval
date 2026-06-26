# Source L2 7b DAC Ready Audit

- Source: `yueyh/L2_7B_DAC.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: ready-clocked 7-bit weighted DAC monitor with first-sample discard.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch23-evas/238-l2-7b-dac-ready`
  - `WORK/source-import-batch23-spectre/238-l2-7b-dac-ready`
