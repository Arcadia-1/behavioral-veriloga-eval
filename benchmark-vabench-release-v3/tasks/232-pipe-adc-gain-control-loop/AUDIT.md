# Source Pipe ADC Gain Control Loop Audit

- Scenario: pipeline ADC backend gain-control loop that alternates plus/minus test DAC codes and updates a 7-bit gain control word.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `l2_core_ready`.
- Rationale: this is an ADC-oriented calibration loop with alternating test stimulus, measured code difference, and gain-control update.
- Counting recommendation: retain as calibration/control L2.

## Window B Calibration Closeout

- Gate 2 status: `cadence_modeling_ready`.
- Evidence: Window B targeted review on 2026-07-03 recorded EVAS hidden gold PASS, 5/5 concrete negatives rejected, AHDL-like lint PASS with 0 diagnostics, and targeted Spectre hidden gold PASS.
- Gold cleanup: integer absolute error is now computed without implicit real-to-integer conversion.
- Counting recommendation: retain as a calibration/control L2 row. `TASKS.json` level is updated from L1 to L2 to match this boundary.
