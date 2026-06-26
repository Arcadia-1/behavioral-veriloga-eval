# Source SAR Weighted Sum Audit

- Source: `shigao/V_SAR_sum.va`
- Scenario: SAR non-binary weighted residue/code reconstruction.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch3-evas/127-sar-weighted-sum`
  - `WORK/source-import-batch3-spectre/127-sar-weighted-sum`
