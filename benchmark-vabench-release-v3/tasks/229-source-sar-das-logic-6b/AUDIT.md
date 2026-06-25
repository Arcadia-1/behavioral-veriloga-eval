# Source SAR DAS Logic 6b Audit

- Source: `zhangz/SAR_logic_DAS_va.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: six decision-bit differential SAR switching controller with sampling refresh and comparator-coded updates.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch21-evas/229-source-sar-das-logic-6b`
  - `WORK/source-import-batch21-spectre/229-source-sar-das-logic-6b`
