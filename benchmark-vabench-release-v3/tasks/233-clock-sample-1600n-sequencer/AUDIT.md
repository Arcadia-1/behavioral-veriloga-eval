# Source Clock Sample 1600n Sequencer Audit

- Source: `tangxy/CLOCK_VA_SAMPLE_1600n.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: ADC sample timing generator with reset, sample, non-overlap, residue, and conversion windows.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch22-evas/233-clock-sample-1600n-sequencer`
  - `WORK/source-import-batch22-spectre/233-clock-sample-1600n-sequencer`
