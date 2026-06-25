# Source Divide By Two Toggle Audit

- Source: `zhangz/L2_Divider_2.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a divide-by-two edge toggle. OUT toggles on every rising CLK edge, starting low and becoming high after the first edge.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch30-evas/275-source-divide-by-two-toggle`
  - `WORK/source-import-batch30-spectre/275-source-divide-by-two-toggle`
