# Source LT Read SAR6B Weighted Audit

- Source: `gaoya/LT_READ_SAR6B.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a continuous 6-bit SAR readout with source weights. D5..D1 contribute 1, 1/2, 1/4, 1/8, and 1/16 of vref; D0 is present but ignored, matching the source model.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch27-evas/258-source-lt-read-sar6b-weighted`
  - `WORK/source-import-batch27-spectre/258-source-lt-read-sar6b-weighted`
