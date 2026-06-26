# Source Bipolar DFF Sample Audit

- Source: `wangx/d_ff.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a rising-edge D flip-flop with bipolar outputs. Q/QB are +1/-1 V complements sampled from D at each clock edge.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/299-source-bipolar-dff-sample`
  - `WORK/source-import-batch32-spectre/299-source-bipolar-dff-sample`
