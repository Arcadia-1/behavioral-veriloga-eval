# Source Pipe 2lane Edge Align Audit

- Source: `guoxy/ideal_PIPE_10B_TI_ALIGN.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: two-lane pipeline data alignment controlled by clock edge polarity.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch16-evas/204-pipe-2lane-edge-align`
  - `WORK/source-import-batch16-spectre/204-pipe-2lane-edge-align`
