# Source VA Lx ADC Ideal 4b Audit

- Source: `zhangfm/VA_Lx_ADC_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked four-bit SAR-style ideal ADC conversion.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch14-evas/195-va-lx-adc-ideal-4b`
  - `WORK/source-import-batch14-spectre/195-va-lx-adc-ideal-4b`
