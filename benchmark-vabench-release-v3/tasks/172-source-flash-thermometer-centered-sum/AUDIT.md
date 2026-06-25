# Source Flash Thermometer Centered Sum Audit

- Source: `zhaoty/TB_flash.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: flash ADC thermometer-code post-processing.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch10-evas/172-source-flash-thermometer-centered-sum`
  - `WORK/source-import-batch10-spectre/172-source-flash-thermometer-centered-sum`
