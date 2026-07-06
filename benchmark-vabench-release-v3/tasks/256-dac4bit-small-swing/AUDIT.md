# Source DAC4bit Small Swing Audit

- Source: `shigao/DAC4bit_1.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a continuous 4-bit small-swing DAC. Decode VD3..VD0 as an unsigned code and map it to `vref * (2*code/15 - 1)` with vref = 20 mV.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
