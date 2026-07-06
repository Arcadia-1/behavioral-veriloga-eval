# Source Accum3 Pulse Audit

- Source: `huangsy/ACCUM_3_bit.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a 3-bit modulo accumulator pulse generator. The internal count starts at 7, increments on each rising edge, and OUT is high only when count is 0.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
