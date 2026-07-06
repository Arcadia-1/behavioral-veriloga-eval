# Source VA DAC 6b SE Audit

- Source: `zhangym/_va_6b_dac.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: ready-triggered single-ended 6-bit weighted DAC using the source model's bipolar normalization.
- Import status: certified only after visible compile, EVAS/Spectre semantic checks, parity pass, and negative variant rejection.
- Evaluation: stable sampled DAC output from `tran.csv`; raw simulator timestep equality is not used.
