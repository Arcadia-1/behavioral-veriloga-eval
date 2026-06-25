# Source Foreground Cload Calibrator Audit

- Source: `zhaoh/VA_calib_foreground_cload.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: foreground capacitor-load calibration bit capture and enable handoff.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch18-evas/214-source-foreground-cload-calibrator`
  - `WORK/source-import-batch18-spectre/214-source-foreground-cload-calibrator`
