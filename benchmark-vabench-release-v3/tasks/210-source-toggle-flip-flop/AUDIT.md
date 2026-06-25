# Source Toggle Flip Flop Audit

- Source: `wangx/t_ff.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: rising-edge triggered T flip-flop with complementary voltage outputs.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch17-evas/210-source-toggle-flip-flop`
  - `WORK/source-import-batch17-spectre/210-source-toggle-flip-flop`
