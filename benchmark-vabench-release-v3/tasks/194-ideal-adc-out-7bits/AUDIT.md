# Source Ideal ADC Out 7bits Audit

- Source: `guoxy/ideal_ADC_OUT_7BITS.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: weighted seven-bit ADC output compression into a scalar voltage.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch14-evas/194-ideal-adc-out-7bits`
  - `WORK/source-import-batch14-spectre/194-ideal-adc-out-7bits`
