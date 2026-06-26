# Source Deadband Diffamp Audit

- Source: `wangx/deadband_diffamp.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a differential deadband amplifier. Inside +/-100 mV it outputs 20 mV leakage; outside it applies asymmetric low/high gains.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/290-deadband-diffamp`
  - `WORK/source-import-batch32-spectre/290-deadband-diffamp`
