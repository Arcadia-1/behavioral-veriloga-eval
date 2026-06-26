# Source VA DAC 6b SE Audit

- Source: `zhangym/_va_6b_dac.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: ready-triggered single-ended 6-bit weighted DAC using the source model's bipolar normalization.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled DAC output from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch24-evas/246-va-dac-6b-se`
  - `WORK/source-import-batch24-spectre/246-va-dac-6b-se`
