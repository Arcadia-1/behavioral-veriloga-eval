# Source L2 SAR Logic 4b Audit

- Source: `yueyh/L2_4bit_sar_logic.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: four-bit pipe-SAR controller that gates a comparator clock and records DP/DN decisions into CDAC controls.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch22-evas/234-l2-sar-logic-4b`
  - `WORK/source-import-batch22-spectre/234-l2-sar-logic-4b`
