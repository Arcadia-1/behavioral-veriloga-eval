# Source ADC Sample Clock Sequencer Audit

- Source: `tangxy/CLOCK_VA_SAMPLE_1800n.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: timer-driven ADC phase sequencer with reset, sample, autozero, conversion, and non-overlap pulses.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch20-evas/223-adc-sample-clock-sequencer`
  - `WORK/source-import-batch20-spectre/223-adc-sample-clock-sequencer`
