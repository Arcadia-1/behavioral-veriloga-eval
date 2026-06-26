# Source XOR Phase Detector Audit

- Source: `huangsy/PD_XOR.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a combinational XOR phase detector. UP is high when REF and FB differ; DOWN is high when the logical levels match.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch30-evas/277-xor-phase-detector`
  - `WORK/source-import-batch30-spectre/277-xor-phase-detector`
