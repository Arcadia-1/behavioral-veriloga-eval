# Source Ideal DAC 4bit Differential Audit

- Source: `zhaoh/IDEAL_DAC_V.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: edge-sampled code-to-differential-voltage reconstruction.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch10-evas/168-source-ideal-dac-4bit-differential`
  - `WORK/source-import-batch10-spectre/168-source-ideal-dac-4bit-differential`
