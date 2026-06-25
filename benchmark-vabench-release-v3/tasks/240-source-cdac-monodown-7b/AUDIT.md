# Source CDAC Monodown 7b Audit

- Source: `caiyizeng25/cdac_ideal_monodown.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: sample-and-hold CDAC residue that steps downward on rising monodown control bits.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch23-evas/240-source-cdac-monodown-7b`
  - `WORK/source-import-batch23-spectre/240-source-cdac-monodown-7b`
