# Source DAC Serial Accumulator Audit

- Source: `zhangz/DAC_serial_va.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: serial SAR/DAC bit accumulation into a bipolar analog output.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch16-evas/205-dac-serial-accumulator`
  - `WORK/source-import-batch16-spectre/205-dac-serial-accumulator`
