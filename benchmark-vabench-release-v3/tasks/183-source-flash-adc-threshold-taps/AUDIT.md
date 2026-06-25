# Source Flash ADC Threshold Taps Audit

- Source: `zhangsh/ADC_31LEVEL.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: selected-threshold flash ADC thermometer sampling.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch12-evas/183-source-flash-adc-threshold-taps`
  - `WORK/source-import-batch12-spectre/183-source-flash-adc-threshold-taps`
