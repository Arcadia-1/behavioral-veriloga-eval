# Source Single ADC 7b Weighted Audit

- Source: `lixingyu/TEST_D2A_SINGLE_ADC_7B.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: continuous 7-bit weighted backend code-to-voltage monitor.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch22-evas/236-single-adc-7b-weighted`
  - `WORK/source-import-batch22-spectre/236-single-adc-7b-weighted`
