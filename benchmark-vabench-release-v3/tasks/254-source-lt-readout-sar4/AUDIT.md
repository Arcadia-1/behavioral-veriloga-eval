# Source LT Readout SAR4 Audit

- Source: `gaoya/LT_READOUT_SAR4_NEW.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a continuous 4-bit SAR readout DAC. DIN0 is the LSB, DIN3 is the MSB, and VOUT equals the unsigned code times 1.8/16.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch26-evas/254-source-lt-readout-sar4`
  - `WORK/source-import-batch26-spectre/254-source-lt-readout-sar4`
