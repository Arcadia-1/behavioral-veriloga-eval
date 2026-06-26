# Source Clocked ADC3bit Audit

- Source: `wangx/adc_8bit.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a clocked 3-bit ADC. On each rising clock edge, quantize VIN in [0,1] to code floor(8*VIN), clipped to 0..7.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/295-clocked-adc3bit`
  - `WORK/source-import-batch32-spectre/295-clocked-adc3bit`
