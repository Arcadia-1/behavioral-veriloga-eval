# Source DFF Set Reset Audit

- Source: `gaoya/L4_DFF_VA.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a voltage-coded D flip-flop with active-low asynchronous SETB/RSTB and complementary outputs. Clock rising samples D when both async controls are inactive.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch28-evas/266-source-dff-set-reset`
  - `WORK/source-import-batch28-spectre/266-source-dff-set-reset`
