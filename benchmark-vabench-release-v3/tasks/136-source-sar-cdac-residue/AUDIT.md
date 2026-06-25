# Source SAR CDAC Residue Audit

- Source: `caiyizeng25/L3_SAR2_cdac_7b_ideal.va`
- Scenario: sample-and-step SAR CDAC residue update.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch4-evas/136-source-sar-cdac-residue`
  - `WORK/source-import-batch4-spectre/136-source-sar-cdac-residue`
