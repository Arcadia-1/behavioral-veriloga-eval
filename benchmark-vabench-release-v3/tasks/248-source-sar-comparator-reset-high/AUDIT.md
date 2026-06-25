# Source SAR Comparator Reset High Audit

- Source: `caiyizeng25/L3_SAR_comparator_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a clocked SAR comparator that compares VINP/VINN on CMPCK rising and resets both differential outputs high on initial step or CMPCK falling.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch25-evas/248-source-sar-comparator-reset-high`
  - `WORK/source-import-batch25-spectre/248-source-sar-comparator-reset-high`
