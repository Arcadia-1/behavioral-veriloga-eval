# Source LT Read SAR7B Weighted Audit

- Source: `gaoya/LT_READ_SAR7B.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a continuous 8-input SAR readout using the source model weights D7..D0 = 1, 1/2, ..., 1/128 times vref, offset by -vref.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
