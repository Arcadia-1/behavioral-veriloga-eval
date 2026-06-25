# Source Two Period Sample Delay Audit

- Source: `zhangzixuan/_tool_delay_two_period.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked one-sample analog pipeline delay.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch10-evas/169-source-two-period-sample-delay`
  - `WORK/source-import-batch10-spectre/169-source-two-period-sample-delay`
