# Source Clock Sample 1600n Sequencer Audit

- Source: `tangxy/CLOCK_VA_SAMPLE_1600n.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: ADC sample timing generator with reset, sample, non-overlap, residue, and conversion windows.
- Import status: certified only after visible compile, EVAS/Spectre semantic checks and parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
