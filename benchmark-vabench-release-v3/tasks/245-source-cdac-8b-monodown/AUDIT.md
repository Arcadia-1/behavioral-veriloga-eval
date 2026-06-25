# Source CDAC 8b Monodown Audit

- Source: `liudongyang/L2_cdac_8b_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: sampled 8-bit SAR CDAC residue model that subtracts DCTRL7..DCTRL1 binary weights from the held VIN value.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled residue values from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch24-evas/245-source-cdac-8b-monodown`
  - `WORK/source-import-batch24-spectre/245-source-cdac-8b-monodown`
