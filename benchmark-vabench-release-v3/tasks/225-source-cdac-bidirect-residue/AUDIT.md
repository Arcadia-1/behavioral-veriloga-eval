# Source CDAC Bidirect Residue Audit

- Source: `caiyizeng25/cdac_ideal_bidirect.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: sampled residue update with one positive MSB step followed by binary weighted subtractive control edges.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch20-evas/225-source-cdac-bidirect-residue`
  - `WORK/source-import-batch20-spectre/225-source-cdac-bidirect-residue`
