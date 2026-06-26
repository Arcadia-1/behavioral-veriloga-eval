# Source CAL4bit Modulo Audit

- Source: `chengqidong25/CAL4bit.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a scalar-to-4-bit calibration encoder. The input voltage is rounded down to an integer code and emitted as four voltage-coded bits.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/296-cal4bit-modulo`
  - `WORK/source-import-batch32-spectre/296-cal4bit-modulo`
