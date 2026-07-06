# Source SUM5 Signed SAR Weight Audit

- Source: `zhangz/DAC_serial_PPSAR_va.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a 5-input signed SAR weighted summer. Each bit is interpreted as +1 above threshold and -1 below threshold, then combined with 1/2, 1/4, 1/8, 1/16, and 1/32 weights.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
