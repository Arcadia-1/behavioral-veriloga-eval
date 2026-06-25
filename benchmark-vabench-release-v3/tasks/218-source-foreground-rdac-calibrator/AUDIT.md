# Source Foreground RDAC Calibrator Audit

- Source: `zhaoh/VA_calib_foreground_rdac.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: foreground RDAC calibration code capture with enable handoff.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch19-evas/218-source-foreground-rdac-calibrator`
  - `WORK/source-import-batch19-spectre/218-source-foreground-rdac-calibrator`
