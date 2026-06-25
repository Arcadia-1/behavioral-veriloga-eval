# Source Phase Detector Chopper Audit

- Source: `wangx/phase_detector.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: chopper phase detector that flips the RF input sign according to the local oscillator polarity.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch22-evas/235-source-phase-detector-chopper`
  - `WORK/source-import-batch22-spectre/235-source-phase-detector-chopper`
