# Source Pipe15 Data Align Audit

- Source: `liudongyang/PIPE8B_DATA_ALIGN.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: pipeline ADC lane alignment with different latency groups across a 15-bit word.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch18-evas/215-pipe15-data-align`
  - `WORK/source-import-batch18-spectre/215-pipe15-data-align`
