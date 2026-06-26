# Source Differential DAC Calc 6b Audit

- Source: `zhangm/DAC_CALC_VA.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked complementary DAC voltage reconstruction.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch12-evas/182-differential-dac-calc-6b`
  - `WORK/source-import-batch12-spectre/182-differential-dac-calc-6b`
