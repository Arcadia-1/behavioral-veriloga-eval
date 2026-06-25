# Source Clocked DAC 4b Binary Audit

- Source: `wangxy/DAC_4b.va`
- Scenario: clocked 4-bit binary-weighted bipolar DAC reconstruction.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch3-evas/125-source-clocked-dac-4b-binary`
  - `WORK/source-import-batch3-spectre/125-source-clocked-dac-4b-binary`
