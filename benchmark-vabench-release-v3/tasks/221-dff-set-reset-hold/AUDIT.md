# Source DFF Set Reset Hold Audit

- Source: `zhangm/DFFRSHQ.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: D flip-flop with asynchronous active-low set/reset priority and held clocked data.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch19-evas/221-dff-set-reset-hold`
  - `WORK/source-import-batch19-spectre/221-dff-set-reset-hold`
