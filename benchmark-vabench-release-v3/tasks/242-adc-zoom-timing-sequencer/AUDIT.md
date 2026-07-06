# Source ADC Zoom Timing Sequencer Audit

- Source: `tangxy/CLOCK_VA.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: multi-phase ADC timing generator with reset, sample, SAR, residue, integration, zoom, and zoom reset pulses.
- Import status: certified only after visible compile, EVAS/Spectre semantic checks and parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
