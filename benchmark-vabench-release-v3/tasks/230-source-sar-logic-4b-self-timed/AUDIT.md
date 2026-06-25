# Source SAR Logic 4b Self Timed Audit

- Source: `zhangz/L3_logic_4b.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: self-timed four-bit SAR controller that gates the comparator clock and updates top/bottom CDAC controls from comparator pulses.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch21-evas/230-source-sar-logic-4b-self-timed`
  - `WORK/source-import-batch21-spectre/230-source-sar-logic-4b-self-timed`
