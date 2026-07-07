# Source Sample Hold 5v Clock Audit

- Source: `wangx/sah_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement an ideal sample-and-hold. When the 5 V clock crosses 2.5 V rising, sample VIN and hold that value on VOUT until the next sample edge.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
