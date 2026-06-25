# Source Ideal Clkmux 8channel Audit

- Source: `wangxy/DAC_4bit_restore_8channel.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked eight-channel analog mux with exposed modulo counter.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch15-evas/199-source-ideal-clkmux-8channel`
  - `WORK/source-import-batch15-spectre/199-source-ideal-clkmux-8channel`
