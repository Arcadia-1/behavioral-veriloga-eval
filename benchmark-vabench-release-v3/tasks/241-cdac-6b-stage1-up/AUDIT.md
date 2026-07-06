# Source CDAC 6b Stage1 Up Audit

- Source: `zhangym/cdac_6b_ideal_stage1.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: sample-and-hold CDAC residue that steps upward on rising 6-bit control bits.
- Import status: certified only after visible compile, EVAS/Spectre semantic checks and parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
