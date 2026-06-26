# Source DAC 8bit Ideal Scalar Audit

- Source: `wangx/dac_8bit_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: continuous 8-bit ideal DAC code-to-voltage conversion.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch14-evas/191-dac-8bit-ideal-scalar`
  - `WORK/source-import-batch14-spectre/191-dac-8bit-ideal-scalar`
