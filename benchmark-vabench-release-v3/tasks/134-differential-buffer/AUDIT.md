# Source Differential Buffer Audit

- Source: `liudongyang/TOOL_buffer.va`
- Scenario: differential analog pass-through buffer.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch4-evas/134-differential-buffer`
  - `WORK/source-import-batch4-spectre/134-differential-buffer`
