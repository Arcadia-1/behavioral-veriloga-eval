# Source L3 SAR2 Logic 7b Audit

- Source: `caiyizeng25/L3_SAR2_logic_7b_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: active-low comparator-output SAR2 controller with CLK reset/start, SP/SN CDAC controls, and final latched 7-bit DO publication.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled logic behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch24-evas/244-source-l3-sar2-logic-7b`
  - `WORK/source-import-batch24-spectre/244-source-l3-sar2-logic-7b`
