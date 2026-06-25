# Source DAC Ideal 4b Offset Audit

- Source: `caiyizeng25/dac_ideal_4b.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: four-bit weighted DAC compression with fixed offset term.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch15-evas/200-source-dac-ideal-4b-offset`
  - `WORK/source-import-batch15-spectre/200-source-dac-ideal-4b-offset`
