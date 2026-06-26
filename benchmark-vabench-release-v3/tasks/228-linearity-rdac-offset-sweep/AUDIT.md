# Source Linearity RDAC Offset Sweep Audit

- Source: `zhaoh/VA_comparator_offset_calib_linearity_rdac.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: comparator offset stimulus generator that alternates bisection search and RDAC code stepping.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch21-evas/228-linearity-rdac-offset-sweep`
  - `WORK/source-import-batch21-spectre/228-linearity-rdac-offset-sweep`
