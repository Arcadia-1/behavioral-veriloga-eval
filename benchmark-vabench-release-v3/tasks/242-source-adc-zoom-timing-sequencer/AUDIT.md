# Source ADC Zoom Timing Sequencer Audit

- Source: `tangxy/CLOCK_VA.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: multi-phase ADC timing generator with reset, sample, SAR, residue, integration, zoom, and zoom reset pulses.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch23-evas/242-source-adc-zoom-timing-sequencer`
  - `WORK/source-import-batch23-spectre/242-source-adc-zoom-timing-sequencer`
