# Source VA Lx DAC Ideal 4b Audit

- Source: `zhangfm/VA_Lx_DAC_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: ready-triggered four-bit unipolar ideal DAC reconstruction.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch15-evas/196-source-va-lx-dac-ideal-4b`
  - `WORK/source-import-batch15-spectre/196-source-va-lx-dac-ideal-4b`
