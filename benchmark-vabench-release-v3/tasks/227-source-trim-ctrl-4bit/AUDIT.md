# Source Trim Ctrl 4bit Audit

- Source: `guoxy/ideal_TRIM_CTRL_4BITS.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: analog trim-code decoder that converts an input code voltage into four binary trim control rails.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch20-evas/227-source-trim-ctrl-4bit`
  - `WORK/source-import-batch20-spectre/227-source-trim-ctrl-4bit`
