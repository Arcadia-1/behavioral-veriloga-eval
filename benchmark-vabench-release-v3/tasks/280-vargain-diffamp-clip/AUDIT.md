# Source Vargain Diffamp Clip Audit

- Source: `wangx/vargain_diffamp.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a voltage-controlled differential gain block with output clipping. The output is 3*(CTRL_P-CTRL_N)*((INP-INN)-0.05) limited to +/-1 V.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch31-evas/280-vargain-diffamp-clip`
  - `WORK/source-import-batch31-spectre/280-vargain-diffamp-clip`
