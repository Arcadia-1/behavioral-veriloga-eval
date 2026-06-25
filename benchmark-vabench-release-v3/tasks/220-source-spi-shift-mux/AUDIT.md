# Source SPI Shift Mux Audit

- Source: `zhangz/L3_SPI_MUX_Big_V1.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: serially shifted mux configuration word with SDO and forwarded SCK.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch19-evas/220-source-spi-shift-mux`
  - `WORK/source-import-batch19-spectre/220-source-spi-shift-mux`
