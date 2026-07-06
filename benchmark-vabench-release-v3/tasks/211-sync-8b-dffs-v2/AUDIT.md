# Source Sync 8b DFFs V2 Audit

- Source: `zhangm/SYNC_8B_DFFS_V2.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: multi-phase synchronizer that assembles nine delayed data bits through staggered clock phases.
- Import status: certified only after visible compile, EVAS/Spectre semantic checks and parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
