# Source DAC7 Code Generator Audit

- Source: `zhangm/DAC7B_TB_VA.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked seven-bit inverted counter code generator for DAC test stimulus.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch18-evas/217-dac7-code-generator`
  - `WORK/source-import-batch18-spectre/217-dac7-code-generator`
